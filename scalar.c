
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h> 
#include <math.h>
#include <mpi.h>
#include <math.h>


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

double multiply(double a, double e) {
    return a * e; 
}
double plus(double a, double e) {
    return a + e; 
}

double divide(double a, double divider) {
    return (a+ 0.0) / divider; 
}

double _abs(double a) {
    return fabs(a);
}

double _log(double a, double base) {
    return log(a) / log(base);
}

double _sqrt(double a) {
    return sqrt(a); 
}

double _power(double a,  double powerNum ) {
    return pow(a, powerNum);
}

void* scalar_func(void* input, int row, int col, int ele, 
    double (*func1)(double, double), double (*func2)(double) ){
    
    double* a = input; 

    MPI_Comm comm = MPI_COMM_WORLD; 

    int comm_sz;
    int my_rank;
    // MPI_Init(NULL, NULL);
    MPI_Comm_size(comm, &comm_sz);
    MPI_Comm_rank(comm, &my_rank);

    // double* output;
    // if (my_rank == 0) {
    //     output = malloc(n * sizeof(double));
    // }

    int n = row * col; 
    int local_n = n / comm_sz;

    // printf("comm_size is %d, local_n is %d my_rank is %d \n",comm_sz, local_n, my_rank);


    int scatteredSize = local_n * comm_sz; 
  
    double* local_a = malloc(local_n *  sizeof(double));
    

    MPI_Scatter(a, local_n, MPI_DOUBLE, local_a, local_n, MPI_DOUBLE, 0, comm);

    for (int i = 0; i < local_n; i++) {
        if (func1 != NULL) {
            local_a[i] =(*func1)(local_a[i], ele);
        }else {
            local_a[i] = (*func2)(local_a[i]);
        }
    }

    // deal with remainder part 
    if (my_rank ==0 ) {
        for (int i = scatteredSize; i < n; i++ ) {
            if (func1 != NULL) {
                a[i] =(*func1)(a[i], ele);
            }else {
                a[i] =(*func2)(a[i]);
            }
        }
    }

    MPI_Gather(local_a, local_n, MPI_DOUBLE, a, local_n, MPI_DOUBLE, 0, comm);

    // if (my_rank == 0) {
    //     for (int i = 0; i < n; i ++) {
    //         printf("%f ", a[i]);
    //     }
    //     printf("\n");
    // }

    free(local_a);
    
    // MPI_Finalize();
    return a; 
}

void* scalar_func1(void* input, int row, int col, int ele, 
    double (*func1)(double, double)) {

    return scalar_func(input, row, col, ele, func1, NULL);
}

void* scalar_func2(void* input, int row, int col, 
    double (*func2)(double)) {

    return scalar_func(input, row, col, 0, NULL, func2);
}

void* multiply_scalar(void* input, int row, int col, int multiplier) {
    scalar_func1(input, row, col, multiplier, &multiply);

    return input;
}


void* add_scalar(void* input, int row, int col, int ele) {
    scalar_func1(input, row, col, ele, &plus);

    return input;
}

void* divide_scalar(void* input, int row, int col, int ele) {
    scalar_func1(input, row, col, ele, &divide);

    return input;
}

void* sqrt_scalar(void* input, int row, int col) {
    scalar_func2(input, row, col, &_sqrt);

    return input;
}

void* abs_scalar(void* input, int row, int col) {
    scalar_func2(input, row, col, &_abs);

    return input;
}

void* log_scalar(void* input, int row, int col, int base) {
    scalar_func1(input, row, col, base, &_log);

    return input;
}

void* power_scalar(void* input, int row, int col, int powerNum) {
    scalar_func1(input, row, col, powerNum, &_power);

    return input;
}
