# exercise-monitoring-system-opencv

[**Click Here for project settings**](SETTINGS.md)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)
![Qt](https://img.shields.io/badge/Qt-%23217346.svg?style=for-the-badge&logo=Qt&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=for-the-badge&logo=TensorFlow&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
<!-- ![C++](https://img.shields.io/badge/c++-%2300599C.svg?style=for-the-badge&logo=c%2B%2B&logoColor=white) -->
<!-- ![CMake](https://img.shields.io/badge/CMake-%23008FBA.svg?style=for-the-badge&logo=cmake&logoColor=white) -->

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
├── controllers
│   ├── abdominal_controller.py
│   ├── biceps_controller.py
│   ├── elevaciones_controller.py
│   ├── estocada_controller.py
│   ├── jumps_controller.py
│   ├── main_controller.py
│   ├── plancha_controller.py
│   ├── puente_controller.py
│   └── sentadilla_controller.py
|
├── detection
│   ├── abdominal.mp4
│   ├── bicep.mp4
│   ├── estocada.mp4
│   ├── flexion.mp4
│   ├── jumping_jack.mp4
│   ├── movenet_thunder.py
│   └── sentadilla.mp4
|
├── resources
│   ├── 1_sentadilla_btn.png
│   ├── 2_lunge_btn.png
│   ├── 3_biceps_btn.png
│   ├── 4_jumping_jacks_btn.png
│   ├── 5_flexion_btn.png
│   ├── 6_abdominal_btn.png
│   ├── img
│   │   ├── 1_sentadilla.png
│   │   ├── 2_stocada.png
│   │   ├── 3_biceps.png
│   │   ├── 4_puente.png
│   │   ├── 5_elevaciones.png
│   │   └── 6_plancha.png
│   └── models
│       └── model.tflite
|
├── ui
│   └── main_window.ui
|
├── utils
│   └── download_vid.py
|
├── views
|   └── main_window.py
|
├── main.py
├── test.py
├── README.md
├── SETTINGS.md
└── requirements.txt


```

### Tecnologies and tools
- Python >= 3.10
- OpenCV
- Tensorflow
- NumPy
- MinGW (for C++ compilation)
- GCC
- CMake
- Ninja (optional, for generating build files with CMake)
