cmake_minimum_required(VERSION 3.5.1)
project(lanelet2_matching VERSION 4.0.0)

# Set C++ standard
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Find required dependencies
find_package(Eigen3 REQUIRED)
find_package(Boost REQUIRED)
# find_package(lanelet2_core REQUIRED)
# find_package(lanelet2_traffic_rules REQUIRED)

# Collect source files
file(GLOB_RECURSE HEADER_FILES
    "include/${PROJECT_NAME}/*.h"
    "include/${PROJECT_NAME}/*.hpp"
    "include/${PROJECT_NAME}/*.cuh"
)

file(GLOB SOURCE_FILES
    "src/*.cpp"
    "src/*.cu"
)

# Create main library
add_library(${PROJECT_NAME} SHARED
    ${SOURCE_FILES}
    ${HEADER_FILES}
)

# Set include directories
target_include_directories(${PROJECT_NAME}
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include>
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/src
        ${CMAKE_CURRENT_SOURCE_DIR}/include/${PROJECT_NAME}  # Add this line
)

# Link dependencies
target_link_libraries(${PROJECT_NAME}
    PUBLIC
        Eigen3::Eigen
        lanelet2_core
        lanelet2_traffic_rules
        Boost::boost
)


# Install targets
install(TARGETS ${PROJECT_NAME}
    EXPORT ${PROJECT_NAME}-targets
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
    INCLUDES DESTINATION include
)

# Install headers
install(DIRECTORY include/${PROJECT_NAME}/
    DESTINATION include/${PROJECT_NAME}
    FILES_MATCHING PATTERN "*.h"
                   PATTERN "*.hpp"
                   PATTERN "*.cuh"
)

# Export targets
install(EXPORT ${PROJECT_NAME}-targets
    FILE ${PROJECT_NAME}-targets.cmake
    NAMESPACE ${PROJECT_NAME}::
    DESTINATION lib/cmake/${PROJECT_NAME}
)

# Create and install config file
include(CMakePackageConfigHelpers)
configure_package_config_file(
    cmake/${PROJECT_NAME}-config.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}-config.cmake
    INSTALL_DESTINATION lib/cmake/${PROJECT_NAME}
)

install(FILES
    ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}-config.cmake
    DESTINATION lib/cmake/${PROJECT_NAME}
)
