cmake_minimum_required (VERSION 3.5.1)

message(STATUS "Palisade dir: ${PALISADE_DIR}")
message(STATUS "Palisade include dir: ${PALISADE_INCLUDE_DIR}")
message(STATUS "Python include dir: ${Python3_INCLUDE_DIRS}")

project(demo CXX)
set(CMAKE_CXX_STANDARD 11)

set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(BOOST_ROOT "/home/hoseung/Work/palisade-python-demo/boost_1_77_0")

set(PYTHON_INCLUDE_PATH "$ENV{HOME}/anaconda3/envs/deepinsight/include/python3.9")
set(PYTHON_LIBRARIES "$ENV{HOME}/anaconda3/envs/deepinsight/lib/libpython3.9.so")
set(Python3_INCLUDE_DIRS "$ENV{HOME}/anaconda3/envs/deepinsight/include/python3.9")

find_package(Palisade 1.10.6) # Palisade's ConfigVersion allows this to mean that 1.10.6 is MINIMUM supported ver.
# find_package searches for the package in CMAKE_MODULE_PATH

find_package (Python 3.9 COMPONENTS Interpreter Development)
find_package (Boost 1.77 REQUIRED)
if(NOT APPLE)
	find_package (Boost 1.77 COMPONENTS python${Python3_VERSION_MAJOR}${Python3_VERSION_MINOR})
endif()
message(STATUS "CMake module path: ${CMAKE_MODULE_PATH}")

set( CMAKE_CXX_FLAGS ${PALISADE_CXX_FLAGS} )
set( CMAKE_EXE_LINKER_FLAGS ${PALISADE_EXE_LINKER_FLAGS} )

include_directories( ${OPENMP_INCLUDES} )
include_directories( ${PALISADE_INCLUDE} )
include_directories( ${PALISADE_INCLUDE}/core )
include_directories( ${PALISADE_INCLUDE}/pke )
include_directories( ${PALISADE_INCLUDE}/third-party/include )

include_directories(${Python3_INCLUDE_DIRS})
include_directories(${Boost_INCLUDE_DIRS})

link_directories( ${PALISADE_LIBDIR} )
link_directories( ${OPENMP_LIBRARIES} )

link_libraries( ${PALISADE_LIBRARIES} )

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

target_link_libraries (pycrypto PALISADEcore PALISADEpke ${Python3_LIBRARIES} ${Boost_LIBRARIES}  ${THIRDPARTYLIBS} ${OpenMP_CXX_FLAGS})

message(STATUS "Palisade include dir: ${PALISADE_INCLUDE}")
message(STATUS "Python include dir: ${Python3_INCLUDE_DIRS}")

# python code ends

