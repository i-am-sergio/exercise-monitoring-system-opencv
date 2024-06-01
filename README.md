# exercise-monitoring-system-opencv

[**Click Here for project settings**](SETTINGS.md)

## Description

This project is an exercise monitoring system that uses OpenCV for video capture and processing, NumPy for data processing, and is implemented in both C++ and Python. The system captures video from a camera, processes the frames to monitor exercises, and displays the results in real-time.

## Requirements

1. **Real-Time Video Capture:** The system should be able to capture video from a camera in real-time to monitor exercises as they are being performed.

2. **Exercise Detection:** The system should be capable of detecting and identifying specific exercises or movements within the captured video stream.

3. **On-Screen Visualization:** Detected exercises or movements should be visually displayed in real-time on the screen, providing immediate feedback to the user.

4. **Multi-Platform Support:** The software should be compatible with multiple platforms, including Windows, Linux, and macOS, to ensure accessibility for a wide range of users.

5. **Modular Architecture:** The system's architecture should be modular, allowing for easy extension and customization of exercise detection algorithms and integration of additional features in the future.


## Structure

```
exercise-monitoring-system/
│
├── main.py
├── modules/
│   ├── video_capture.py
│   ├── exercise_detection.py
│   ├── visualization.py
│   └── utils.py
│
├── data/
│   ├── detection_model.pkl
│   └── ...
│
├── tests/
│   ├── test_video_capture.py
│   ├── test_exercise_detection.py
│   ├── test_visualization.py
│   └── ...
│
├── requirements.txt
└── README.md
└── SETTINGS.md
```

### Tecnologies and tools
- Python >= 3.10
- OpenCV
- NumPy
- MinGW (for C++ compilation)
- GCC
- CMake
- Ninja (optional, for generating build files with CMake)
