"""Utility functions and classes for sparse matrices"""

import logging
import os
import ctypes

import numpy as np
import scipy

from nacl.sparseutils_ext import _kron_product_by_line


def kron_product_by_line(a, b):
    r"""A line-wise Kronecker product of two matrices

    Parameters
    ----------
    a : (k, n) sparse matrix
        first matrix of the product, must be sparse preferably in CSR format.
        The matrix is converted to CSR format if needed.
    b : (k, m) dense matrix
        second matrix of the product

    Returns
    -------
    c : (k, m*n) sparse matrix in COO format
        Line-wise Kronecker product of `a` and `b`

    Examples
    --------
    >>> import numpy as np
    >>> import scipy as sp
    >>> from nacl.sparseutils import kron_product_by_line
    >>> a = sp.sparse.csr_matrix(np.array([[0, 2], [5, 0]]))
    >>> b = np.array([[1, 2], [3, 4]])
    >>> kron_product_by_line(a, b).toarray()
    array([[ 0.,  0.,  2.,  4.],
           [15., 20.,  0.,  0.]])

    """
    if not (a.ndim == 2 and b.ndim == 2):
        raise ValueError("The both arrays should be 2-dimensional.")

    if not a.shape[0] == b.shape[0]:
        raise ValueError(
            "The number of rows for both arrays should be equal.")

    if not scipy.sparse.issparse(a):
        raise ValueError("`a` must be a sparse array.")

    if scipy.sparse.issparse(b):
        raise ValueError("`b` must be a dense array.")

    a = a.tocsr()

    # estimate the number of non-zero triplets in result
    non_zeros = a.indptr[1:] - a.indptr[:-1]
    estimated_result_size = (non_zeros * b.shape[1]).sum()

    rows = np.zeros(estimated_result_size, dtype=np.int32)
    cols = np.zeros(estimated_result_size, dtype=np.int32)
    vals = np.zeros(estimated_result_size, dtype=np.float64)

    n = _kron_product_by_line(
        a.shape[0], a.shape[1], b.shape[1], non_zeros.max(),
        a.indices, a.indptr, a.data,
        b,
        rows, cols, vals)

    return scipy.sparse.coo_matrix(
        (vals[:n], (rows[:n], cols[:n])),
        shape=(a.shape[0], a.shape[1] * b.shape[1]))


class CooMatrixBuff:
    def __init__(self, shape, estimated_nnz, increment=1.3):
        self.shape = shape
        self.size = estimated_nnz
        self.increment = increment
        self.i = np.zeros(self.size).astype(np.int64)
        self.j = np.zeros(self.size).astype(np.int64)
        self.val = np.zeros(self.size)
        self.ptr = 0

    def _resize(self):
        logging.warning(
            'need to resize CooMatrixBuff: revise your estimates of non-zero terms !')
        new_size = self.size * self.increment
        self.i = np.resize(self.i, new_size)
        self.j = np.resize(self.j, new_size)
        self.val = np.resize(self.val, new_size)
        self.i[self.ptr:] = 0
        self.j[self.ptr:] = 0
        self.val[self.ptr:] = 0.
        self.size = new_size

    def append(self, i, j, val, free_pars_only=False):
        """
        """
        logging.info(f'appending {len(i)} to buffer at location {self.ptr}')
        sz = len(i)
        assert (len(j) == sz) and (len(val) == sz)

        if (self.ptr + sz) > self.size:
            self._resize()

        # if free_pars_only:
        #     sz = lib.append(
        #         len(i), self.ptr,
        #         i.astype(np.int64), j.astype(np.int64), val,
        #         self.i, self.j, self.val,
        #         1)
        #     self.ptr += sz
        # else:
        #     sz = lib.append(
        #         len(i), self.ptr,
        #         i.astype(np.int64), j.astype(np.int64), val,
        #         self.i, self.j, self.val,
        #         0)
        #     self.ptr += sz

        if free_pars_only:
            idx = j >= 0
            sz = idx.sum()
            self.i[self.ptr:self.ptr+sz] = i[idx]
            self.j[self.ptr:self.ptr+sz] = j[idx]
            self.val[self.ptr:self.ptr+sz] = val[idx]
            self.ptr += sz
        else:
            self.i[self.ptr:self.ptr+sz] = i
            self.j[self.ptr:self.ptr+sz] = j
            self.val[self.ptr:self.ptr+sz] = val
            self.ptr += sz
        logging.info('done')

    def tocoo(self):
        return scipy.sparse.coo_matrix(
            (self.val[:self.ptr], (self.i[:self.ptr], self.j[:self.ptr])),
            self.shape)


class CooMatrixBuff2:
    def __init__(self, shape, increment=1.3):
        self.shape = shape
        self.increment = increment
        self._row = []
        self._col = []
        self._data = []
        self._idx = []

    def append(self, i, j, val):
        """
        """
        self._row.append(i)
        self._col.append(j)
        self._data.append(val)
        self._idx.append(j>=0)

    def tocoo(self):
        idx = np.hstack(self._idx)
        r = scipy.sparse.coo_matrix(
            (np.hstack(self._data)[idx],
             (np.hstack(self._row)[idx], np.hstack(self._col)[idx])),
            self.shape)
        return r

    @property
    def row(self):
        return self._row

    @property
    def col(self):
        return self._col

    @property
    def data(self):
        return self._data
