
import ctypes
from ctypes import *

scalarLibrary = "./scalar"

handle = ctypes.cdll.LoadLibrary(scalarLibrary)

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

def multiply_scalar(matrix, row, col, ele):
    matrix_pointer = getCPointer(matrix)

    handle.multiply_scalar(matrix_pointer, row, col, ele)

    return matrix_pointer[:]

def divide_scalar(matrix, row, col, ele):
    matrix_pointer = getCPointer(matrix)

    handle.divide_scalar(matrix_pointer, row, col, ele)
     
    return matrix_pointer[:]

## todo debug here 
def add_scalar(matrix, row, col, ele):
    matrix_pointer = getCPointer(matrix)
    #DoublePointer = POINTER(c_double)
    #b = DoublePointer.from_buffer(matrix_pointer)
    #ctypes.cast(matrix_pointer, ctypes.POINTER(ctypes.c_double))
    func = handle.add_scalar
    ele = int(ele)


    func.restype = POINTER(c_double)
    handle.add_scalar(matrix_pointer, row, col, ele) 

    return matrix_pointer[:]

def abs_scalar(matrix, row, col):
    
    matrix_pointer = getCPointer(matrix)

    handle.abs_scalar(matrix_pointer, row, col) 
    
    return matrix_pointer[:]

def log_scalar(matrix, row, col, base):
    
    matrix_pointer = getCPointer(matrix)

    handle.log_scalar(matrix_pointer, row, col, base) 
    
    return matrix_pointer[:]

def sqrt_scalar(matrix, row, col):
    
    matrix_pointer = getCPointer(matrix)

    handle.sqrt_scalar(matrix_pointer, row, col) 
    
    return matrix_pointer[:]

def power_scalar(matrix, row, col, powerNum):
    
    matrix_pointer = getCPointer(matrix)

    handle.power_scalar(matrix_pointer, row, col, powerNum) 
    
    return matrix_pointer[:]
   

if __name__== "__main__":
    mpiInit()

    m = [1,2,3,4,5,6,7,8]

    output = add_scalar(m, 4, 2, 10)

    output = add_scalar(output, 4, 2, 100)

    if isMaster():
        print(output)

    mpiFinialize()