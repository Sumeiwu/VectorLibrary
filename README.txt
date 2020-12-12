
1. A quick demo 

import mpivecpy 
from mpivecpy import Vec, mpiInit, isMaster, mpiFinialize 

mpiInit() ## required to declare before a program
x  = Vec([1,2,3,4], 2,2)
y  = Vec([4,5,6,7], 2,2)

x = x + 100 
x = x + y
y = x * y

sum_x = mpivecpy.sum( (x - y) ** 2) 

if isMaster():  ## the result is only delivered to master process currently 
    print(sum_x)

mpiFinialize() ## required to declare after a program 

2. required environments
A cluster with MPI installed and python installed, better on linux OS

3. how to compile and test 
To compile: sh run.sh compile
To run test: sh run.sh test 

4. major code files description
mpivecpy.py : library entrance 
testVector.py: this is for library unit test 



