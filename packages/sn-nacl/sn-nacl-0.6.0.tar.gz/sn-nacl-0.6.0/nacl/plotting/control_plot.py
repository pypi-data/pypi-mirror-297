import numpy as np
import pylab as pl
import sncosmo
from nacl.models.salt2.salt import SALT2Like
source = sncosmo.get_source('salt2', version='2.4')
import matplotlib.colors as mcolors
import numpy.polynomial.polynomial as nppol

def plot_stacked_residuals_snake(tds, pars, v, var):
    """
    Plotting the stacked residuals comparing the all of the data and the model
    
    Parameters:
    ----------
    tds : nacl.dataset.TrainingDataset 
          initial training dataset
          
    model : nacl.models.salt2.salt.SALT2Like
            the model
        
    v : numpy.array
        result values that come out of the NaCl model. Default=None
    
    """

    
    wl = tds.spec_data.wavelength / (1. + tds.spec_data.z)
    ph = (tds.spec_data.mjd - pars['tmax'].full[tds.spec_data.sn_index]) / (1 + tds.spec_data.z)

    pl.figure(figsize=(14, 10))
    idx = tds.spec_data.valid > 0
    res = tds.spec_data.flux - v[len(tds.lc_data.flux):len(tds.lc_data.flux)+len(tds.spec_data.flux)]
    wres = res / (tds.spec_data.fluxerr + np.sqrt(var[len(tds.lc_data.flux):len(tds.lc_data.flux)+len(tds.spec_data.flux)]))
    ii = ph[idx] < 50.
    pl.hexbin(wl[idx][ii], ph[idx][ii], wres[idx][ii], vmin=-2.5, vmax=2.5)
    pl.title('weighted residuals Spectra', fontsize=16)
    pl.xlabel(r'restframe $\lambda [\AA]$', fontsize=16)
    pl.ylabel('restframe phase [days]', fontsize=16)
    pl.colorbar()
    pl.show()
    
    wl = tds.lc_data.wavelength / (1. + tds.lc_data.z)
    ph = (tds.lc_data.mjd - pars['tmax'].full[tds.lc_data.sn_index]) / (1 + tds.lc_data.z)

    pl.figure(figsize=(14, 10))
    idx = tds.lc_data.valid > 0
    res = tds.lc_data.flux - v[:len(tds.lc_data.flux)]
    wres = res / (tds.lc_data.fluxerr + np.sqrt(var[:len(tds.lc_data.flux)]) )
    ii = ph[idx] < 50.
    pl.hexbin(wl[idx][ii], ph[idx][ii], wres[idx][ii], vmin=-2.5, vmax=2.5)
    pl.title('weighted residuals LCs', fontsize=16)
    pl.xlabel(r'restframe $\lambda [\AA]$', fontsize=16)
    pl.ylabel('restframe phase [days]', fontsize=16)
    pl.colorbar()
    pl.show()
    
def plot_band_residuals_z(tds, v, var):
    """
    Plotting residuals in each band
    
    Parameters:
    -----------
    tds : nacl.TrainingDataset
        The training dataset
    v : np.array
        The model evaluation
    var : np.array
        The error model
    """
    nb_bands = len(tds.lc_data.band_set)
    v_lc = v[:len(tds.lc_data)]
    
    fig, axs = pl.subplots(nrows = nb_bands, ncols=2, width_ratios=np.array([3,1]), sharey='row', figsize=(14,10))
    bands = np.unique(tds.lc_data.nt['band'])
    color = ['azure', 'black', 'blue', 'brown', 'chocolate', 'cyan', 'darkblue', 'darkcyan', 'darkgreen', 'darkolivegreen', 'darkred', 'darkorange',
    'darkmagenta', 'darkviolet', 'green', 'olive', 'red', 'orange', 'magenta', 'lime', 'gold', 'lavender', 'pink', 'teal']
    #cc = np.random.choice(np.array(list(mcolors.cnames.keys())), size=nb_bands, replace=False)
    cc = np.random.choice(np.array(color), size=nb_bands, replace=False)
    for i in range(nb_bands):
        idx = tds.lc_data.band == bands[i]
        band_name = tds.lc_data.band[idx][0]
        
        res = tds.lc_data.flux[idx] - v_lc[idx]
        z = tds.lc_data.z[idx]
        
        axs[i,0].errorbar(z, res, yerr = tds.lc_data.fluxerr[idx], fmt='.', label=band_name, color=cc[i])
        axs[i,1].hist(res, bins=100, orientation='horizontal', color=cc[i])
        axs[i,1].set_ylim(np.mean(res) -5*np.std(res), np.mean(res) + 5*np.std(res))
        
        #reindexing = sorted(enumerate(z), key = lambda x:x[1])
        #z_idx = np.array([index for index, value in reindexing])
        #axs[i].fill_between(z[z_idx], res[z_idx]+np.sqrt(var[:len(tds.lc_data)][idx][z_idx]), res[z_idx]-np.sqrt(var[:len(tds.lc_data)][idx][z_idx]), alpha=0.5)
        
        
        axs[i,0].set_xlabel('z')
        axs[i,0].set_ylabel('res')
        axs[i,0].legend()
        
    pl.tight_layout()
    
    
