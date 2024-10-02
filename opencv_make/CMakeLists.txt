cmake_minimum_required(VERSION 3.28.3)
project(FLIPimage)
find_package(OpenCV REQUIRED)
add_executable(flip_image opencv.cpp)
target_link_libraries(flip_image ${OpenCV_LIBS})

