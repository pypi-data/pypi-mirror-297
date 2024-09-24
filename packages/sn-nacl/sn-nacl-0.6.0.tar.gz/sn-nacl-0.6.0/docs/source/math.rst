.. include:: macros.rst

NaCl likelihood and Normal equations
====================================

Generalities
------------

In this section, we explicit the equations behind the NaCl training process.
The main complication comes from the fact that the NaCl model (like all models
proposed so far) does not capture the entirety of the supernova diversity.  In
other terms, after the training, the measurement uncertainties do not allow to
explain the totality of the variance of the residuals. It is therefore
necessary to build a model of this excess variance, and incorporate it in the
training likelihood.  Another source of complexity is that several components
of the error model, including components that are unknown a priori are
non-diagonal, which leads to normal equations which are computationnaly
untractable when the number of supernovae increases beyond O(1000). 


Notations
---------

Data
++++

We group the photometric and spectroscopic measurements in a single noted
:math:`\vec{Y}`. The model expects up to 3 blocks of data, aligned with the
contents of the `TrainingDataset`:

.. math::
   \vec{Y} = \begin{pmatrix}
   \vec{Y}_{\mathrm{phot}} \\
   \vec{Y}_\mathrm{spec} \\
   \vec{Y}_{\mathrm{spphot}} \\
   \end{pmatrix}

We note :math:`N` the size of :math:`\vec{Y}`.

Model
+++++

The NaCl model takes as an input a training dataset and predicts the values of
components the data, :math:`\vec{Y}`, as a function of a vector of unknown
parameters, :math:`vec{\theta}`. Some of the parameters are specific to each
SN, e.g.  :math:`X_0, X_1, c`, others are specific to the model, e.g. the
parameters which define the :math:`M0, M1` surfaces, or the color law. The
former are the true parameters of interest of the fit, from which we derive
cosmological distances. We group them into a block, :math:`\vec{\xi}`. The
former are the model parameters, which we group into a block
:math:`\vec{\beta}`.

.. math::
   \vec{\theta} = \begin{pmatrix}
   \vec{\xi} \\
   \vec{\beta} \\
   \end{pmatrix}


Noise, error model
++++++++++++++++++

The training data is affected by noise.

First, there is noise of instrumental origin. We generally distinguish two
components: 

  - uncorrelated measurement noise :math:`n_{\mathrm{m}}` (poisson noise
    principally), which is assumed to be gaussian
    :math:`n_{\mathrm{m}} = {\cal N}(0, \vec{V}_{\mathrm{m}})`, with 
    :math:`\vec{V}_{\mathrm{m}}` the covariance matrix of this noise 
    diagonal. :math:`\vec{V}_{\mathrm{m}}` is reported by the observers and is
    not re-evaluated in the training process.

  - calibration noise, :math:`n_{\mathrm{cal}}`, also assumed to be gaussian,
    of covariance matrix :math:`\vec{V}_{\mathrm{cal}}`:
    :math:`n_{\mathrm{cal}} \sim {\cal N}(0, \vec{V}_{\mathrm{cal}})`. This
    noise typically correlates all the measurements taken in the same band
    hence, :math:`\vec{V}_{\mathrm{cal}}` is not diagonal. The exact structure
    of :math:`\vec{V}_{\mathrm{cal}}` depends on the survey strategy and
    analysis procedure. Again, :math:`\vec{V}_{\mathrm{cal}}` is assumed to be
    known and not re-evaluated during training. 

The two components above do not permit to explain the variance of the training
residuals. The excess variance observed is attributed to the fact that the
model, cannot capture the full diversity of the SNIa family. We model this 
situation with additional noise components, whose properties are inferred from 
the data itself. The current model includes classically:

  - a so-called *error snake*, which describes the uncorrelated part of the
    residual variance around the model. We model it as:
    :math:`n_{\mathrm{snake}} = {\cal N}(0, \mathrm{V}_{\mathrm{snake}})`.
    :math:`\vec{V}_{\mathrm{snake}}` is a diagonal matrix. It is unknown a
    priori and must be determined during the training. It is generally
    parametrized as a function of the model parameters :math:`\vec{\beta}` and
    specific error-snake parameters, :math:`\gamma`. 

  - a second component, the *color scatter* to describe the correlated
    variability observed in the training residuals, around the color law. 
    The color scatter variability is parametrized as a function of 
    specific parameters, :math:`\vec{\sigma}`, which are determined 
    during the training. 

