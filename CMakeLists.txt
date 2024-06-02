SET(PROJECT_NAME poseEstimation)

PROJECT(${PROJECT_NAME})

FIND_PACKAGE(OpenCV REQUIRED)
INCLUDE_DIRECTORIES(${OpenCV_INCLUDE_DIRS})
INCLUDE_DIRECTORIES("include")

# Add the OpenCV library directory (libs)
link_directories("C:/opencv/install/x64/mingw/lib")
link_directories("C:/opencv/install/x64/mingw/bin")

# Copy the image to the build directory
file(COPY "ichikanakano.jpg" DESTINATION ${CMAKE_CURRENT_BINARY_DIR})
file(COPY "fit1.jpg" DESTINATION ${CMAKE_CURRENT_BINARY_DIR})
file(COPY "fit2.jpg" DESTINATION ${CMAKE_CURRENT_BINARY_DIR})
file(COPY "fit3.jpg" DESTINATION ${CMAKE_CURRENT_BINARY_DIR})
file(COPY "pose/coco/pose_deploy_linevec.prototxt" DESTINATION ${CMAKE_CURRENT_BINARY_DIR})
file(COPY "pose/coco/pose_iter_440000.caffemodel" DESTINATION ${CMAKE_CURRENT_BINARY_DIR})

# Find the OpenCV libraries names
find_package(OpenCV REQUIRED)

# Add the executable
add_executable(testimg main.cpp)
add_executable(testvideo video.cpp)
add_executable(testload load.cpp)

# Link the OpenCV libraries to the executable
target_link_libraries(testimg ${OpenCV_LIBS})
target_link_libraries(testvideo ${OpenCV_LIBS})
target_link_libraries(testload ${OpenCV_LIBS})
