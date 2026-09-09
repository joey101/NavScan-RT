# CubeMX may regenerate this toolchain file. Keep application build changes in
# the root CMakeLists.txt; these comments explain the generated target settings.

# Generic means bare metal (no target OS). 'arm' describes the STM32 target,
# independently of the Linux x86_64 computer running CMake.
set(CMAKE_SYSTEM_NAME               Generic)
set(CMAKE_SYSTEM_PROCESSOR          arm)

set(CMAKE_C_COMPILER_ID GNU)
set(CMAKE_CXX_COMPILER_ID GNU)

# Resolve cross-compilers from PATH, using their shared executable-name prefix.
# This does not download the toolchain: its bin directory must already be on PATH.
set(TOOLCHAIN_PREFIX                arm-none-eabi-)

# Compile .c with gcc, .cpp with g++, and startup assembly with the gcc driver.
set(CMAKE_C_COMPILER                ${TOOLCHAIN_PREFIX}gcc)
set(CMAKE_ASM_COMPILER              ${CMAKE_C_COMPILER})
set(CMAKE_CXX_COMPILER              ${TOOLCHAIN_PREFIX}g++)
set(CMAKE_LINKER                    ${TOOLCHAIN_PREFIX}g++)
set(CMAKE_OBJCOPY                   ${TOOLCHAIN_PREFIX}objcopy)
set(CMAKE_SIZE                      ${TOOLCHAIN_PREFIX}size)

# ELF retains symbols and memory-section information for ST-LINK/GDB debugging.
set(CMAKE_EXECUTABLE_SUFFIX_ASM     ".elf")
set(CMAKE_EXECUTABLE_SUFFIX_C       ".elf")
set(CMAKE_EXECUTABLE_SUFFIX_CXX     ".elf")

# Compiler probes build a library: a bare-metal test executable would need our
# startup code and linker script, and cannot run on the development computer.
set(CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY)

# F446RE: Cortex-M4 CPU, single-precision FPv4 FPU, hardware floating-point ABI.
# Objects and libraries linked together must use compatible CPU/FPU/ABI settings.
set(TARGET_FLAGS "-mcpu=cortex-m4 -mfpu=fpv4-sp-d16 -mfloat-abi=hard ")

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${TARGET_FLAGS}")
# Preprocess startup assembly; emit dependency files so header edits rebuild it.
set(CMAKE_ASM_FLAGS "${CMAKE_C_FLAGS} -x assembler-with-cpp -MMD -MP")
# Split functions/data into sections for linker garbage collection. Emit .su
# reports describing stack use; -Wall enables common compiler warnings.
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -fdata-sections -ffunction-sections -fstack-usage")

# The cyclomatic-complexity parameter must be defined for the Cyclomatic complexity feature in STM32CubeIDE to work.
# However, most GCC toolchains do not support this option, which causes a compilation error; for this reason, the feature is disabled by default.
# set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fcyclomatic-complexity")

# Debug favors source-level stepping; Release favors small firmware size.
set(CMAKE_C_FLAGS_DEBUG "-O0 -g3")
set(CMAKE_C_FLAGS_RELEASE "-Os -g0")
set(CMAKE_CXX_FLAGS_DEBUG "-O0 -g3")
set(CMAKE_CXX_FLAGS_RELEASE "-Os -g0")

# CubeMX disables RTTI, exceptions, and guards for local-static initialization.
# With these flags, initialize local-static objects before concurrent task access.
set(CMAKE_CXX_FLAGS "${CMAKE_C_FLAGS} -fno-rtti -fno-exceptions -fno-threadsafe-statics")

set(CMAKE_EXE_LINKER_FLAGS "${TARGET_FLAGS}")
# The linker script places vector tables, code, data, heap, and stack in MCU memory.
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -T \"${CMAKE_SOURCE_DIR}/STM32F446xx_FLASH.ld\"")
# Use the size-oriented newlib-nano C library. Emit a map and discard unused sections.
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} --specs=nano.specs")
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -Wl,-Map=${CMAKE_PROJECT_NAME}.map -Wl,--gc-sections")
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -Wl,--print-memory-usage")
# libm supplies mathematical functions such as sin/cos for later scan processing.
set(TOOLCHAIN_LINK_LIBRARIES "m")
