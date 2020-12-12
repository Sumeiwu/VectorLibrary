#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <mpi.h>
#include <time.h>

void MPIInit() {
    MPI_Init(NULL, NULL);
}

int IsMPIMaster() {
    MPI_Comm comm = MPI_COMM_WORLD;
    int my_rank;
    MPI_Comm_rank(comm, &my_rank);

    if (my_rank == 0) {
        return 1;

    }
    return 0;
}

void MPIFinalize() {
    MPI_Finalize();
}

void* multiply(double* matrix_a, double* matrix_b, double* matrix_c, int m, int n, int q){

    MPI_Comm comm = MPI_COMM_WORLD;

    int com_size;
    int id;
    double *local_a, *local_c;
    int local_m;
    MPI_Comm_size(comm, &com_size);
    MPI_Comm_rank(comm, &id);

   // MPI_Bcast(&m, 1, MPI_INT, 0, comm);
   // MPI_Bcast(&n, 1, MPI_INT, 0, comm);
   // MPI_Bcast(&q, 1, MPI_INT, 0, comm);

    //local_m = numbers of rows each process gonna calculate
    local_m = m/com_size;
    local_a = (double*)malloc(sizeof(double)*local_m*n);
    int scatteredSize = local_m * com_size;

    MPI_Scatter(matrix_a, local_m*n, MPI_DOUBLE, local_a, local_m*n, MPI_DOUBLE, 0, comm);
   // MPI_Bcast(matrix_b, n*q, MPI_DOUBLE, 0, comm);

    //calculate matrix_c
    local_c = (double*)malloc(sizeof(double)*local_m*q);

    for(int i = 0; i < local_m; i++){
        for(int j = 0; j < q; j++){
            local_c[i*q+j] = 0;
            for(int k = 0; k < n; k++){
                local_c[i*q+j] += local_a[i*n+k] * matrix_b[k*q+j];
            }
        }
    }

    MPI_Gather(local_c, local_m*q, MPI_DOUBLE, matrix_c, local_m*q, MPI_DOUBLE, 0, comm);

    if (id == 0){
        //if the m can't be divisible by the number of processes
        //then it will be calculated in process 0
        int rem = m%com_size;
        if(rem != 0){
            for (int i = scatteredSize; i < m; i++){
                for(int j = 0; j < q; j++){
                    matrix_c[i*q+j] = 0;
                    for(int k = 0; k < n; k++){
                        matrix_c[i*q+j] += matrix_a[i*n+k] * matrix_b[k*q+j];
                    }
                }

            }
        }
    }

    free(local_a);
    free(local_c);

    return matrix_c;
}

void* matrix_multiply(double* matrix_a, double* matrix_b, double* matrix_c, int m, int n, int q) {
    multiply(matrix_a, matrix_b, matrix_c, m, n, q);

    return matrix_c;
}
