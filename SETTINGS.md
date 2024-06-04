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

3. **Compile .ui file to .py:**
```bash
pyuic5 file_window.ui -o file_window.py
```
4. **Run Project:**
```bash
python3 main.py
```
