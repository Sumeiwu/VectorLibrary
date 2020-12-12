import ctypes
from ctypes import *

plusLibrary = "./add"

handle = ctypes.cdll.LoadLibrary(plusLibrary)

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


def getCPointer(matrix):
   seq = ctypes.c_double * len(matrix)
   arr = seq(*matrix)

   return arr

def plus(matrix1, matrix2, row, col):
   matrix_pointer1 = getCPointer(matrix1)
   matrix_pointer2 = getCPointer(matrix2)

   handle.plus(matrix_pointer1,matrix_pointer2, row, col)

   #return
   return matrix_pointer1[:]


if __name__== "__main__":
    mpiInit()

    m1 = [1,2,3,4,5,6,7,8]
    m2 = [1,2,3,4,5,6,7,8]

    output = plus(m1, m2, 4, 2)

    if isMaster():
        print(output)

    mpiFinialize()
