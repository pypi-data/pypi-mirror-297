#ifndef _SPARSEUTILS_H
#define _SPARSEUTILS_H

int kron_product_by_line(
   int n, int na, int nb, int k_max,
   int* A_indices, int* A_indptr, double* A_data,
   double* B_data,
   int * i_triplets, int * j_triplets, double * val_triplets);


// int append(
//    int input_size, int offset,
//    long int * row, long int * col, double * val,
//    long int * row_buff, long int * col_buff, double * val_buff,
//    int check_free_pars);


#endif
