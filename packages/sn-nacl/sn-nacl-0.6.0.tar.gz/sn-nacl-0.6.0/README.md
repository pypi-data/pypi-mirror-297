# NaCl

[![PyPI - Version](https://img.shields.io/pypi/v/sn-nacl.svg)](https://pypi.org/project/sn-nacl)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sn-nacl.svg)](https://pypi.org/project/sn-nacl)
![coverage](https://gitlab.in2p3.fr/lemaitre/sn-nacl/badges/master/coverage.svg)


> **:warning: This code is still under development and cannot be considered stable**

The `NaCl` package contains code to develop and train type Ia supernova
spectrophotometric models. NaCl can train hybrid models, i.e. models trained
simultaneously on lightcurves, spectral and/or, optionaly, spectrophotometric
data, such as the spectrophotometric sequences published by the SNfactory
collaboration.

As of today, `NaCl` contains:

- a re-implementation of the SALT2 model and error model (Guy et al, 2007,
  2010), with various improvements to make sure that the training can be
  performed in one single minimization

- classes to manage a hybrid (light curves + spectra + photometric spectra)
  training sample

- a minimization framework that is able to minize a log-likelihood function,
  along with quadratic constraints (optional) and quadratic regularization
  penalities (optional). It is also possible to fit a fairly general error model
  simultaneously.


**Table of Contents**

- [Installation](#installation)
- [Getting started](#getting started)
- [Troubleshooting](#troubleshooting)
- [License](#license)


# Installation

## virtual environments

We recommend using `conda` which comes with a compiled version of `suitesparse`.
`venv` is also a suitable option if suitesparse is already installed on your
machine, or if you are ready to compile it yourself (on Debian/Unbuntu, just
have a `sudo apt install libsuitesparse-dev`).

As a reminder:

```bash
conda create -n MY_ENV
conda activate MY_ENV
```

or:

```bash
python -m venv MY_ENV
source MY_ENV/bin/activate
```

## Prerequisites

conda packages for `sn-nacl` are in preparation (but not ready yet). If you are
working within a conda environnment, we recommend that you install these conda
packages first:

```bash
conda install ipython numpy scipy matplotlib scikit-sparse pandas h5py pyarrow
```

The `mkl` library can enhance training speed. While it is not a requirement, we
recommend installing it if you are using an Intel platform:

```bash
conda install mkl sparse_dot_mkl
```

Until our changes are merged in sncosmo, we use a modified version of it:

```bash
git clone https://github.com/nregnault/sncosmo.git
cd sncosmo
pip install .
```

Finally, `cmake` and a C++ compiler with OpenMP support are also required to build a
Python extension. On Linux, `gcc` supports OpenMP out of the box. On macos an
installation is required:

```bash
# for linux
conda install cmake
# for macos
conda install cmake openmp
```

## Installing NaCl

``` bash
pip install sn-nacl
```

or, if you prefer installing it from sources:

```bash
git clone https://gitlab.in2p3.fr/lemaitre/sn-nacl
cd sn-nacl
pip install -e .
```

If your you are a developper and want to work on the `sn-nacl` package:

```bash
pip install nanobind ninja scikit-build-core[pyproject]
pip install --no-build-isolation -Ceditable.rebuild=true -ve .
```


## Running the tests

```bash
pip install .[test]
pytest
```

## Building the documentation

```bash
pip install -e .[doc]
cd docs
make html  # for example, type "make" for a list of targets
```

Then the documenation is available at `docs/build/html/index.html`

# Getting started

TBD

# Troubleshooting

## Dealing with scikit-sparse

`NaCl` depends on the python bindings to the `cholmod` package, distributed with
the `scikit-sparse` package. In most cases, `scikit-sparse` will be fetched
automatically and installed without any problem. However, depending on your
version of python the installation may crash for various reasons:

- The package needs numpy to be installed already (and doesn't fetch it
  automatically if missing).

- The packages needs `cython` : `pip install cython` should solve the problem.

- Finally, `libsuitesparse` should also be available on your system. On a debian
  or ubuntu system: `sudo apt-get install libsuitesparse-dev` should suffice. On
  Fedora/CentOS the equivalent is `sudo yum install libsuitesparse-devel`.
  Otherwise, an alternative is to to the [SuiteSparse
  repository](https://github.com/DrTimothyAldenDavis/SuiteSparse), clone it and
  follow the installation instructions.

- Also, for `python>=3.10`, the pip installation of scikit-sparse may complain
  about various things and stops. If you encounter this kind of problem, this
  longer install sequence should work:

  ```bash
  pip install numpy
  git clone https://github.com/scikit-sparse/scikit-sparse.git
  cd scikit-sparse; python setup.py install; cd ..
  pip install sn-nacl
  ```

# License

`sn-nacl` is distributed under the terms of the
[MIT](https://spdx.org/licenses/MIT.html) license.
