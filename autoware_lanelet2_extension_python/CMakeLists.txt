cmake_minimum_required(VERSION 3.14)
project(lanelet2_extension_python)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(CMAKE_SKIP_BUILD_RPATH FALSE)
set(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)
set(CMAKE_INSTALL_RPATH "$ORIGIN;$ORIGIN/lib")
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
set(PYTHON_INSTALL_DIR "lib/python3/dist-packages")

# Add path to custom cmake modules if needed
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake/")


find_package(Python3 REQUIRED COMPONENTS Interpreter Development)
find_package(Boost REQUIRED COMPONENTS python${Python3_VERSION_MAJOR}${Python3_VERSION_MINOR})
find_package(Eigen3 REQUIRED)

include_directories(
  ${Boost_INCLUDE_DIRS}
  ${Python3_INCLUDE_DIRS}
  ${EIGEN3_INCLUDE_DIRS}
)

# Find Lanelet2 components
# Set paths to Lanelet2 build directories
set(LANELET2_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/../Rosless-Lanelet2")

# Create imported targets for Lanelet2 components
foreach(comp core io projection routing traffic_rules validation)
    string(TOUPPER ${comp} COMP_UPPER)

    # Find library
    find_library(Lanelet2_${COMP_UPPER}_LIBRARY
        NAMES lanelet2_${comp}
        PATHS
            "${LANELET2_ROOT}/build/lanelet2_${comp}"
            "${LANELET2_ROOT}/build/lib"
        NO_DEFAULT_PATH
    )

    # Directly set the include directory path
    set(Lanelet2_${COMP_UPPER}_INCLUDE_DIR "${LANELET2_ROOT}/lanelet2_${comp}/include")

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

set(Lanelet2_PYTHON_INCLUDE_DIR "${LANELET2_ROOT}/lanelet2_python/include")

## add path to lanelet2_extension
set(LANELET2_EXTENSION_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/../autoware_lanelet2_extension")
find_library(Lanelet2_Extension_LIBRARY
    NAMES lanelet2_extension_lib
    PATHS
        "${LANELET2_EXTENSION_ROOT}/build/"
    NO_DEFAULT_PATH
)
set(Lanelet2_Extension_INCLUDE_DIR "${LANELET2_EXTENSION_ROOT}/include")
message(STATUS "  Library: ${Lanelet2_Extension_LIBRARY}")
message(STATUS "  Include: ${Lanelet2_Extension_INCLUDE_DIR}")
if(Lanelet2_Extension_LIBRARY AND EXISTS ${Lanelet2_Extension_INCLUDE_DIR})
        add_library(Lanelet2::Extension UNKNOWN IMPORTED)
        set_target_properties(Lanelet2::Extension PROPERTIES
            IMPORTED_LOCATION "${Lanelet2_Extension_LIBRARY}"
            INTERFACE_INCLUDE_DIRECTORIES "${Lanelet2_Extension_INCLUDE_DIR}"
        )
        message(STATUS "Successfully configured Lanelet2_${comp}")
    else()
        message(FATAL_ERROR "Could not find Lanelet2 component: ${comp}\n"
                          "Library path: ${Lanelet2_Extension_LIBRARY}\n"
                          "Include path: ${Lanelet2_Extension_INCLUDE_DIR}")
endif()



set(CMAKE_SHARED_LIBRARY_PREFIX "")
add_library(_${PROJECT_NAME}_boost_python_utility SHARED
  src/utility.cpp
)
target_link_libraries(_${PROJECT_NAME}_boost_python_utility
  ${Boost_LIBRARIES}
  Eigen3::Eigen
  Lanelet2::core
  Lanelet2::io
  Lanelet2::projection
  Lanelet2::routing
  Lanelet2::traffic_rules
  Lanelet2::validation
  Lanelet2::Extension
)
target_include_directories(_${PROJECT_NAME}_boost_python_utility
  PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
    ${Lanelet2_PYTHON_INCLUDE_DIR}
  PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/lib
)
set_target_properties(_${PROJECT_NAME}_boost_python_utility PROPERTIES
  INSTALL_RPATH "$ORIGIN;$ORIGIN/lib"
  BUILD_RPATH "$ORIGIN;$ORIGIN/lib"
  SKIP_BUILD_RPATH FALSE
)

add_library(_${PROJECT_NAME}_boost_python_projection SHARED
  src/projection.cpp
)
target_link_libraries(_${PROJECT_NAME}_boost_python_projection
  ${Boost_LIBRARIES}
  Eigen3::Eigen
  Lanelet2::core
  Lanelet2::io
  Lanelet2::projection
  Lanelet2::Extension
)
target_include_directories(_${PROJECT_NAME}_boost_python_projection
  PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
    ${Lanelet2_PYTHON_INCLUDE_DIR}
  PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/lib
)
set_target_properties(_${PROJECT_NAME}_boost_python_projection PROPERTIES
  INSTALL_RPATH "$ORIGIN;$ORIGIN/lib"
  BUILD_RPATH "$ORIGIN;$ORIGIN/lib"
  SKIP_BUILD_RPATH FALSE
)

add_library(_${PROJECT_NAME}_boost_python_regulatory_elements SHARED
  src/regulatory_elements.cpp
)
target_link_libraries(_${PROJECT_NAME}_boost_python_regulatory_elements
  ${Boost_LIBRARIES}
  Eigen3::Eigen
  Lanelet2::core
  Lanelet2::io
  Lanelet2::Extension
)
set_target_properties(_${PROJECT_NAME}_boost_python_regulatory_elements PROPERTIES
  INSTALL_RPATH "$ORIGIN;$ORIGIN/lib"
  BUILD_RPATH "$ORIGIN;$ORIGIN/lib"
  SKIP_BUILD_RPATH FALSE
)

install(TARGETS
  _${PROJECT_NAME}_boost_python_utility
  _${PROJECT_NAME}_boost_python_projection
  _${PROJECT_NAME}_boost_python_regulatory_elements
  DESTINATION "${PYTHON_INSTALL_DIR}/autoware_${PROJECT_NAME}"
)

install(DIRECTORY
  ${CMAKE_CURRENT_SOURCE_DIR}/autoware_lanelet2_extension_python
  DESTINATION "${PYTHON_INSTALL_DIR}"
  FILES_MATCHING
  PATTERN "*.py"
  PATTERN "__pycache__" EXCLUDE
)

# Install shared libraries alongside the Python module
install(FILES
    ${CMAKE_CURRENT_SOURCE_DIR}/../Rosless-Lanelet2/build/lanelet2_core/liblanelet2_core.so
    ${CMAKE_CURRENT_SOURCE_DIR}/../Rosless-Lanelet2/build/lanelet2_io/liblanelet2_io.so
    ${CMAKE_CURRENT_SOURCE_DIR}/../Rosless-Lanelet2/build/lanelet2_projection/liblanelet2_projection.so
    ${CMAKE_CURRENT_SOURCE_DIR}/../Rosless-Lanelet2/build/lanelet2_routing/liblanelet2_routing.so
    ${CMAKE_CURRENT_SOURCE_DIR}/../Rosless-Lanelet2/build/lanelet2_traffic_rules/liblanelet2_traffic_rules.so
    ${CMAKE_CURRENT_SOURCE_DIR}/../Rosless-Lanelet2/build/lanelet2_matching/liblanelet2_matching.so
    ${CMAKE_CURRENT_SOURCE_DIR}/../Rosless-Lanelet2/build/lanelet2_validation/liblanelet2_validation.so
    ${CMAKE_CURRENT_SOURCE_DIR}/../autoware_lanelet2_extension/build/liblanelet2_extension_lib.so
    DESTINATION "${PYTHON_INSTALL_DIR}/autoware_${PROJECT_NAME}/lib"
    OPTIONAL
)
