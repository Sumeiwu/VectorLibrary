

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <mpi.h>

double sum(void* input, int row, int col){
    
    double* a = input; 

    MPI_Comm comm = MPI_COMM_WORLD; 

    double global = 0 ; 
    int comm_sz;
    int my_rank;
    MPI_Comm_size(comm, &comm_sz);
    MPI_Comm_rank(comm, &my_rank);


    int n = row * col; 
    int local_n = n / comm_sz;

    int scatteredSize = local_n * comm_sz; 
  
    double* local_a = malloc(local_n *  sizeof(double));
    

    MPI_Scatter(a, local_n, MPI_DOUBLE, local_a, local_n, MPI_DOUBLE, 0, comm);
    double localSum = 0; 
    for (int i = 0; i < local_n; i++) {
        localSum += local_a[i];
    }

    MPI_Reduce(&localSum, &global, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);


    // deal with remainder part 
    if (my_rank ==0 ) {
        for (int i = scatteredSize; i < n; i++ ) {
            global += a[i];
        }
    }
    free(local_a);

    return global; 
}

int main(void) {
    int comm_sz; /* Number of processes */
    int my_rank; /* My process rank */
    MPI_Init(NULL, NULL);
    MPI_Comm_size(MPI_COMM_WORLD, &comm_sz);
    MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);

    double d[6] = {6,5,4,3,2,1};
    
    // todo debug here 
    double global  = sum(d, 3, 2);  

    if (my_rank == 0) {
        printf("the final result is %lf\n", global);
    }

    MPI_Finalize();
}