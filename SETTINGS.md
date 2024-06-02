# Opencv projects configurations

1. **Download opencv**: `Source code` for windows. [**Click Here**](https://github.com/opencv/opencv/releases/tag/4.9.0)
2. **Unzip** source code
3. **Compile** Opencv with Cmake in a build folder named `opencv`:
    ```powershell
    mkdir opencv
    ```
    - Use cmake gui for generate makefikes: [**Step 3 here**](https://medium.com/csmadeeasy/opencv-c-installation-on-windows-with-mingw-c0fc1499f39)
4. **Move Folder**: Put `opencv` folder in C root directory `C:\`
5. **Add this Environment variable to path:** `C:\opencv\install\x64\mingw\bin`

## 1. Configure `.vscode/c_cpp_properties.json`:
```json
{
    "configurations": [
        {
            "name": "Win32",
            "includePath": [
                "${default}",
                "C:\\opencv\\install\\include"
            ],
            "defines": [
                "_DEBUG",
                "UNICODE",
                "_UNICODE"
            ],
            "compilerPath": "C:\\Users\\sergi\\scoop\\apps\\mingw\\current\\bin\\gcc.exe",
            "cStandard": "c17",
            "cppStandard": "gnu++17",
            "intelliSenseMode": "windows-gcc-x64"
        }
    ],
    "version": 4
}
```

## 2. Compile for Windows

2. **Compile with g++**
    ```powershell
    g++ -g -std=c++17 `
    -IC:\opencv\install\include `
    -LC:\opencv\install\x64\mingw\lib `
    -LC:\opencv\install\x64\mingw\bin `
    main.cpp `
    -lopencv_core490 -lopencv_highgui490 -lopencv_imgcodecs490 -lopencv_videoio490 `
    -o main.exe
    ```

1. **Compile with CMake**
    - Create a `CMakeLists.txt`:
        ```cmake
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
        ```

    - Create build directory in root project:
        ```powershell
        mkdir build && cd build
        ```
    - In build directory project, for create makefiles run:
        ```powershell
        cmake -G Ninja -DOpenCV_DIR="C:/opencv/install" ..
        ```
    - Compile project running:
        ```powershell
        cmake --build .
        ```