With these new components, the model becomes:

.. math::
   \vec{Y} = \vec{M}(\vec{\xi}, \vec{\beta}) + \vec{n}_{\mathrm{meas}} + \vec{n}_{\mathrm{cal}} + \vec{n}_{\mathrm{snake}} + \vec{n}_{\mathrm{cscatter}}

with the noise terms :math:`\vec{n}_{\mathrm{snake}}` and
:math:`\vec{n}_{\mathrm{cscatter}}` unknown a priori and inferred during
training. 

The training parameter vector is extended as follows:

.. math::
   \vec{\theta} = \begin{pmatrix}
   \vec{\xi} \\
   \vec{\beta} \\
   \vec{\gamma} \\
   \vec{\sigma} \\
   \end{pmatrix}

and the full training log-likelihood is:

.. math::
   -2 \ln{\cal L} = \vec{R}_{\vec{\theta}}^T \vec{V}_{\vec{\beta\gamma\sigma}}^{-1} \vec{R}_{\vec{\theta}} + \ln |\vec{V}_{\vec{\beta\gamma\sigma}}|

where :math:`\vec{V}_{\vec{\beta\gamma\sigma}}` is the sum of the covariance
matrices of all the noise components discussed above:

.. math::
   \vec{V}_{\vec{\beta\gamma\sigma}} = \vec{V}_{\mathrm{meas}} + \vec{V}_{\mathrm{cal}} + \vec{V}_{\mathrm{snake}|\vec{\beta\gamma}} + \vec{V}_{\mathrm{cscatter}|\vec{\sigma}}

Since :math:`\vec{V}` is now a function of the training parameters, we cannot
discard the :math:`\ln |\vec{V}|` term in the log-likelihood. This complicates
the normal equations a little, but in a very tractable way, as we will see
below. What is *not* tractable, on the other hand, is the inversion of the full
non-diagonal covariance matrix. How to deal with this problem is the subject of
the next section.


Correlated error models
+++++++++++++++++++++++

The contribution of the error snake is diagonal. We can add it to the
measurement covariance matrix without increasing the complexity of the problem.
On the other hand, calibration and error snake are not diagonal. With :math:`N
\sim 10^6` measurements, this leads to very large covariance matrices, which
simply do not fit in memory -- even if the matrix itself is sparse, its inverse
is generally not. 

Calibration
...........

The calibration noise affects all measurements taken in a same band in a
correlated way.  The exact structure of the calibration noise matrix depends on
the calibration process and may be quite complex. However, it is generally true
that its dimensionality is of the order of :math:`N_{\mathrm{bands}}`, the
number of bands in the dataset. We can therefore write:

.. math::
   \vec{n}_{\mathrm{cal}} = \vec{K} \vec{\eta}\ \ \ \mathrm{with}\ \ \ \vec{\eta} = {\cal N}(0, \vec{V_\eta})

where :math:`\vec{\eta}` is modeled as a gaussian random vector of covariance
matrix :math:`\vec{V}_{\vec{\eta}}`. The size of this vector depends on how we
model the calibration process. The simplest model we can think of uses one
:math:`\eta` parameter per band (see below). As mentioned above,
:math:`\vec{V_\eta}` is estimated by the photometric pipeline and not
re-evaluated in the training.

Since the standard likelihood:

.. math::
   -2 \ln {\cal L} = (\vec{Y} - \vec{M}_{\vec{\xi\beta}})^T (\vec{V}_{\mathrm{meas}} + 
   \vec{K} \vec{V}_{\vec{\eta}} \vec{K}^T)^{-1} (\vec{Y} - \vec{M}_{\vec{xi,\beta}})

is not tractable, we notice that:

.. math::
   {L}(\vec{Y},\vec{\eta} | \vec{\beta}) = L(\vec{Y} | \vec{\beta},\vec{\eta}) \times p(\vec{\eta})

