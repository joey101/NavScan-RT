# CMake 3.22 supports the preset format used by this project.
cmake_minimum_required(VERSION 3.22)

# This root file is the place for application build settings. CubeMX regenerates
# cmake/stm32cubemx/CMakeLists.txt, so custom source lists belong here instead.

# Require an explicit cross-compilation setup before project() checks compilers.
# The Debug/Release presets supply this file; an ordinary host build is invalid.
if(NOT CMAKE_TOOLCHAIN_FILE)
    message(FATAL_ERROR
        "STM32 firmware requires a toolchain file. Use python3 build.py "
        "or configure with cmake --preset Debug (or Release).")
endif()

# Generated HAL/FreeRTOS code uses C11 and GNU C extensions.
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS ON)

# Application .cpp files use C++17. CMake calls the C++ language 'CXX'.
# REQUIRED prevents silently falling back to an older standard.
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Presets select Debug or Release; retain Debug as the manual-toolchain default.
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE "Debug")
endif()

# This names the firmware target and its output files, matching the CubeMX name.
set(CMAKE_PROJECT_NAME NavScan-RT)

# Export per-source compiler commands for clangd/Neovim. build.py links this
# build-directory file into the repository root for the editor to discover.
set(CMAKE_EXPORT_COMPILE_COMMANDS TRUE)

# Load the selected toolchain and enable C, C++, and the startup assembly.
# The toolchain selects Arm compilers; these language names do not select a CPU.
project(${CMAKE_PROJECT_NAME} LANGUAGES C CXX ASM)
message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")

# Declare the firmware executable. Sources are attached below and by CubeMX;
# the Arm toolchain supplies the .elf suffix and STM32 flash/RAM linker script.
add_executable(${CMAKE_PROJECT_NAME})

# Import HAL, CMSIS, FreeRTOS, startup code, and generated application sources.
# The stm32cubemx interface target carries shared include paths and definitions.
add_subdirectory(cmake/stm32cubemx)

# Add search directories here only when using additional prebuilt libraries.
target_link_directories(${CMAKE_PROJECT_NAME} PRIVATE
    # Add user defined library search paths
)

# List your own .c/.cpp files here, using paths relative to this root directory.
# CMake compiles .cpp files as C++ and uses the C++ driver for the final link.
target_sources(${CMAKE_PROJECT_NAME} PRIVATE
    App/app.cpp
    # Add user sources here
)

# Add directories containing your own headers (for example App/).
# PRIVATE applies these paths to this firmware target, not to its dependencies.
target_include_directories(${CMAKE_PROJECT_NAME} PRIVATE
    App
    # Add user defined include paths
)

# Add application-specific preprocessor definitions here, without a -D prefix.
target_compile_definitions(${CMAKE_PROJECT_NAME} PRIVATE
    # Add user defined symbols
)

# Retain CubeMX's workaround for a spurious compiler-detected 'ob' library.
list(REMOVE_ITEM CMAKE_C_IMPLICIT_LINK_LIBRARIES ob)

# Link shared CubeMX build requirements, followed by any application libraries.
target_link_libraries(${CMAKE_PROJECT_NAME}
    stm32cubemx

    # Add user defined libraries
)
