# This CMake file is meant to be executed using 'scikit-build'. Running it
# directly will almost certainly not produce the desired result. If you are a
# user trying to install this package, please use the command below, which will
# install all necessary build dependencies, compile the package in an isolated
# environment, and then install it.
# =====================================================================
# $ pip install .
# =====================================================================
# If you are a software developer, and this is your own package, then it is
# usually much more efficient to install the build dependencies in your
# environment once and use the following command that avoids a costly creation
# of a new virtual environment at every compilation:
# =====================================================================
# $ pip install nanobind ninja scikit-build-core[pyproject]
# $ pip install --no-build-isolation -ve .
# =====================================================================
# You may optionally add -Ceditable.rebuild=true to auto-rebuild when the
# package is imported. Otherwise, you need to re-run the above after editing C++
# files.

cmake_minimum_required(VERSION 3.18)

# The project name is nacl and not sn-nacl so that the extension can be imported
# from Python as "import nacl.sparseutils_ext" instead of "import
# sn_nacl.sparseutils_ext"
set(PROJECT_NAME nacl)
project(${PROJECT_NAME} LANGUAGES CXX C)

# Release build (optimized for speed) by default
if (NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build." FORCE)
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

# Find the required dependencies to build the extension
find_package(Python 3.9 REQUIRED COMPONENTS Interpreter Development.Module ${SKBUILD_SABI_COMPONENT})
find_package(nanobind CONFIG REQUIRED)
find_package(OpenMP COMPONENTS C REQUIRED)

add_library(sparseutils STATIC nacl/sparseutils/src/sparseutils.c)
target_link_libraries(sparseutils PUBLIC OpenMP::OpenMP_C)
set_property(TARGET sparseutils PROPERTY POSITION_INDEPENDENT_CODE ON)

# The nanobind extension wrapping the sparseutils.c code into Python
nanobind_add_module(sparseutils_ext STABLE_ABI NB_STATIC NOMINSIZE LTO nacl/sparseutils/src/sparseutils_ext.cpp)
target_link_libraries(sparseutils_ext PRIVATE sparseutils)
install(TARGETS sparseutils_ext LIBRARY DESTINATION ${PROJECT_NAME})