which means that we can consider the :math:`\vec{\eta}` as additional
parameters of the model itself, held by a prior. This prior is known, since we
know that :math:`\vec{\eta} \sim {\cal N}(0, \vec{V_\eta})`. The associated 
log-likelihood becomes:

.. math::
   -2 \ln {\cal L} = (\vec{Y} - \vec{M}_{\vec{\xi, \beta, \ldots, \eta}})^T \vec{V}^{-1}_{\mathrm{meas}} (\vec{Y} - \vec{M}_{\vec{\xi, \beta, \ldots, \eta}}) + \vec{\eta}^T \vec{V_\eta}^{-1} \vec{\eta}
  
This new form is easy to handle: the measurement covariance matrix stays
diagonal, and the calibration information is enclosed in a
low-dimensionality quadradtic prior. We note that the normal equation we get
from this reformulated likelihood is *exactly* the same as that derivated
from the original likelohood, as shown in an appendix of the NaCl paper.

Color scatter
.............

To incorporate the color scatter error model, we use the exact same technique,
with the variation that, this time, the gaussian prior is not known and must be
determined during training. 

We extend the model parameter vector  a new set of latent parameters
:math:`\vec{\kappa}`, held by a gaussian prior of the form
:math:`\vec{\kappa}^T \vec{V}_\vec{\sigma_\kappa}^{-1}\vec{\kappa}` where
:math:`\vec{V}_{\sigma_\kappa}` is parametrized as a function of the
:math:`\vec{\sigma_\kappa}` parameters.  We add to the reformulated
log-likelihood (1) the prior above (2) a term of the form :math:`\ln
|\vec{V_{\sigma_\kappa}}|` since this prior matrix is not constant but depends
on the training parameters.




The NaCl likelihoods
--------------------

The full NaCl likelihood looks like this:

.. math::

   \begin{aligned}
   -2 \ln {\cal L} &=  \vec{R}^T_{\vec{\beta}} \vec{V}_{\vec{\theta}\vec{\gamma}}^{-1} \vec{R}_{\vec{\beta}}  + \ln \|\vec{V}_{\vec{\theta}\vec{\gamma}}\|\
   \ \ \ \ \ \ \ \mbox{(residuals and error snake)} \\
                   &+  \mu_{\mathrm{reg}} \vec{\theta}^T \vec{P}_{\mathrm{reg}} \vec{\theta}\ 
   \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \mbox{(regularization)} \\
                   &+  \mu_{\mathrm{cons}}\ \vec{C}(\vec{\theta})^T \vec{C}(\vec{\theta}) 
   \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \mbox{(constraints)} \\
                   &+  \vec{\eta}^T \vec{V^{-1}}_{\mathrm{calib}} \vec{\eta}\
   \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \mbox{(calibration prior)} \\
                   &+  \vec{\kappa}^T \vec{V}^{-1}_{\vec{\kappa}} \vec{\kappa} + \ln\|\vec{V}_{\vec{\kappa}}\|\
   \ \ \ \ \ \ \ \ \ \ \ \ \mbox{(color scatter prior)}
   \end{aligned}

Finding the minimum of this kind of likelihood is a serious minimization
problem.  Since the dimensionality of the model is large, we favor a
second-order method, that uses the local curvature information, to minimize the
numbers of minimization steps.  We therefore need to compute the first and
second derivatives of the likelihood above. 

This expression may look a little intimidating, but it shouldn't actually.
Computing the derivatives of a  SALT2-like model analytically is inexpensive.
To compute the first and second derivatives of the quadratic terms is easy, as
we will see below.  For the derivatives of the :math:`\ln |\vec{X}|`-like terms
we rely on the `classical formula
<https://www.math.uwaterloo.ca/~hwolkowi/matrixcookbook.pdf>`_:

.. math::

    \frac{\partial \ln |\vec{X}|}{\partial x} = \mathrm{Tr}\left(\vec{X}^{-1} \frac{\partial{\vec{X}}}{\partial x}\right)

Finally, for the derivatives of the inverse covariance matrices (and the second
order derivatives of the :math:`\ln |\vec{X}|` terms) we use: 

