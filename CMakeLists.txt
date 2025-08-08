cmake_minimum_required(VERSION 3.20)
project(lanelet2_python_api_for_autoware)

# Find scikit-build's PythonExtensions
find_package(PythonExtensions REQUIRED)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add subdirectory for the Python module
add_subdirectory(lanelet2_python)