#include "mpi.h"      // must have a system with an MPI library
#include <stdio.h>    //printf
#include <stdlib.h>   //malloc


void MPIInit() {
    MPI_Init(NULL, NULL);
}

int IsMPIMaster() {
    MPI_Comm comm = MPI_COMM_WORLD;
    int rank;
    MPI_Comm_rank(comm, &rank);

    if (rank == 0) {
        return 1;

    }
    return 0;
}

void MPIFinalize() {
    MPI_Finalize();
}


void* diff (double* input1, double* input2, int row, int col)
{

  double* a;
  double* b;
	double* c;
  double* local_a;
  double* local_b;
  double* local_c;


	int size;	 // total nuber of processes
	int rank;        // rank of each process
	int local_n;	// elements per process
  //int row = 4;
  //int col = 2;
  int n = row*col;   // number of array elements
	int i;       // loop index
//  int j;      // loop index

	//MPI_Init (NULL, NULL);
	MPI_Comm_size (MPI_COMM_WORLD, &size);
	MPI_Comm_rank (MPI_COMM_WORLD,&rank);

  if (rank == 0)  {
    a = (double *) malloc(sizeof(double)*n);
    b = (double *) malloc(sizeof(double)*n);
    c = (double *) malloc(sizeof(double)*n);

    for(i=0;i<n;i++)
      a[i] = input1[i];
    for(i=0;i<n;i++)
      b[i] = input2[i];
  }

	local_n = n/size;
  int scatteredSize = local_n * size;

	local_a = (double *) malloc(sizeof(double)*local_n);
	local_b = (double *) malloc(sizeof(double)*local_n);
	local_c = (double *) malloc(sizeof(double)*local_n);

	MPI_Scatter(a, local_n, MPI_DOUBLE, local_a, local_n, MPI_DOUBLE, 0, MPI_COMM_WORLD);
	MPI_Scatter(b, local_n, MPI_DOUBLE, local_b, local_n, MPI_DOUBLE, 0, MPI_COMM_WORLD);

	// operation for getting sum
	for(i=0;i<local_n;i++)
		local_c[i] = local_a[i]-local_b[i];

  if (rank ==0 ) {
      for (int i = scatteredSize; i < n; i++ ) {
          c[i] = a[i]-b[i];
      }
  }

	MPI_Gather(local_c, local_n, MPI_DOUBLE, c, local_n, MPI_DOUBLE, 0, MPI_COMM_WORLD);



/*
	if (rank == 0)  {
		for(i=0;i<n/col;i++) {
      for (j=0;j<col;j++) {
        printf ("%0.0f ", c[i*col+j]);
    }
    printf("\n");
		}
	}
*/


	if (rank == 0)  {
  for(i=0;i<n;i++)
    input1[i] = c[i];
	}

MPI_Bcast(input1, n, MPI_DOUBLE, 0, MPI_COMM_WORLD);

  if (rank == 0)  {
  //for(i=0;i<n;i++)
  //  input1[i] = c[i];
    free(a);
    free(b);
    free(c);
  }
	free(local_a);
  free(local_b);
  free(local_c);


	//MPI_Finalize();

	return input1;
}