.. math::
   \frac{\partial \vec{X}^{-1}}{\partial x} = - \vec{X}^{-1} \frac{\partial \vec{X}}{\partial x} \vec{X}^{-1}

Putting everything together, we obtain:

Gradient
--------

To compute the gradient, 

.. math::
   \begin{aligned}
   \partial_{\vec{\beta}} \left(-2\ln {\cal L}\right)  = & -2 \vec{J}^T \vec{V}^{-1} (\vec{Y} - \vec{M})  \\
   & + \mathrm{Tr} \left(\vec{V}^{-1}\partial_{\vec{\beta}} \vec{V}\right)  \\
   & - (\vec{Y} - \vec{M})^T \vec{V}^{-1} \partial_{\vec{\beta}} \vec{V} \vec{V}^{-1} (\vec{Y} - \vec{M})
    \end{aligned}

.. math::
   \begin{aligned}
   \partial_{\vec{\gamma}} \left(-2\ln {\cal L}\right)  = & -(\vec{Y} - \vec{M})^T \vec{V}^{-1} \partial_{\vec{\gamma}}\vec{V} \vec{V}^{-1}  (\vec{Y - \vec{M}}) \\
        & + \mathrm{Tr}\left(\vec{V}^{-1} \partial_{\vec{\gamma}} \vec{V}\right)
   \end{aligned}

.. math::
   \begin{aligned}
   \partial_{\vec{\eta}} \left(-2\ln {\cal L}\right)  = & 
   \end{aligned}

.. math::
   \begin{aligned}
   \partial_{\vec{\kappa}} \left(-2\ln {\cal L}\right)  = & 
   \end{aligned}

.. math::
   \begin{aligned}
   \partial_{\vec{\sigma_{\kappa}}} \left(-2\ln {\cal L}\right)  = & 
   \end{aligned}


Hessian
-------

To compute the hessian, we follow the classical prescription to drop the model
second derivatives. More exactly, we compute :math:`E(\vec{H})`, which allows
us to drop all terms of the form :math:`\vec{A} \vec{X}` with :math:`A` a
matrix and :math:`X` a vector such as :math:`E(\vec{X}) = 0`. After dropping all 
those terms, we get:

.. math::
   \begin{aligned}
   \partial^2_{\vec{\beta}\vec{\beta}} \left(-2\ln {\cal L}\right)  = & +2 \vec{J}^T \vec{V}^{-1} \vec{J} \\
   & - \mathrm{Tr}\left(\vec{V}^{-1}\partial_\beta\vec{V} \vec{V}^{-1} \partial_\beta\vec{V}\right)\\ 
   & + 2 \vec{R}^T \vec{V}^{-1} \partial_\beta \vec{V} \vec{V}^{-1} \partial_\beta \vec{V} \vec{V}^{-1} \vec{R}
   \end{aligned}


.. math::
   \begin{aligned}
   \partial^2_{\vec{\gamma}\vec{\gamma}} \left(-2\ln {\cal L}\right)  = & 
    +2 \vec{R}^T \vec{V}^{-1} \partial_{\vec{\gamma}} \vec{V} \vec{V}^{-1} \partial_{\vec{\gamma}}\vec{V} \vec{V}^{-1} \vec{R} \\
   & + \mathrm{Tr}\left(-\vec{V}^{-1} \partial_{\vec{\gamma}}{\vec{V}}\vec{V}^{-1}\partial_{\vec{\gamma}}\vec{V}\right)
   \end{aligned}

.. math::
   \begin{aligned}
   \partial^2_{\vec{\beta}\vec{\gamma}} \left(-2\ln {\cal L}\right)  = & +2 \vec{J}^T \vec{V}^{-1} \partial_\gamma \vec{V} \vec{V}^{-1} \vec{R} \\
   & + \mathrm{Tr}\left(-\vec{V}^{-1}\partial_\gamma \vec{V} \vec{V}^{-1} \partial_\beta \vec{V}\right) \\
   & + 2 \vec{R}^T \vec{V}^{-1} \partial_\gamma\vec{V} \vec{V}^{-1} \partial_\beta \vec{V} \vec{V}^{-1} \vec{R} 
   \end{aligned}


Minimization
------------

Implementation details
----------------------

Coding Conventions
------------------



