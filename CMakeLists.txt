cmake_minimum_required(VERSION 3.22)

# Select the cross-toolchain before CMake detects compilers.
if(NOT CMAKE_TOOLCHAIN_FILE)
    message(FATAL_ERROR
        "STM32 firmware requires a toolchain file. Use python3 build.py "
        "or configure with cmake --preset Debug (or Release).")
endif()

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS ON)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE "Debug")
endif()

set(CMAKE_PROJECT_NAME NavScan-RT)

set(CMAKE_EXPORT_COMPILE_COMMANDS TRUE)

project(${CMAKE_PROJECT_NAME} LANGUAGES C CXX ASM)
message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")

add_executable(${CMAKE_PROJECT_NAME})

# CubeMX owns this subdirectory; application sources are registered below.
add_subdirectory(cmake/stm32cubemx)

target_sources(${CMAKE_PROJECT_NAME} PRIVATE
    App/src/app.cpp
    App/src/Lidar.cpp
)

target_include_directories(${CMAKE_PROJECT_NAME} PRIVATE
    App/include
)

# CubeMX workaround for a spurious compiler-detected 'ob' library.
list(REMOVE_ITEM CMAKE_C_IMPLICIT_LINK_LIBRARIES ob)

target_link_libraries(${CMAKE_PROJECT_NAME}
    stm32cubemx
)
