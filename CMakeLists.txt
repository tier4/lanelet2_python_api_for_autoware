cmake_minimum_required(VERSION 3.10)
project(lanelet2_python_api_for_autoware)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Set installation prefix for dependencies if not set
if(NOT CMAKE_INSTALL_PREFIX OR CMAKE_INSTALL_PREFIX STREQUAL "/usr/local")
    set(CMAKE_INSTALL_PREFIX ${CMAKE_CURRENT_SOURCE_DIR}/install)
endif()

# Set install directory for dependencies
set(LANELET2_INSTALL_DIR ${CMAKE_CURRENT_SOURCE_DIR}/install)

# Ensure dependencies are built first
message(STATUS "Building dependencies...")

# Run build script if it exists and libraries are not already built
if(NOT EXISTS ${LANELET2_INSTALL_DIR}/lib/liblanelet2_core.so)
    message(STATUS "Lanelet2 libraries not found, building dependencies...")
    execute_process(
        COMMAND bash ${CMAKE_CURRENT_SOURCE_DIR}/build.sh
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
        RESULT_VARIABLE BUILD_RESULT
    )
    if(NOT BUILD_RESULT EQUAL 0)
        message(FATAL_ERROR "Failed to build dependencies")
    endif()
    message(STATUS "Dependencies built successfully")
endif()

# Find scikit-build's PythonExtensions
find_package(PythonExtensions REQUIRED)

# Add subdirectory for the Python module
add_subdirectory(Rosless-Lanelet2)
add_subdirectory(autoware_lanelet2_extension)
add_subdirectory(autoware_lanelet2_extension_python)
add_subdirectory(lanelet2_python)