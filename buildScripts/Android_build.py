import os
import sys
import shutil

ANDROID_NDK = os.getenv("NDK_HOME")
if(ANDROID_NDK == None):
    print("no ndk found")
else:
    print("foud ndk in " + ANDROID_NDK)

BUILD_TYPE="Release"
BUILD_SHARED_LIBS="OFF"
BUILD_HIDDEN_SYMBOL="ON"
BUILD_RTTI="ON"
BUILD_EXCEPTIONS="ON"

ANDROID_STL_32BIT="c++_shared"
ANDROID_STL_64BIT="c++_shared"
ANDROID_PLATFORM="android-19"
ANDROID_TOOLCHAIN_32BIT="clang"
ANDROID_TOOLCHAIN_64BIT="clang"


CMAKE_TOOLCHAIN_FILE=ANDROID_NDK+"/build/cmake//android.toolchain.cmake"
# CMAKE_TOOLCHAIN_FILE = os.path.join(ANDROID_NDK,"/build/cmake/android.toolchain.cmake")


ALL_ARCHS=["arm64-v8a","armeabi-v7a"]

PROJECT_NAME="FiftyKEngine"


COMMON_FLAGS = " "
COMMON_FLAGS_RELEASE = " -O3"

if(BUILD_HIDDEN_SYMBOL !="OFF"):
    COMMON_FLAGS= COMMON_FLAGS+" -fvisibility=hidden -fvisibility-inlines-hidden"

if(BUILD_RTTI!= "OFF"):
     COMMON_FLAGS=COMMON_FLAGS+" -frtti"

if(BUILD_RTTI!= "OFF"):
     COMMON_FLAGS=COMMON_FLAGS+" -fexceptions"

BUILD_C_FLAGS = ""
BUILD_CXX_FLAGS = ""

BUILD_C_FLAGS = BUILD_C_FLAGS+ COMMON_FLAGS
BUILD_CXX_FLAGS = BUILD_CXX_FLAGS + COMMON_FLAGS + " -std=c++11"


for BUILD_ARCH in ALL_ARCHS:
    if(BUILD_ARCH == "amrabi-v7"):
        # armv7默认关闭neon加速，需要手动开启
        ANDROID_ABI="armeabi-v7a with NEON"
        ANDROID_STL=ANDROID_STL_32BIT
        ANDROID_TOOLCHAIN=ANDROID_TOOLCHAIN_32BIT
        CMAKE_ANDROID_NDK_TOOLCHAIN_VERSION = "gcc"
    else:
        ANDROID_ABI=BUILD_ARCH
        ANDROID_STL=ANDROID_STL_64BIT
        ANDROID_TOOLCHAIN=ANDROID_TOOLCHAIN_64BIT
        CMAKE_ANDROID_NDK_TOOLCHAIN_VERSION = "clang"

    CURRENT_DIR = os.path.split(os.path.abspath(__file__))
    CURRENT_DIR = CURRENT_DIR[0]
    OUTPUT_DIR = os.path.join(CURRENT_DIR, "lib"+PROJECT_NAME, "android", BUILD_ARCH)
    BUILD_DIR = os.path.join(CURRENT_DIR, "lib"+PROJECT_NAME+"Symbols", "android", BUILD_ARCH)


    if(os.path.exists(BUILD_DIR)):
        shutil.rmtree(BUILD_DIR)
    os.makedirs(BUILD_DIR)

    if(os.path.exists(OUTPUT_DIR)):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    CMAKE_C_FLAGS = BUILD_C_FLAGS
    CMAKE_CXX_FLAGS = BUILD_CXX_FLAGS


    CMakeCommand = "cmake"
    CMakeCommand += (" -DCMAKE_ANDROID_NDK_TOOLCHAIN_VERSION=" + CMAKE_ANDROID_NDK_TOOLCHAIN_VERSION)
    CMakeCommand += (" -DCMAKE_TOOLCHAIN_FILE=" + CMAKE_TOOLCHAIN_FILE)
    CMakeCommand += (" -DANDROID_NDK=" + ANDROID_NDK)
    CMakeCommand += (" -DANDROID_PLATFORM=" + ANDROID_PLATFORM)
    CMakeCommand += (" -DANDROID_ABI=" + ANDROID_ABI)
    CMakeCommand += (" -DCMAKE_INSTALL_PREFIX=/")
    CMakeCommand += (" -DCMAKE_BUILD_TYPE=" + CMAKE_TOOLCHAIN_FILE)
    CMakeCommand += (" -DANDROID_STL=" + ANDROID_STL)
    CMakeCommand += (" -DCMAKE_C_FLAGS=" + CMAKE_C_FLAGS)
    CMakeCommand += (" -DCMAKE_CXX_FLAGS=" + CMAKE_CXX_FLAGS)
    CMakeCommand += (" -DBUILD_SHARED_LIBS=" + BUILD_SHARED_LIBS)
    CMakeCommand += (" -DANDROID_TOOLCHAIN=" + ANDROID_TOOLCHAIN)
    CMakeCommand += (" -DCMAKE_C_FLAGS_RELEASE=" + COMMON_FLAGS_RELEASE)
    CMakeCommand += (" -DCMAKE_CXX_FLAGS_RELEASE=" + COMMON_FLAGS_RELEASE)
    CMakeCommand += (" -DANDROID_ARM_NEON=" + "TRUE")
    CMakeCommand += " " + CURRENT_DIR+"/.."
    print(CMakeCommand)


    bashCommand = "cd " + BUILD_DIR
    bashCommand += "&& " + CMakeCommand
    bashCommand += "&& make all -j8"
    bashCommand += "&& make install/strip DESTDIR=" + OUTPUT_DIR

    os.system(bashCommand)
    # os.system("cd " + CURRENT_DIR);

