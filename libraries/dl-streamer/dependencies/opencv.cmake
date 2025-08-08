include(ExternalProject)

# When changing version, you will also need to change the download hash
set(DESIRED_VERSION 4.6.0)

find_package(OpenCV ${DESIRED_VERSION})

if (OpenCV_FOUND)
    return()
endif()

ExternalProject_Add(
    opencv-contrib
    PREFIX ${CMAKE_BINARY_DIR}/opencv-contrib
    URL     https://github.com/opencv/opencv_contrib/archive/${DESIRED_VERSION}.zip
    URL_MD5 9065c130d87da6f5e7a4044f6f7ce4f6
    DOWNLOAD_EXTRACT_TIMESTAMP  true
    CONFIGURE_COMMAND   ""
    BUILD_COMMAND       ""
    INSTALL_COMMAND     ""
    TEST_COMMAND        ""
)

ExternalProject_Get_Property(opencv-contrib SOURCE_DIR)
ExternalProject_Add(
    opencv
    PREFIX ${CMAKE_BINARY_DIR}/opencv
    URL     https://github.com/opencv/opencv/archive/${DESIRED_VERSION}.zip
    URL_MD5 e86914869fd4811f42814a4a2ad98d86
    DOWNLOAD_EXTRACT_TIMESTAMP  true
    CMAKE_GENERATOR     Ninja
    TEST_COMMAND        ""
    CMAKE_ARGS          -DBUILD_TESTS=OFF 
                        -DBUILD_PERF_TESTS=OFF 
                        -DBUILD_EXAMPLES=OFF 
                        -DBUILD_opencv_apps=OFF 
                        -DOPENCV_EXTRA_MODULES_PATH=${SOURCE_DIR}/modules
                        -DCMAKE_INSTALL_PREFIX:PATH=${CMAKE_BINARY_DIR}/install 
)