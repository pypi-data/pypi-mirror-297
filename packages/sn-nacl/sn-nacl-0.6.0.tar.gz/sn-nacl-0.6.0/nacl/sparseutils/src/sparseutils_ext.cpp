#include <nanobind/nanobind.h>
#include <nanobind/ndarray.h>

extern "C"
{
   #include "sparseutils.h"
}


namespace nb = nanobind;

using namespace nb::literals;


int kron_product_by_line_ext(
   int n, int na, int nb, int k_max,
   const nb::ndarray<nb::numpy, int, nb::shape<-1>>& A_indices,
   const nb::ndarray<nb::numpy, int, nb::shape<-1>>& A_indptr,
   const nb::ndarray<nb::numpy, double, nb::shape<-1>>& A_data,
   const nb::ndarray<nb::numpy, double, nb::shape<-1, -1>>& B,
   nb::ndarray<nb::numpy, int, nb::shape<-1>>& i,
   nb::ndarray<nb::numpy, int, nb::shape<-1>>& j,
   nb::ndarray<nb::numpy, double, nb::shape<-1>>& val)
{
   return kron_product_by_line(
      n, na, nb, k_max,
      A_indices.data(), A_indptr.data(), A_data.data(),
      B.data(),
      i.data(), j.data(), val.data());
}


NB_MODULE(sparseutils_ext, m)
{
   m.doc() = "Wrappers to C implementation of sparseutils";

   m.def(
      "_kron_product_by_line", kron_product_by_line_ext,
      "n"_a, "na"_a, "nb"_a, "k_max"_a,
      "A_indices"_a, "A_indptr"_a, "A_data"_a,
      "B_data"_a,
      "i"_a, "j"_a, "val"_a);
}
