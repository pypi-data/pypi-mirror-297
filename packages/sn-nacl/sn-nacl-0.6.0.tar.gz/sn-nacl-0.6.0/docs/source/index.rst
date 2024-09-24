NaCl: Nouveaux algorithmes de Courbes de lumiere
================================================

   |:warning:|  **This code is still under development and cannot be considered stable** 

The ``NaCl`` package contains code to develop and train type Ia supernova
spectrophotometric models. NaCl can train hybrid models, i.e. models trained
simultaneously on lightcurves, spectral and/or, optionaly, spectrophotometric
data, such as the spectrophotometric sequences published by the SNfactory
collaboration.

As of today, ``NaCl`` contains:
  - a re-implementation of the SALT2 model and error model (Guy et al, 2007,
    2010), with various improvements to make sure that the training can be
    performed in one single minimization 
  - classes to manage a hybrid (light curves + spectra + photometric spectra)
    training sample
  - a minimization framework that is able to minize a log-likelihood function,
    along with quadratic constraints (optional) and quadratic regularization
    penalities (optional).  It is also possible to fit a fairly general error
    model simultaneously.

The code is available on `gitlab <https://gitlab.in2p3.fr/cosmo/sn-nacl>`_.  A
companion paper, documenting the code is available `here
<https://gitlab.in2p3.fr/cosmo/nacl-paper>`_. If you have any question,
regarding the code or its applications, please contact the paper contact
author.

See :doc:`Installation instructions <installation>` and :doc:`quickstart
<quickstart>` for installation instructions and usage overview. The section
:doc:`Examples <examples>` also contains step by step tutorials on how to train
``NaCl`` on real and simulated datasets.

.. toctree::
   :maxdepth: 4
   :caption: Contents:

   installation
   quickstart
   datasets/index
   models/index
   training
   examples

.. toctree::
   :hidden:
   :maxdepth: 4
   :caption: API reference

   code/index

.. toctree::
   :hidden:
   :maxdepth: 3
   :caption: Resources and links

   math
   gitlab repository <https://gitlab.in2p3.fr/cosmo/sn-nacl>
   paper             <https://gitlab.in2p3.fr/cosmo/nacl-paper>


