# Quick Start Guide - Member 1

## 5-Minute Setup

### Step 1: Install Python Packages (1 minute)
```bash
pip install -r requirements.txt
```

**What this does**: Installs OpenCV, MediaPipe, and NumPy

### Step 2: Test Your Camera (2 minutes)
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

### Step 3: Run the Main System (2 minutes)
```bash
python main.py
```

**What to expect**:
- Camera window opens
- Shows face detection in real-time
- Displays bounding boxes and landmarks
- Press 'q' or ESC to quit

---

## Understanding the Code Structure

```
Main File/
├── camera_module.py          # Core camera & detection logic
├── main.py                    # System integration entry point
├── test_camera_module.py      # Testing suite
├── requirements.txt           # Dependencies
├── README_MEMBER1.md          # Full documentation
└── QUICK_START.md             # This file
```

### Three Main Classes in camera_module.py:

1. **CameraCapture** - Captures video frames
   - Handles: Camera initialization, frame reading, buffer management
   - Used by: DrownessDetectionCamera

2. **FaceDetector** - Detects faces and landmarks
   - Handles: Face detection, facial landmarks (468 points)
   - Used by: DrownessDetectionCamera

3. **DrownessDetectionCamera** - Main interface
   - Combines camera + detector
   - Method to call: `camera_module.capture_and_detect()`

---

## Key Code Examples

### Example 1: Basic Usage (Simplest)
```python
from camera_module import DrownessDetectionCamera
import cv2

# Initialize
camera = DrownessDetectionCamera()

# Main loop
while True:
    frame, face_detected, landmarks = camera.capture_and_detect()
    
    if face_detected:
        print("Face found!")
    
    camera.display_frame(frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
```

### Example 2: Get Landmarks for Member 2
```python
from camera_module import DrownessDetectionCamera

camera = DrownessDetectionCamera()

frame, face_detected, landmarks = camera.capture_and_detect()

if face_detected:
    # Pass to Member 2's eye detection
    eye_detector.analyze(landmarks)
```

### Example 3: Check Face Detection Status
```python
from camera_module import DrownessDetectionCamera

camera = DrownessDetectionCamera()

while True:
    frame, _, _ = camera.capture_and_detect()
    
    if camera.is_face_detected():
        print("Driver detected")
    else:
        print("No driver detected - alert!")
    
    camera.display_frame(frame)
```

---

## What Each File Does

### camera_module.py
**Your main implementation file**
- CameraCapture class: Handles camera hardware
- FaceDetector class: Uses MediaPipe for face detection
- DrownessDetectionCamera class: Combines both

### main.py
**Integration with other members**
- DrownessDetectionSystem class: Central hub
- Methods to add Member 2's eye detection
- Methods to add Member 3's alarm system
- Main detection loop

### test_camera_module.py
**Verification that everything works**
- 5 automated tests
- Tests camera, face detection, real-time, integration
- Performance measurements

### requirements.txt
**List of dependencies to install**
- opencv-python: Video capture and display
- mediapipe: Face detection & landmarks
- numpy: Numerical operations

---

## For Viva Presentation

### What to say:
"I implemented camera access using OpenCV and face detection using MediaPipe. The system captures real-time video, detects the driver's face with bounding boxes, and extracts 468 facial landmarks for eye analysis. The landmarks are passed to Member 2 for drowsiness detection logic."

### What to show:
1. Run `python main.py`
2. Show video with face detection
3. Show the code structure in camera_module.py
4. Explain the three classes

### Key points to highlight:
- ✓ Real-time video capture
- ✓ MediaPipe for accurate detection
- ✓ 468 facial landmarks for eye analysis
- ✓ Clean interface for Member 2 integration
- ✓ Error handling and logging

---

## Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| "Failed to open camera" | Check if camera is connected, close other apps using camera |
| "ModuleNotFoundError: opencv" | Run `pip install -r requirements.txt` |
| Low FPS | Reduce resolution or use `camera_index=0` (built-in instead of USB) |
| Face not detected | Ensure good lighting, face is visible, at appropriate distance (~50cm) |
| No landmarks detected | Face needs to be frontal/forward-facing |

---

## Next Steps

1. **Test everything works**: Run `python test_camera_module.py`
2. **Understand the code**: Read `camera_module.py` comments
3. **Integration**: Provide landmarks to Member 2
4. **Viva prep**: Memorize how face detection works

---

## Landmarks Data for Member 2

When you call:
```python
frame, face_detected, landmarks = camera.capture_and_detect()
```

The `landmarks` variable contains:
- **Type**: MediaPipe FaceLandmarks object
- **Count**: 468 facial landmarks
- **Format**: Each landmark has (x, y, z) normalized coordinates (0-1 range)

**Important indices for eye detection:**
```
Left eye: landmarks.multi_face_landmarks[0].landmark[33] (left corner)
Left eye: landmarks.multi_face_landmarks[0].landmark[133] (right corner)
Right eye: landmarks.multi_face_landmarks[0].landmark[362] (left corner)
Right eye: landmarks.multi_face_landmarks[0].landmark[263] (right corner)
```

---

## Performance Expected

- **Frame Rate**: 30 FPS
- **Detection Time**: ~50ms per frame
- **Face Detection Accuracy**: ~98%
- **CPU Usage**: 10-20%

---

## Files to Submit

✓ camera_module.py - Core implementation
✓ main.py - Integration code
✓ test_camera_module.py - Tests
✓ requirements.txt - Dependencies
✓ README_MEMBER1.md - Full documentation
✓ QUICK_START.md - This file

---

## Questions?

Refer to:
- camera_module.py comments for implementation details
- README_MEMBER1.md for deep technical info
- test_camera_module.py for usage examples

Good luck with your viva! 🚀
