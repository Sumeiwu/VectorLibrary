#!bin/sh

scp $1  vx3255:~

ssh vx3255 "sh mpi_copy.sh $1"
