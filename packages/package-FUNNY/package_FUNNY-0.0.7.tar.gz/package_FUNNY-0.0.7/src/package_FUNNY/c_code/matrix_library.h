// matrix_library.h
#ifndef MATRIX_LIBRARY_H
#define MATRIX_LIBRARY_H

double* matrix_multiply(double *A, double *B, double *C, int m, int n, int p);
double* matrix_transpose(double *A, double *B, int m, int n);
double* matrix_add(double *A, double *B, double *C, int m, int n);

#endif