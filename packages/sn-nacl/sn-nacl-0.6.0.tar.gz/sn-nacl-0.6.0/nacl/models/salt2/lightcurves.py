"""SN light curve eval unit
"""

import logging

import time
import numpy as np
import scipy

# import numexpr as ne

try:
    from sparse_dot_mkl import gram_matrix_mkl, dot_product_mkl
except:
    logging.warning('module: `sparse_dot_mkl` not available')
else:
    logging.info('sparse_dot_mkl found. Building hessian should be faster.')

from nacl.sparseutils import kron_product_by_line, CooMatrixBuff, CooMatrixBuff2
from bbf import magsys


class LightcurveEvalUnit:
    """The evaluation unit for light curves.

    This class evaluates all light curves present in the training dataset at
    once for increased efficiency.

    """
    def __init__(self, model):
        """
        Initialize the LightcurveEvalUnit.

        Parameters
        ----------
        model : object
            The main model object containing the training dataset.
        """
        self.model = model
        self.training_dataset = model.training_dataset
        self.gram = self.model.gram.todense()
        self.color_law = self.model.color_law

        nb_lightcurves = len(self.training_dataset.lc_db)
        filter_db_basis_size = len(model.filter_db.basis)
        F = np.zeros((nb_lightcurves, filter_db_basis_size))
        for lc in self.training_dataset.lc_db:
            # tqz, _ = self.model.filter_db.insert(lc.band, z=lc.z)
            tr_data = self.model.filter_db.insert(lc.band, z=lc.z)
            F[lc.lc_index, :] = tr_data.tq

        self.flux_scales = self.compute_flux_scales()
        self.flux_scales *= self.model.norm

        # filter projections
        self.filter_projections = (self.gram @ F.T).T
        self.meas_filter_projections = \
            self.filter_projections[self.training_dataset.lc_data.lc_index]

    def compute_flux_scales(self):
        """Compute the flux scales for the training dataset.

        The flux scales are necessary to convert model fluxes to observed
        fluxes in units defined by the observer.

        Returns
        -------
        numpy.array
            Array of flux scales.

        Notes
        -----
        Here, we assume that all mags are in the AB mag system. This may not be true.
        This need to be corrected.

        """
        zp_scale = self.training_dataset.lc_data.zp_scale

        # also insert the filter at z = 0, needed to compute integrals of AB spectrum
        bands = np.unique(self.training_dataset.lc_db.band)
        for b in bands:
            self.model.filter_db.insert(b, z=0.)

        ms = magsys.SNMagSys(self.model.filter_db)
        int_AB_dict = dict(zip(bands, [10.**(0.4 * ms.get_zp(b.lower())) for b in bands]))
        int_AB = np.array([int_AB_dict[b] for b in self.training_dataset.lc_data.band])
        flux_scales = int_AB / zp_scale
        return flux_scales

    def __call__(self, pars, jac=False):
        """Evaluate the light curve model for a given set of parameters.

        Parameters
        ----------
        pars : nacl.fitparameters.FitParameters
            The current set of fit parameters.
        jac : bool, optional
            Whether to compute and return the Jacobian matrix. Defaults to False.

        Returns
        -------
        numpy.array
            Model flux values.
        scipy.sparse.coo_matrix, optional
            Jacobian matrix if `jac` is True.

        """
        lc_data = self.training_dataset.lc_data
        lc_db = self.training_dataset.lc_db

        wl_basis = self.model.basis.bx
        ph_basis = self.model.basis.by
        n_wl, n_ph = len(wl_basis), len(ph_basis)

        # pick matrix
        n_lc, n_meas = len(lc_db), len(lc_data)

        # phases
        zz = 1. + lc_data.z
        tmax = pars['tmax'].full[lc_data.sn_index]
        restframe_phases = (lc_data.mjd - tmax) / zz
        J_phase_sparse = ph_basis.eval(restframe_phases + self.model.delta_phase)
        J_phase = np.array(J_phase_sparse.todense())


        if 'eta_calib' in pars._struct.slices:
            calib_corr = 1. + pars['eta_calib'].full[lc_data.band_index]
        else:
            calib_corr = np.ones(len(lc_data.band_index))

        if 'kappa_color' in pars._struct.slices:
            cs_corr = 1. + pars['kappa_color'].full[lc_data.lc_index]
        else:
            cs_corr = np.ones(len(lc_data.lc_index))

        M0 = pars['M0'].full.reshape(n_ph, n_wl)
        M1 = pars['M1'].full.reshape(n_ph, n_wl)
        C0_ = np.array(M0.dot(self.meas_filter_projections.T))
        C0 = (J_phase * C0_.T).sum(axis=1)
        C1_ = np.array(M1.dot(self.meas_filter_projections.T))
        C1 = (J_phase * C1_.T).sum(axis=1)

        X0 = pars['X0'].full[lc_data.sn_index]
        X1 = pars['X1'].full[lc_data.sn_index]
        col = pars['c'].full[lc_data.sn_index]

        # color law - so here, we decide to move it out of the integral
        # maybe we need to add a small correction
        cl_pars = pars['CL'].full

        restframe_wavelength = lc_data.wavelength / zz
        cl_pol, J_cl_pol = self.color_law(restframe_wavelength,
                                          cl_pars, jac=jac)
        cl = np.power(10., 0.4 * col * cl_pol)

        pca = C0 + X1 * C1
        model_val = X0 * pca * cl * zz * calib_corr * cs_corr

        if not jac:
            v = np.zeros(len(self.training_dataset))
            v[lc_data.row] = self.flux_scales * model_val
            return v

        # jacobian
        N = len(self.training_dataset)
        n_free_pars = len(pars.free)

        # since the hstack is taking a lot of time and memory, we do things differently:
        # we allocate 3 large buffers for the jacobian i, j, vals, and we
        # update them in place.

        # estimated size of the derivatives
        logging.debug(' ... kron')
        K = kron_product_by_line(J_phase_sparse, self.meas_filter_projections)
        logging.debug(f'     -> done, K.nnz={K.nnz} nnz_real={(K.data != 0.).sum()} {len(K.row)}')

        estimated_size = 2 * K.nnz   # dMdM0 and dMdM1
        estimated_size += 6 * N      # local parameters (dMdX0, dMdX1, dMdcol, dMtmax, dMdeta, dMdkappa)
        nnz = len(J_cl_pol.nonzero()[0])
        estimated_size += nnz
        logging.debug(f'estimated size: {estimated_size}')

        buff = CooMatrixBuff2((N, n_free_pars)) # , estimated_size)
        self.K = K
        self.X0 = X0
        self.cl = cl
        self.calib_corr = calib_corr
        self.cs_corr = cs_corr
        self.zz = zz

        # we start with the largest derivatives: dMdM0 and dMdM1
        # dMdM0
        # we could write it as:
        # v_ = X0[K.row] * K.data * cl[K.row] * calib_corr[K.row] * cs_corr[K.row] * zz[K.row]
        # but it is slow. So, we re-arrange it as:
        i_ = lc_data.row[K.row]
        v_ = X0 * cl * calib_corr * cs_corr * zz
        # vv_, dd_ = v_[K.row], K.data
        # v_ = ne.evaluate('vv_ * dd_')
        v_ = v_[K.row] * K.data
        buff.append(i_,
                    pars['M0'].indexof(K.col),
                    v_)

        # dMdM1
        # X1_ = X1[K.row]
        buff.append(lc_data.row[K.row],
                    pars['M1'].indexof(K.col),
                    v_ * X1[K.row])

        del K
        del i_
        del v_

        # dMdtmax
        phase_basis = self.model.basis.by
        dJ = np.array(phase_basis.deriv(restframe_phases + self.model.delta_phase).todense())
        dC0 = (dJ * C0_.T).sum(axis=1)
        dC1 = (dJ * C1_.T).sum(axis=1)
        buff.append(lc_data.row,
                    pars['tmax'].indexof(lc_data.sn_index),
                    # ne.evaluate('-X0 * (dC0 + X1 * dC1) * cl * calib_corr * cs_corr'))
                    -X0 * (dC0 + X1 * dC1) * cl * calib_corr * cs_corr)

        del dJ
        del C0_
        del C1_

        # dMdcl
        JJ = scipy.sparse.coo_matrix(J_cl_pol)
        model_val_, col_, d_ = model_val[JJ.row], col[JJ.row], JJ.data
        buff.append(JJ.row,
                    pars['CL'].indexof(JJ.col),
                    # ne.evaluate('model_val_ * 0.4 * np.log(10.) * col_ * d_'))
                    # self.flux_scales[JJ.row] * model_val[JJ.row] * 0.4 * np.log(10.) * col[JJ.row] * JJ.data)
                    model_val[JJ.row] * 0.4 * np.log(10.) * col[JJ.row] * JJ.data)

        del JJ
        del model_val_
        del col_
        del d_

        # dMdX0
        buff.append(lc_data.row,
                    pars['X0'].indexof(lc_data.sn_index),
                    pca * cl * zz * calib_corr * cs_corr)

        # dMdX1
        buff.append(lc_data.row,
                    pars['X1'].indexof(lc_data.sn_index),
                    X0 * C1 * cl * zz * calib_corr * cs_corr)

        # dMdcol
        buff.append(
            lc_data.row,
            pars['c'].indexof(lc_data.sn_index),
            model_val * 0.4 * np.log(10.) * cl_pol)

        # dMdeta
        if 'eta_calib' in pars._struct:
            buff.append(lc_data.row,
                        pars['eta_calib'].indexof(lc_data.band_index),
                        X0 * pca * cl * zz * cs_corr)

        # dMkappa
        if 'kappa_color' in pars._struct:
            buff.append(lc_data.row,
                        pars['kappa_color'].indexof(lc_data.band_index),
                        X0 * pca * cl * zz * calib_corr)

        logging.debug(' -> tocoo()')
        J = buff.tocoo()
        del buff

        # multiply the data by the flux scales
        # to express fluxes in observer units
        J.data *= self.flux_scales[J.row]
        v = np.zeros(len(self.training_dataset))
        v[lc_data.row] = self.flux_scales * model_val

        return v, J
