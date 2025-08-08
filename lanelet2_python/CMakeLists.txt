# Find required packages
find_package(pybind11 REQUIRED)

# Set installation prefix for dependencies if not set
if(NOT CMAKE_INSTALL_PREFIX)
    set(CMAKE_INSTALL_PREFIX ${CMAKE_CURRENT_SOURCE_DIR}/../install)
endif()

# Set install directory for dependencies
set(LANELET2_INSTALL_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../install)

# Create Python extension module
add_library(_lanelet2_python_api MODULE
    ${CMAKE_CURRENT_SOURCE_DIR}/../src/main.cpp
)

# Set properties for the Python module
python_extension_module(_lanelet2_python_api)

# Include directories
target_include_directories(_lanelet2_python_api PRIVATE
    ${LANELET2_INSTALL_DIR}/include
    ${CMAKE_CURRENT_SOURCE_DIR}/../Rosless-Lanelet2/lanelet2_core/include
    ${CMAKE_CURRENT_SOURCE_DIR}/../Rosless-Lanelet2/lanelet2_io/include
    ${CMAKE_CURRENT_SOURCE_DIR}/../Rosless-Lanelet2/lanelet2_routing/include
    ${CMAKE_CURRENT_SOURCE_DIR}/../Rosless-Lanelet2/lanelet2_projection/include
    ${CMAKE_CURRENT_SOURCE_DIR}/../Rosless-Lanelet2/lanelet2_traffic_rules/include
    ${CMAKE_CURRENT_SOURCE_DIR}/../Rosless-Lanelet2/lanelet2_matching/include
    ${CMAKE_CURRENT_SOURCE_DIR}/../autoware_lanelet2_extension/include
)

# Link directories
link_directories(${LANELET2_INSTALL_DIR}/lib)

# Link against Lanelet2 libraries
target_link_libraries(_lanelet2_python_api PRIVATE
    pybind11::module
    lanelet2_core
    lanelet2_io
    lanelet2_routing
    lanelet2_projection
    lanelet2_traffic_rules
    lanelet2_matching
    lanelet2_extension_lib
)

# Install the Python module
install(TARGETS _lanelet2_python_api LIBRARY DESTINATION lanelet2_python)