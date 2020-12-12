
import ctypes
from ctypes import *

aggregationLibrary = "./aggregation"

handle = ctypes.cdll.LoadLibrary(aggregationLibrary)

def getCPointer(matrix):
   seq = ctypes.c_double * len(matrix)
   arr = seq(*matrix)

   return arr 

def sum_aggregate(matrix, row, col):
    matrix_pointer = getCPointer(matrix)
    func = handle.sum
    func.restype = ctypes.c_double

    result = handle.sum(matrix_pointer, row, col)

    return result

   
