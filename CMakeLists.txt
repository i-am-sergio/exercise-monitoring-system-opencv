cmake_minimum_required(VERSION 3.17)
project(TFLiteMoveNet)

set(CMAKE_CXX_STANDARD 17)

# Incluir los directorios de encabezados
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../tflite-dist/include/)

# Encontrar OpenCV
find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})

file(COPY "model.tflite" DESTINATION ${CMAKE_CURRENT_BINARY_DIR})
file(COPY "sentadilla.mp4" DESTINATION ${CMAKE_CURRENT_BINARY_DIR})

# Agregar la biblioteca compartida tensorflowlite
add_library(tensorflowlite SHARED IMPORTED)
set_property(TARGET tensorflowlite PROPERTY IMPORTED_LOCATION ${CMAKE_CURRENT_SOURCE_DIR}/../tflite-dist/libs/linux_x64/libtensorflowlite.so)

# Crear el ejecutable
add_executable(TFLiteMoveNet movenet.cpp)

# Especificar los directorios de búsqueda de bibliotecas
link_directories(${CMAKE_CURRENT_SOURCE_DIR}/../tflite-dist/libs/linux_x64)

# Enlazar el ejecutable con la biblioteca tensorflowlite y OpenCV
target_link_libraries(TFLiteMoveNet ${OpenCV_LIBS} tensorflowlite pthread dl m)