def plot_band_residuals_phase(tds, pars, v, var):
    """
    Plotting residuals in each band
    
    Parameters:
    -----------
    tds : nacl.TrainingDataset
        The training dataset
    v : np.array
        The model evaluation
    var : np.array
        The error model
    """
    nb_bands = len(tds.lc_data.band_set)
    v_lc = v[:len(tds.lc_data)]
    
    fig, axs = pl.subplots(nrows = nb_bands, ncols=2, width_ratios=np.array([3,1]), sharey='row', figsize=(14,10))
    bands = np.unique(tds.lc_data.nt['band'])
    color = ['azure', 'black', 'blue', 'brown', 'chocolate', 'cyan', 'darkblue', 'darkcyan', 'darkgreen', 'darkolivegreen', 'darkred', 'darkorange',
    'darkmagenta', 'darkviolet', 'green', 'olive', 'red', 'orange', 'magenta', 'lime', 'gold', 'lavender', 'pink', 'teal']
    #cc = np.random.choice(np.array(list(mcolors.cnames.keys())), size=nb_bands, replace=False)
    cc = np.random.choice(np.array(color), size=nb_bands, replace=False)
    for i in range(nb_bands):
        idx = tds.lc_data.band == bands[i]
        band_name = tds.lc_data.band[idx][0]
        
        res = tds.lc_data.flux[idx] - v_lc[idx]
        p = tds.lc_data.mjd[idx] - pars['tmax'].full[tds.lc_data.sn_index][idx]
        
        axs[i,0].errorbar(p, res, yerr = tds.lc_data.fluxerr[idx], fmt='.', label=band_name, color=cc[i])
        axs[i,1].hist(res, bins=100, orientation='horizontal', color=cc[i])
        axs[i,1].set_ylim(np.mean(res) -5*np.std(res), np.mean(res) + 5*np.std(res))
        
        #reindexing = sorted(enumerate(z), key = lambda x:x[1])
        #z_idx = np.array([index for index, value in reindexing])
        #axs[i].fill_between(z[z_idx], res[z_idx]+np.sqrt(var[:len(tds.lc_data)][idx][z_idx]), res[z_idx]-np.sqrt(var[:len(tds.lc_data)][idx][z_idx]), alpha=0.5)
        
        
        axs[i,0].set_xlabel('phase')
        axs[i,0].set_ylabel('res')
        axs[i,0].legend()
        
    pl.tight_layout()
    
    
def plot_cs_variance(tds, pars, cs):
    """
    Color scatter varaince
    """
    lc_data = tds.lc_data
    _restframe_wl = lc_data.wavelength / (1. + lc_data.z)
    _, ii = np.unique(lc_data.lc_index, return_index=True)
    ii.sort()
    restframe_wl = _restframe_wl[ii]
    
    sigma_kappa = pars['sigma_kappa'].full
    #var = np.exp(np.polyval(sigma_kappa, cs.reduced_restframe_wl))
    var = np.exp(nppol.Polynomial(sigma_kappa)(cs.reduced_restframe_wl))
    
    pl.figure(figsize=(12,8))
    pl.plot(restframe_wl, var, 'b.')
    pl.xlabel('restframe wavelengths')
    pl.ylabel(r'$\sigma_{\kappa}$')
    pl.title('color scatter variance')
    
def plot_cs_cl(tds, logs, cl):
    """
    Color law after each fit
    """
    lc_data = tds.lc_data
    _restframe_wl = lc_data.wavelength / (1. + lc_data.z)
    _, ii = np.unique(lc_data.lc_index, return_index=True)
    ii.sort()
    restframe_wl = _restframe_wl[ii]
    
    pars_final = logs[-1].pars['CL'].full
    pars_no_cs = logs[-2].pars['CL'].full
    pars_init = logs[0].pars['CL'].full
    
    fig, axs = pl.subplots(nrows = 2, ncols=1, height_ratios=np.array([3,1]), figsize=(14,10))
    
    axs[0].plot(restframe_wl, cl(restframe_wl, pars_init)[0], 'b.', label='SALT2.4')
    axs[0].plot(restframe_wl, cl(restframe_wl, pars_no_cs)[0], 'r.', label='no color scatter')
    axs[0].plot(restframe_wl, cl(restframe_wl, pars_final)[0], 'g.', label='full fit')
    
    axs[0].set_xlabel('restframe wavelengths')
    axs[0].set_label(r'CL$(\lambda)$')
    axs[0].set_title('Color Law evolution')
    
    axs[0].legend()
    
    axs[1].plot(restframe_wl, cl(restframe_wl, pars_init)[0] - cl(restframe_wl, pars_final)[0], 'b.', label='SALT2.4 - full fit')
    
    axs[1].set_xlabel('restframe wavelengths')
    axs[1].set_label(r'$\Delta$CL$(\lambda)$')
    axs[1].set_title('Color Law difference')
    
    axs[1].legend()
    
    
def plot_kappa(tds, pars):
    """
    Color scatter coeffs
    """
    lc_data = tds.lc_data
    _restframe_wl = lc_data.wavelength / (1. + lc_data.z)
    _, ii = np.unique(lc_data.lc_index, return_index=True)
    ii.sort()
    restframe_wl = _restframe_wl[ii]
    
    pl.figure(figsize=(12,8))
    pl.plot(restframe_wl, pars['kappa_color'].full, 'b.')
    pl.xlabel('restframe wavelengths')
    pl.ylabel(r'$\kappa_{color}$')
    pl.title('kappa color')
    

