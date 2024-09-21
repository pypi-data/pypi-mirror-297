#include "matrix_library.h"

// n deve essere uguale per garantire la moltiplicazione
double*  matrix_multiply(double *A, double *B, double *C, int m, int n, int p){
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < p; j++) {
            C[i * p + j] = 0;
            for (int k = 0; k < n; k++) {
                C[i * p + j] += A[i * n + k] * B[k * p + j];
            }
        }
    }
    return C;
    //resistuisco l'indirizzo a cui punta C
    //Se mettessi l'asterisco, cioè return *C;, significherebbe che stai cercando
    //di restituire il valore a cui punta C (un singolo double
}

double* matrix_transpose(double *A, double *B, int m, int n){
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            B[j * m + i] = A[i * n + j];
        }
    }
    return B;
}

double*  matrix_add(double *A, double *B, double *C, int m, int n){
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            C[i * n + j] = A[i * n + j] + B[i * n + j];
        }
    }
    return C;
}