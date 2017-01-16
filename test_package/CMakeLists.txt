project(FoundationTimer)
cmake_minimum_required(VERSION 2.8.12)

SET(CMAKE_CXX_STANDARD 14)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

FIND_PACKAGE(Threads REQUIRED)

add_executable(cftest cftest.cpp)
target_link_libraries(cftest ${CONAN_LIBS} ${CMAKE_THREAD_LIBS_INIT})

