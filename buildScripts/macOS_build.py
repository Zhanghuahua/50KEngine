import os
import sys
import shutil

PROJECT_NAME = "FiftyKEngine"
# 编译安装目录

CURRENT_DIR = os.path.split(os.path.abspath(__file__))
CURRENT_DIR = CURRENT_DIR[0]
OUTPUT_DIR = os.path.join(CURRENT_DIR, "lib"+PROJECT_NAME, "macOS")
BUILD_DIR = os.path.join(CURRENT_DIR, "lib"+PROJECT_NAME+"Symbols", "macOS")

if(os.path.exists(BUILD_DIR)):
    shutil.rmtree(BUILD_DIR)
os.makedirs(BUILD_DIR)

if(os.path.exists(OUTPUT_DIR)):
    shutil.rmtree(OUTPUT_DIR)
os.makedirs(OUTPUT_DIR)


# run cmake and make 

CMakeCommand = "cmake"
CMakeCommand += (" -DCMAKE_CXX_FLAGS=" + "$CMAKE_CXX_FLAGS -g -O3 -fPIC -std=c++11")
CMakeCommand += " " + CURRENT_DIR+"/.."

print(CMakeCommand)

bashCommand = "cd " + BUILD_DIR
bashCommand += "&& " + CMakeCommand 
bashCommand += "&& make all -j8"
bashCommand += "&& make install/strip DESTDIR=" + OUTPUT_DIR

os.system(bashCommand)