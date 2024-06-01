cmake_minimum_required(VERSION 3.10)
project(SampleProject)

# Set the C++ standard to C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Add the OpenCV include directory (headers)
include_directories("C:/opencv/install/include")

# Add the OpenCV library directory (libs)
link_directories("C:/opencv/install/x64/mingw/lib")
link_directories("C:/opencv/install/x64/mingw/bin")

# Copy the image to the build directory
file(COPY "ichikanakano.jpg" DESTINATION ${CMAKE_CURRENT_BINARY_DIR})

# Find the OpenCV libraries names
find_package(OpenCV REQUIRED)

# Add the executable
add_executable(testimg main.cpp)
add_executable(testvideo video.cpp)

# Link the OpenCV libraries to the executable
target_link_libraries(testimg ${OpenCV_LIBS})
target_link_libraries(testvideo ${OpenCV_LIBS})
