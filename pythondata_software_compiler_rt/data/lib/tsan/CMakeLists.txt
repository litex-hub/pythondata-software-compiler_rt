# Build for the ThreadSanitizer runtime support library.

include_directories(..)

set(TSAN_CFLAGS ${SANITIZER_COMMON_CFLAGS})
# SANITIZER_COMMON_CFLAGS contains -fPIC, but it's performance-critical for
# TSan runtime to be built with -fPIE to reduce the number of register spills.
append_list_if(COMPILER_RT_HAS_FPIE_FLAG -fPIE TSAN_CFLAGS)
append_no_rtti_flag(TSAN_CFLAGS)

set(TSAN_RTL_CFLAGS ${TSAN_CFLAGS})
append_list_if(COMPILER_RT_HAS_MSSE3_FLAG -msse3 TSAN_RTL_CFLAGS)
append_list_if(SANITIZER_LIMIT_FRAME_SIZE -Wframe-larger-than=512
               TSAN_RTL_CFLAGS)
append_list_if(COMPILER_RT_HAS_WGLOBAL_CONSTRUCTORS_FLAG -Wglobal-constructors
               TSAN_RTL_CFLAGS)
# FIXME: Add support for --sysroot=. compile flag:

set(TSAN_SOURCES
  rtl/tsan_clock.cc
  rtl/tsan_flags.cc
  rtl/tsan_fd.cc
  rtl/tsan_ignoreset.cc
  rtl/tsan_interceptors.cc
  rtl/tsan_interface_ann.cc
  rtl/tsan_interface_atomic.cc
  rtl/tsan_interface.cc
  rtl/tsan_interface_java.cc
  rtl/tsan_malloc_mac.cc
  rtl/tsan_md5.cc
  rtl/tsan_mman.cc
  rtl/tsan_mutex.cc
  rtl/tsan_mutexset.cc
  rtl/tsan_report.cc
  rtl/tsan_rtl.cc
  rtl/tsan_rtl_mutex.cc
  rtl/tsan_rtl_report.cc
  rtl/tsan_rtl_thread.cc
  rtl/tsan_stack_trace.cc
  rtl/tsan_stat.cc
  rtl/tsan_suppressions.cc
  rtl/tsan_symbolize.cc
  rtl/tsan_sync.cc)

set(TSAN_CXX_SOURCES
  rtl/tsan_new_delete.cc)

if(APPLE)
  list(APPEND TSAN_SOURCES
    rtl/tsan_platform_mac.cc
    rtl/tsan_platform_posix.cc)
elseif(UNIX)
  # Assume Linux
  list(APPEND TSAN_SOURCES
    rtl/tsan_platform_linux.cc
    rtl/tsan_platform_posix.cc)
endif()

set(TSAN_HEADERS
  rtl/tsan_clock.h
  rtl/tsan_defs.h
  rtl/tsan_dense_alloc.h
  rtl/tsan_fd.h
  rtl/tsan_flags.h
  rtl/tsan_flags.inc
  rtl/tsan_ignoreset.h
  rtl/tsan_interceptors.h
  rtl/tsan_interface_ann.h
  rtl/tsan_interface.h
  rtl/tsan_interface_inl.h
  rtl/tsan_interface_java.h
  rtl/tsan_mman.h
  rtl/tsan_mutex.h
  rtl/tsan_mutexset.h
  rtl/tsan_platform.h
  rtl/tsan_report.h
  rtl/tsan_rtl.h
  rtl/tsan_stack_trace.h
  rtl/tsan_stat.h
  rtl/tsan_suppressions.h
  rtl/tsan_symbolize.h
  rtl/tsan_sync.h
  rtl/tsan_trace.h
  rtl/tsan_update_shadow_word_inl.h
  rtl/tsan_vector.h)

set(TSAN_RUNTIME_LIBRARIES)
add_custom_target(tsan)

