Installation
============

Installing NaCl with conda
--------------------------

This is currently the recommended method. NaCl depends on the `cholmod
<https://scikit-sparse.readthedocs.io/en/latest/cholmod.html>`_ library, a
component of `suitesparse
<https://people.engr.tamu.edu/davis/suitesparse.html>`_, which may be missing
on some platforms. conda provides compiled packages for suitesparse and
cholmod, which may greatly simplify the installation process. Another
(optional, but potentially very useful dependency) is the `sparse_dot_mkl
<https://pypi.org/project/sparse-dot-mkl/>`_ package, a component of the Intel
`mkl <https://anaconda.org/intel/mkl>`_ library. Both may be obtained from
conda.

In it recommended to create a specific conda environment::

   $ conda create -n nacl python 
   $ conda activate nacl

Some packages actually come from conda-forge::

   $ conda config --add channels conda-forge
   $ conda config --set channel_priority strict

Install the pre-requisites::

   $ conda install numpy scipy mkl sparse_dot_mkl

and install NaCl::

   $ # sn-nacl will soon be available as a conda package
   $ # conda install sn-nacl
   $ pip install sn-nacl

Install from PyPI
-----------------

``NaCl`` can be installed from PyPI, either from within a virtual environment::

   $ python3 -m venv nacl
   $ source nacl/bin/activate
   $ pip install sn-nacl

or from a conda environment::

   $ conda activate nacl
   $ pip install sn-nacl

Install from source code
------------------------

At this stage of development, the best option is to clone the 
``NaCl`` repository and install from source::

   $ git clone https://gitlab.in2p3.fr/cosmo/sn-nacl
   $ cd sn-nacl 
   $ pip install -r requirements.txt

To install the NaCl code::

   $ pip install . 

If you intend to hack the code, and avoid re-installing each time you modify a file::

   $ pip install -e . 


Building the documentation
--------------------------





Dealing with `scikit-sparse <https://github.com/scikit-sparse/scikit-sparse>`_  
------------------------------------------------------------------------------

``NaCl`` depends on the cholmod package, available from the `scikit-sparse
<https://github.com/scikit-sparse/scikit-sparse>`_  package. In most cases,
``scikits-sparse`` will be fetched automatically and installed without any
trouble by the installer. In some cases, depending on your version of python,
the installation may crash for various reasons:

  - ``scikit-sparse`` assumes that ``numpy`` is installed already and cannot
    fetch it automatically if missing. :code:`pip install numpy` should solve
    the problem.

  - ``scikit-sparse`` needs ``cython`` and does not know how to get it.
    :code:`pip install cython` should solve the problem. 

  - `libsuitesparse <https://github.com/ethz-asl/suitesparse>`_ should also be
    available on your system.  This is the library which contains the core of
    the ``cholmod`` routines.  If you are using conda, or miniconda,
    ``libsuitesparse`` should be fetched automagically. On a debian or ubuntu
    system: :code:`sudo apt-get install libsuitesparse-dev` should suffice. On
    Fedora/CentOS the equivalent is :code:`sudo yum install
    libsuitesparse-devel`. Otherwise, an alternative is to to the `SuiteSparse
    repository <https://github.com/DrTimothyAldenDavis/SuiteSparse>`_, clone it
    and follow the installation instructions.

  - finally, for python>=3.10, the ``pip`` installation of ``scikit-sparse``
    may complain about various things and stop. If you encounter this, this longer
    install sequence should work::

    $ pip install numpy
    $ git clone https://github.com/scikit-sparse/scikit-sparse.git
    $ cd scikit-sparse; python setup.py install; cd ..
    $ pip install sn-nacl


Installing metadata
-------------------

TBW: not yet, because it will change soon.

