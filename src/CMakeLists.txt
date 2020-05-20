cmake_minimum_required(VERSION 3.10)

include_directories(
        ${PROJECT_SOURCE_DIR}/3rdparty/rapidjson/include
        ${PROJECT_SOURCE_DIR}/3rdparty/eigen/include
        ${PROJECT_SOURCE_DIR}/3rdparty/spdlog/include
)

link_directories(

)

link_libraries(

)

# General source files
file(GLOB SOURCE_FILES MyMath.cpp)
set(HEADERS MyMath.h)
include_directories (
        ./
        ${PROJECT_SOURCE_DIR}/3rdparty/rapidjson/include
)

link_directories (
)

link_libraries (

)

set(LIBRARY_NAME "fiftyK")
add_library(${LIBRARY_NAME} ${SOURCE_FILES})

# install library 库的安装路径
install(TARGETS ${LIBRARY_NAME} DESTINATION "lib")
install(FILES ${HEADERS} DESTINATION "include")