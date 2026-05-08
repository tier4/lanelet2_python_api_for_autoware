# Find Lanelet2 components in build directories
function(find_lanelet2_component COMPONENT)
  find_library(Lanelet2_${COMPONENT}_LIBRARY
    NAMES lanelet2_${COMPONENT}
    PATHS
      ${CMAKE_CURRENT_SOURCE_DIR}/../Rosless-Lanelet2/lanelet2_${COMPONENT}
    NO_DEFAULT_PATH
  )

  if(Lanelet2_${COMPONENT}_LIBRARY)
    set(Lanelet2_${COMPONENT}_FOUND TRUE PARENT_SCOPE)
    list(APPEND Lanelet2_LIBRARIES ${Lanelet2_${COMPONENT}_LIBRARY})
    set(Lanelet2_LIBRARIES ${Lanelet2_LIBRARIES} PARENT_SCOPE)
  endif()
endfunction()

# Find each component
foreach(comp Core IO Projection Routing Traffic_Rules Validation)
  find_lanelet2_component(${comp})
endforeach()

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(Lanelet2
  REQUIRED_VARS Lanelet2_LIBRARIES
  HANDLE_COMPONENTS
)
