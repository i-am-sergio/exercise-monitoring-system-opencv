# exercise-monitoring-system-opencv

[**Click Here for project settings**](SETTINGS.md)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
<!-- ![CMake](https://img.shields.io/badge/CMake-%23008FBA.svg?style=for-the-badge&logo=cmake&logoColor=white) -->
<!-- ![C++](https://img.shields.io/badge/c++-%2300599C.svg?style=for-the-badge&logo=c%2B%2B&logoColor=white) -->

## Description

This project is an exercise monitoring system that uses OpenCV for video capture and processing, NumPy for data processing, and is implemented in both C++ and Python. The system captures video from a camera, processes the frames to monitor exercises, and displays the results in real-time.

## Requirements

1. **Real-Time Video Capture:** The system should be able to capture video from a camera in real-time to monitor exercises as they are being performed.

2. **Exercise Detection:** The system should be capable of detecting and identifying specific exercises or movements within the captured video stream.

3. **On-Screen Visualization:** Detected exercises or movements should be visually displayed in real-time on the screen, providing immediate feedback to the user.

4. **Multi-Platform Support:** The software should be compatible with multiple platforms, including Windows, Linux, and macOS, to ensure accessibility for a wide range of users.

5. **Modular Architecture:** The system's architecture should be modular, allowing for easy extension and customization of exercise detection algorithms and integration of additional features in the future.


## Structure

4. **Project Structure:**
```
exercise-monitoring-system/
│
├── main.py                 # Archivo principal para ejecutar la aplicación
├── requirements.txt        # Dependencias del proyecto
│
├── resources/              # Archivos de recursos como imágenes, iconos, etc.
│   ├── icons ...
│   ├── images ...
│   └── stylesheets ...
│
├── ui/                     # Interfaces de usuario
│   ├── main_window.py      # Ventana principal de la aplicación
│   ├── exercise_window.py  # Ventana de seguimiento de ejercicios
│   └── __init__.py
│
├── core/                   # Funcionalidades principales de la aplicación
│   ├── exercise.py         # Lógica relacionada con los ejercicios
│   ├── routine.py          # Gestión de las rutinas de ejercicios
│   └── __init__.py
│
├── detection/              # Módulos relacionados con la detección y seguimiento de poses
│   ├── pose_estimation.py  # Lógica de estimación de poses utilizando OpenCV y el modelo MobileNet
│   ├── camera.py           # Manejo de la cámara
│   └── __init__.py
│
└── utils/                  # Utilidades y funciones auxiliares
    ├── helpers.py          # Funciones de ayuda generales
    └── __init__.py


```

### Tecnologies and tools
- Python >= 3.10
- OpenCV
- NumPy
- MinGW (for C++ compilation)
- GCC
- CMake
- Ninja (optional, for generating build files with CMake)
