cmake_minimum_required(VERSION 3.14)
project(lanelet2_extension)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(PYTHON_INSTALL_DIR "lib/python3/dist-packages")

# Add path to custom cmake modules if needed
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake/")

# Find all required packages
find_package(Boost REQUIRED)
find_package(Eigen3 REQUIRED)
find_package(GeographicLib REQUIRED)
find_package(pugixml REQUIRED)
find_package(range-v3 REQUIRED)

# Find Lanelet2 components
# Set paths to Lanelet2 build directories
set(LANELET2_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/../Rosless-Lanelet2")

# Create imported targets for Lanelet2 components
foreach(comp core io projection routing traffic_rules validation)
    string(TOUPPER ${comp} COMP_UPPER)

    # Find library - check multiple possible locations
    find_library(Lanelet2_${COMP_UPPER}_LIBRARY
        NAMES lanelet2_${comp}
        PATHS
            "${CMAKE_INSTALL_PREFIX}/lib"
            "${LANELET2_ROOT}/build/lanelet2_${comp}"
            "${LANELET2_ROOT}/build/lib"
            "${LANELET2_ROOT}/install/lib"
        NO_DEFAULT_PATH
    )

    # Check for include directory in multiple locations
    if(EXISTS "${CMAKE_INSTALL_PREFIX}/include/lanelet2_${comp}")
        set(Lanelet2_${COMP_UPPER}_INCLUDE_DIR "${CMAKE_INSTALL_PREFIX}/include")
    elseif(EXISTS "${LANELET2_ROOT}/install/include/lanelet2_${comp}")
        set(Lanelet2_${COMP_UPPER}_INCLUDE_DIR "${LANELET2_ROOT}/install/include")
    else()
        set(Lanelet2_${COMP_UPPER}_INCLUDE_DIR "${LANELET2_ROOT}/lanelet2_${comp}/include")
    endif()

    message(STATUS "Looking for ${comp} in:")
    message(STATUS "  Library: ${LANELET2_ROOT}/build/lanelet2_${comp}")
    message(STATUS "  Include: ${Lanelet2_${COMP_UPPER}_INCLUDE_DIR}")
    message(STATUS "Found library: ${Lanelet2_${COMP_UPPER}_LIBRARY}")

    if(Lanelet2_${COMP_UPPER}_LIBRARY AND EXISTS "${Lanelet2_${COMP_UPPER}_INCLUDE_DIR}")
        add_library(Lanelet2::${comp} UNKNOWN IMPORTED)
        set_target_properties(Lanelet2::${comp} PROPERTIES
            IMPORTED_LOCATION "${Lanelet2_${COMP_UPPER}_LIBRARY}"
            INTERFACE_INCLUDE_DIRECTORIES "${Lanelet2_${COMP_UPPER}_INCLUDE_DIR}"
        )
        message(STATUS "Successfully configured Lanelet2_${comp}")
    else()
        message(FATAL_ERROR "Could not find Lanelet2 component: ${comp}\n"
                          "Library path: ${Lanelet2_${COMP_UPPER}_LIBRARY}\n"
                          "Include path: ${Lanelet2_${COMP_UPPER}_INCLUDE_DIR}")
    endif()

    unset(Lanelet2_${COMP_UPPER}_LIBRARY CACHE)
endforeach()

add_library(${PROJECT_NAME}_lib SHARED
  lib/autoware_osm_parser.cpp
  lib/autoware_traffic_light.cpp
  lib/crosswalk.cpp
  lib/detection_area.cpp
  lib/no_parking_area.cpp
  lib/no_stopping_area.cpp
  lib/bus_stop_area.cpp
  lib/mgrs_projector.cpp
  lib/query.cpp
  lib/road_marking.cpp
  lib/speed_bump.cpp
  lib/transverse_mercator_projector.cpp
  lib/utilities.cpp
  lib/virtual_traffic_light.cpp
)

# Now we can set include directories for our library
target_include_directories(${PROJECT_NAME}_lib
  PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
  PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/lib
)

# And link against the dependencies
target_link_libraries(${PROJECT_NAME}_lib
  PUBLIC
    Lanelet2::core
    Lanelet2::io
    Lanelet2::projection
    Lanelet2::routing
    Lanelet2::traffic_rules
    Lanelet2::validation
    GeographicLib::GeographicLib
    pugixml::pugixml
    range-v3::range-v3
    Boost::boost
    Eigen3::Eigen
)

# Install targets
install(TARGETS ${PROJECT_NAME}_lib
  EXPORT ${PROJECT_NAME}Targets
  LIBRARY DESTINATION lib
  ARCHIVE DESTINATION lib
  RUNTIME DESTINATION bin
  INCLUDES DESTINATION include
)

# Install headers
install(DIRECTORY include/
  DESTINATION include
  FILES_MATCHING PATTERN "*.hpp" PATTERN "*.h"
)

add_executable(${PROJECT_NAME}_sample src/sample_code.cpp)
target_link_libraries(${PROJECT_NAME}_sample
  ${PROJECT_NAME}_lib
)
