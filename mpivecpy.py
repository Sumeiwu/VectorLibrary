import scalar_proxy
from scalar_proxy  import add_scalar, divide_scalar

import plus_proxy1
from plus_proxy1 import plus

import diff_proxy1
from diff_proxy1 import diff

import matrixmul_proxy
from matrixmul_proxy import matrix_multiply

import minimum_proxy
import aggregation_proxy 

import math
import numpy as np


def mpiInit():
    scalar_proxy.mpiInit() 

def mpiFinialize():
    scalar_proxy.mpiFinialize()
def isMaster():
    return scalar_proxy.isMaster()

def log(base, vec):
    result = scalar_proxy.log_scalar(vec.matrix, vec.row, vec.col, base)

    return Vec(result, vec.row, vec.col)

def log2(vec):
    return log(2, vec)

def log10(vec):
    return log(10, vec)

def abs(vec):
    result = scalar_proxy.abs_scalar(vec.matrix, vec.row, vec.col)

    return Vec(result, vec.row, vec.col)

def sqrt(vec):
    result = scalar_proxy.sqrt_scalar(vec.matrix, vec.row, vec.col)

    return Vec(result, vec.row, vec.col)

def sum(vec):
    result = aggregation_proxy.sum_aggregate(vec.matrix, vec.row, vec.col)

    return result

def minimum(vec1, vec2):
    result = minimum_proxy.minimum(vec1.matrix, vec2.matrix, vec1.row, vec2.col)

    return Vec(result, vec1.row, vec2.col)

class Vec():

    def __init__(self, matrix, row, col, dim = 2):
        self.matrix = matrix
        self.row = row
        self.col = col
        self.dim = dim 

    def __add__(self, other):
        if isinstance(other, Vec):
            return self._addMatrix(other)
        else:
            return self._addScalar(other)

    def __radd__(self, other):

        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Vec):
            return self._subMatrix(other)
        else:
            return self._subScalar(other)


    def __mul__(self, other):
        if isinstance(other, Vec):
            return self._mulMatrix(other)
        else:
            return self._mulScalar(other)


    def __div__(self, other):
        if isinstance(other, Vec):
            raise Exception("unsupported operation")
        else:
            return self._divideScalar(other)

    def __floordiv__(self, other):
        pass


    def __pow__(self, other):

        res = scalar_proxy.power_scalar(self.matrix, self.row, self.col, other)


        return Vec(res, self.row, self.col) 

    def _subMatrix(self, other):
        res  =  diff(self.matrix, other.matrix, self.row, self.col)

        return Vec(res, self.row, self.col)

    def _addMatrix(self, other):
        res  =  plus(self.matrix, other.matrix, self.row, self.col)

        return Vec(res, self.row, self.col)

    def _mulMatrix(self, other):
        #vec3 = np.arange(9)
        vec3 = []
        res  =  matrix_multiply(self.matrix, other.matrix, vec3, self.row, self.col, other.col)

        return Vec(res, self.row, self.col)

    def _addScalar(self, other):
        
        res  =  add_scalar(self.matrix, self.row, self.col, other)

        return Vec(res, self.row, self.col)
        #return res

    def _divideScalar(self, other):
        res  =  divide_scalar(self.matrix, self.row, self.col, other)

        return Vec(res, self.row, self.col)


    def __setitem__(self, left, right):
        if isinstance(left, tuple):
            rowIndex, t = left

            if isinstance(rowIndex, int) and isinstance(t, slice):
                indices = range(*t.indices(self.col))
                for i in indices:
                    self.matrix[rowIndex * self.col + i] = right.matrix[i]
            else:
                raise Exception("unsupported index")
        else:
            raise Exception("unsupported index")

    def __getitem__(self, index):

        if isinstance(index, tuple):
            r, c = index
            if isinstance(r, int) and isinstance(c, int):
                return self.matrix[r * self.col + c]
            elif isinstance(r, int) and isinstance(c, slice):
                indices = range(*c.indices(self.col))
                newl =   [self.matrix[r * self.col + i] for i in indices]
                return Vec(newl, len(newl), 1)
            else:
                raise Exception("unsupported index")

        else:
            raise Exception("unsupported index")


    def __repr__(self):
        return self.matrix

