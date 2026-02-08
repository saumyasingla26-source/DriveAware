# DriveAware
Driver Drowsiness Detection System

### Step 1: Install Python Packages 
```bash
pip install opencv-python mediapipe
```

**What this does**: Installs OpenCV, MediaPipe, and NumPy

### Step 2: Test Your Camera 
```bash
python test_camera_module.py
```

**What to expect**: 
- Camera Access test ✓
- Face Detection test ✓
- Real-time detection for 30 seconds
- Performance metrics

**Troubleshooting**: If camera fails:
1. Check if camera is connected
2. Grant camera permissions (Windows might ask)
3. Try closing other apps using camera (Zoom, Teams, etc.)

### Step 3: Run the Main System 
```bash
python main.py
```
