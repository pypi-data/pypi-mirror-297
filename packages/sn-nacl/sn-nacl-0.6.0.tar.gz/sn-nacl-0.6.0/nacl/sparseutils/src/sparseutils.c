#include <math.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <omp.h>


int kron_product_by_line(
   int n, int na, int nb, int k_max,
   int* A_indices, int* A_indptr, double* A_data,
   double* B_data,
   int * i_triplets, int * j_triplets, double * val_triplets)
{
   const int num_threads = omp_get_max_threads();
   int *local_i_triplets[num_threads];
   int *local_j_triplets[num_threads];
   double *local_val_triplets[num_threads];
   int local_c[num_threads];

   #pragma omp parallel \
      shared(local_i_triplets, local_j_triplets, local_val_triplets, local_c) \
      num_threads(num_threads)
   {
      int tid = omp_get_thread_num();
      local_i_triplets[tid] = (int *)malloc(n * nb * k_max * sizeof(int));
      local_j_triplets[tid] = (int *)malloc(n * nb * k_max * sizeof(int));
      local_val_triplets[tid] = (double *)malloc(n * nb * k_max * sizeof(double));
      local_c[tid] = 0;

      #pragma omp for
      // for each row i
      for(int i = 0; i < n; i++)
      {
         // for each non-zero value in A[i, :]
         for(int k = A_indptr[i]; k < A_indptr[i + 1]; k++)
         {
            // computing A[i, j] * B[i, :]
            const int j = A_indices[k];
            for(int l = 0; l < nb; l++)
            {
               const int m = i * nb + l;
               if(B_data[m] == 0.)
                  continue;

               local_i_triplets[tid][local_c[tid]] = i;
               local_j_triplets[tid][local_c[tid]] = j * nb + l;
               local_val_triplets[tid][local_c[tid]] = B_data[m] * A_data[k];
               local_c[tid]++;
            }
         }
      }
   }

   // Combine the local arrays into the global arrays
   int c = 0;
   for(int t = 0; t < num_threads; t++)
   {
      memcpy(&i_triplets[c], local_i_triplets[t], local_c[t] * sizeof(int));
      memcpy(&j_triplets[c], local_j_triplets[t], local_c[t] * sizeof(int));
      memcpy(&val_triplets[c], local_val_triplets[t], local_c[t] * sizeof(double));

      c += local_c[t];

      free(local_i_triplets[t]);
      free(local_j_triplets[t]);
      free(local_val_triplets[t]);
   }

   return c;
}


/* int append(int input_size, int offset,
              long int * row, long int * col, double * val,
              long int * row_buff, long int * col_buff, double * val_buff,
              int check_free_pars)
   {
      int i;
      int c = 0;
      for(i=0; i<input_size; i++)
      {
         if((col[i]<0) & (check_free_pars>0))
            continue;
         row_buff[offset+c] = row[i];
         col_buff[offset+c] = col[i];
         val_buff[offset+c] = val[i];
         c++;
      }
      return c;
   } */
