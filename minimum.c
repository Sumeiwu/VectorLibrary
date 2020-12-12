#include "mpi.h"      // must have a system with an MPI library
#include <stdio.h>    //printf
#include <stdlib.h>   //malloc

#define MIN(x, y) (((x) < (y)) ? (x) : (y))

void* minimum (double* input1, double* input2, int row, int col)
{
  double* local_a;
  double* local_b;
  double* local_c;

	int size;	 // total nuber of processes
	int rank;        // rank of each process
	int local_n;	// elements per process

  int n = row*col;   // number of array elements
	int i;       // loop index

	MPI_Comm_size (MPI_COMM_WORLD, &size);
	MPI_Comm_rank (MPI_COMM_WORLD,&rank);


	local_n = n/size;
  int scatteredSize = local_n * size;

	local_a = (double *) malloc(sizeof(double)*local_n);
	local_b = (double *) malloc(sizeof(double)*local_n);
	local_c = (double *) malloc(sizeof(double)*local_n);

	MPI_Scatter(input1, local_n, MPI_DOUBLE, local_a, local_n, MPI_DOUBLE, 0, MPI_COMM_WORLD);
	MPI_Scatter(input2, local_n, MPI_DOUBLE, local_b, local_n, MPI_DOUBLE, 0, MPI_COMM_WORLD);

	// operation for getting sum
	for(i=0;i<local_n;i++)    
		local_c[i] = MIN(local_a[i], local_b[i]);

  if (rank ==0 ) {
      for (int i = scatteredSize; i < n; i++ ) {
          input1[i] = MIN(input1[i], input2[i]);
      }
  }

	MPI_Gather(local_c, local_n, MPI_DOUBLE, input1, local_n, MPI_DOUBLE, 0, MPI_COMM_WORLD);

	free(local_a);
  free(local_b);
  free(local_c);

	return input1;
}
