import ctypes
from ctypes import *

matrixmulLibrary = "./matrixmul"

handle = ctypes.cdll.LoadLibrary(matrixmulLibrary)

def mpiInit():
    handle.MPIInit()

## check whether it is master , because we only get result from the master
def isMaster():
    func = handle.IsMPIMaster
    func.restype = ctypes.c_int

    result = func()

    return result == 1

def mpiFinialize():
    handle.MPIFinalize()

def getCPointer(matrix, row, col):
   seq = ctypes.c_double * (row*col)
   arr = seq(*matrix)

   return arr

def matrix_multiply(matrix1, matrix2, matrix3, m, n, q):
    matrix_a = getCPointer(matrix1, m, n)
    matrix_b = getCPointer(matrix2, n, q)
    matrix_c = getCPointer(matrix3, m, q)
    handle.multiply(matrix_a, matrix_b, matrix_c, m, n, q)

    return matrix_c[:]
    

if __name__== "__main__":
    mpiInit()

    m1 = [1,2,3]
    m2 = [4,5,6]
    m3 = []
    output = matrix_multiply(m1, m2, m3, 3, 1, 3)
    
    if isMaster():
        print(output)

    mpiFinialize()
