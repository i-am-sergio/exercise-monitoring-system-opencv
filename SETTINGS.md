## Project Settings 

1. **Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
```

2. **Install Dependencies:**
```bash
pip install PyQt5
pip install opencv-python
pip install tensorflow
pip install pytube
pip install moviepy
```

3. **Download test videos:**
```bash
python3 utils/download_vid.py # From root project
```

4. **Run Project:**
```bash
python3 main.py # From root project
```

- **Extra: For Compile .ui file to .py:**
```bash
pyuic5 file_window.ui -o file_window.py
```