if(APPLE)
  add_compiler_rt_runtime(clang_rt.tsan
    SHARED
    OS ${TSAN_SUPPORTED_OS}
    ARCHS ${TSAN_SUPPORTED_ARCH}
    SOURCES ${TSAN_SOURCES} ${TSAN_CXX_SOURCES}
    OBJECT_LIBS RTInterception
                RTSanitizerCommon
                RTSanitizerCommonLibc
                RTUbsan
    CFLAGS ${TSAN_RTL_CFLAGS}
    PARENT_TARGET tsan)
else()
  foreach(arch ${TSAN_SUPPORTED_ARCH})
    if(arch STREQUAL "x86_64")
      set(TSAN_ASM_SOURCES rtl/tsan_rtl_amd64.S)
      # Pass ASM file directly to the C++ compiler.
      set_source_files_properties(${TSAN_ASM_SOURCES} PROPERTIES
        LANGUAGE C)
      # Sanity check for Go runtime.
      set(BUILDGO_SCRIPT ${CMAKE_CURRENT_SOURCE_DIR}/go/buildgo.sh)
      add_custom_target(GotsanRuntimeCheck
        COMMAND env "CC=${CMAKE_C_COMPILER} ${CMAKE_C_COMPILER_ARG1}"
                IN_TMPDIR=1 SILENT=1 ${BUILDGO_SCRIPT}
        DEPENDS clang_rt.tsan-${arch} ${BUILDGO_SCRIPT}
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/go
        COMMENT "Checking TSan Go runtime..."
        VERBATIM)
    else()
      set(TSAN_ASM_SOURCES)
    endif()
    add_compiler_rt_runtime(clang_rt.tsan
      STATIC
      ARCHS ${arch}
      SOURCES ${TSAN_SOURCES} ${TSAN_ASM_SOURCES}
              $<TARGET_OBJECTS:RTInterception.${arch}>
              $<TARGET_OBJECTS:RTSanitizerCommon.${arch}>
              $<TARGET_OBJECTS:RTSanitizerCommonLibc.${arch}>
              $<TARGET_OBJECTS:RTUbsan.${arch}>
      CFLAGS ${TSAN_RTL_CFLAGS})
    add_compiler_rt_runtime(clang_rt.tsan_cxx
      STATIC
      ARCHS ${arch}
      SOURCES ${TSAN_CXX_SOURCES}
              $<TARGET_OBJECTS:RTUbsan_cxx.${arch}>
      CFLAGS ${TSAN_RTL_CFLAGS})
    list(APPEND TSAN_RUNTIME_LIBRARIES clang_rt.tsan-${arch}
                                       clang_rt.tsan_cxx-${arch})
    add_sanitizer_rt_symbols(clang_rt.tsan
      ARCHS ${arch}
      EXTRA rtl/tsan.syms.extra)
    add_sanitizer_rt_symbols(clang_rt.tsan_cxx
      ARCHS ${arch}
      EXTRA rtl/tsan.syms.extra)
    add_dependencies(tsan clang_rt.tsan-${arch}
                          clang_rt.tsan_cxx-${arch}
                          clang_rt.tsan-${arch}-symbols
                          clang_rt.tsan_cxx-${arch}-symbols)
  endforeach()
endif()

add_dependencies(compiler-rt tsan)

# Build libcxx instrumented with TSan.
if(COMPILER_RT_HAS_LIBCXX_SOURCES AND
   COMPILER_RT_TEST_COMPILER_ID STREQUAL "Clang")
  set(LIBCXX_PREFIX ${CMAKE_CURRENT_BINARY_DIR}/libcxx_tsan)
  add_custom_libcxx(libcxx_tsan ${LIBCXX_PREFIX}
    DEPS ${TSAN_RUNTIME_LIBRARIES}
    CFLAGS -fsanitize=thread)
endif()

if(COMPILER_RT_INCLUDE_TESTS)
  add_subdirectory(tests)
endif()
