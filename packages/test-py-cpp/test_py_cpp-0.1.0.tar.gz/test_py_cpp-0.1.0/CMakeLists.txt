cmake_minimum_required(VERSION 3.15...3.29)

project(_core LANGUAGES CXX)

set(PYBIND11_FINDPYTHON ON)
find_package(pybind11 CONFIG REQUIRED)

include_directories("/boost/boost_1_86_0")

pybind11_add_module(_core src/main.cpp)

install(TARGETS _core DESTINATION test_py_cpp)