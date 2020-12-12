#!bin/sh

compile() {
    echo "Start Compile"
    mpicc -fPIC -shared -g -Wall -o scalar scalar.c
    mpicc -fPIC -shared -g -Wall -o add add.c
    mpicc -fPIC -shared -g -Wall -o diff diff.c
    mpicc -fPIC -shared -g -Wall -o matrixmul matrixmul.c
    mpicc -fPIC -shared -g -Wall -o aggregation aggregation.c
    mpicc -fPIC -shared -g -Wall -o minimum minimum.c
    echo "Compiling Success"
}

test() {
    echo "Start Test"
    mpirun -np 2 python testVector.py
    echo "End of Testing"
}

command=$1

if [ $command = "compile" ]
then
    compile
elif [ $command = "test" ]
then 
    compile
    test
else
    echo "please input command: sh run.sh compile or sh run.sh test"
fi







