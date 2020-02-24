cmake_minimum_required (VERSION 3.5.1)

project(demo C CXX)
set(CMAKE_CXX_STANDARD 11)

set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

if(APPLE)
        set(OPENMP_LIBRARIES "/usr/local/opt/libomp/lib")
        set(OPENMP_INCLUDES "/usr/local/opt/libomp/include")
endif()

OPTION (USE_OpenMP "Use OpenMP to enable <omp.h>" ON)

# Set OpenMP configuration manually for macOS
if(APPLE AND USE_OpenMP)
    if(CMAKE_C_COMPILER_ID MATCHES "Clang")
       set(OpenMP_C_FLAGS "-Xpreprocessor -fopenmp -lomp -Wno-unused-command-line-argument")
       set(OpenMP_C_LIB_NAMES "libomp")
       set(OpenMP_libomp_LIBRARY ${OpenMP_C_LIB_NAMES})
    endif()
    if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
       set(OpenMP_CXX_FLAGS "-Xpreprocessor -fopenmp -lomp -Wno-unused-command-line-argument")
       set(OpenMP_CXX_LIB_NAMES "libomp")
       set(OpenMP_libomp_LIBRARY ${OpenMP_CXX_LIB_NAMES})
    endif()
endif()

find_package (Python3 COMPONENTS Interpreter Development)
if(NOT APPLE)
	find_package (Boost COMPONENTS python${Python3_VERSION_MAJOR}${Python3_VERSION_MINOR})
endif()

find_package (OpenMP)

if( APPLE AND USE_OpenMP)
        include_directories("${OPENMP_INCLUDES}")
        link_directories("${OPENMP_LIBRARIES}")
        set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
        set (CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
endif()

# OpenMP_CXX_FOUND was added in cmake 3.9.x
# so we are also checking the OpenMP_FOUND flag
if (OpenMP_CXX_FOUND OR OpenMP_FOUND)
        set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
        set (CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
        message("-- OpenMP is turned ON")
else()
        message("-- OpenMP is turned OFF")
endif()

if (OpenMP_C_FOUND)
        set (CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
endif()

# Added -Wno-parentheses -Wno-pessimizing-move for compatibility with g++ >= v9.0
if("${CMAKE_CXX_COMPILER_ID}" STREQUAL "GNU")
    if (CMAKE_CXX_COMPILER_VERSION VERSION_LESS 9.0)
                set (IGNORE_WARNINGS "")
        else()
                set (IGNORE_WARNINGS "-Wno-parentheses -Wno-pessimizing-move")
        endif()
endif()
if(APPLE AND "${CMAKE_CXX_COMPILER_ID}" MATCHES "Clang")
        set(IGNORE_WARNINGS "${IGNORE_WARNINGS} -Wno-unused-private-field -Wno-shift-op-parentheses")
endif()
#-Werror 
set(COMPILEFLAGS "-Wall -O3 -DPALISADE_VERSION=${PALISADE_VERSION} ${IGNORE_WARNINGS} -Wno-deprecated-declarations")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${COMPILEFLAGS}")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${COMPILEFLAGS}")

# be sure to set PALISADE_DIR to the base install directory for PALISADE: -DPALISADE_DIR=/your/path

if( "${PALISADE_DIR}" STREQUAL "" )
	message(SEND_ERROR "PALISADE_DIR must be set to the install location for PALISADE")
endif()

include_directories( ${PALISADE_DIR}/include/palisade )
include_directories( ${PALISADE_DIR}/include/palisade/core )
include_directories( ${PALISADE_DIR}/include/palisade/pke )
include_directories( ${PALISADE_DIR}/include/palisade/trapdoor )

include_directories(${Python3_INCLUDE_DIRS})
include_directories(${Boost_INCLUDE_DIRS})

# python code
# builds the .so file for python

file (GLOB_RECURSE PYTHON_SRC_FILES CONFIGURE_DEPENDS src/*.cpp)

add_library (pythonobj OBJECT ${PYTHON_SRC_FILES})
# add_dependencies(pythonobj PALISADEcore PALISADEpke PALISADEduality)
set_property(TARGET pythonobj PROPERTY POSITION_INDEPENDENT_CODE 1)

add_library (pycrypto SHARED $<TARGET_OBJECTS:pythonobj>)
set_property(TARGET pycrypto PROPERTY VERSION 1)
set_property(TARGET pycrypto PROPERTY SOVERSION 1)
set_property(TARGET pycrypto PROPERTY RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib/)
set_property(TARGET pycrypto PROPERTY PREFIX "")
install(TARGETS pycrypto DESTINATION lib)

target_link_directories(pycrypto PUBLIC ${PALISADE_DIR}/lib)

target_link_libraries (pycrypto PALISADEcore PALISADEpke PALISADEtrapdoor ${Python3_LIBRARIES} ${Boost_LIBRARIES}  ${THIRDPARTYLIBS} ${OpenMP_CXX_FLAGS})

# python code ends
