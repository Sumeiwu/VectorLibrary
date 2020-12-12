import ctypes
from ctypes import *

plusLibrary = "./minimum"

handle = ctypes.cdll.LoadLibrary(plusLibrary)

def getCPointer(matrix):
   seq = ctypes.c_double * len(matrix)
   arr = seq(*matrix)

   return arr

def minimum(matrix1, matrix2, row, col):
   matrix_pointer1 = getCPointer(matrix1)
   matrix_pointer2 = getCPointer(matrix2)

   handle.minimum(matrix_pointer1,matrix_pointer2, row, col)

   #return
   return matrix_pointer1[:]