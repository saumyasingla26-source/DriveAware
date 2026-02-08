"""
Configuration File for Member 1 - Camera & Face Detection Module
All tunable parameters for the camera and detection system
"""

# ============================================================================
# CAMERA SETTINGS
# ============================================================================

# Camera device index (0 = built-in/default, 1+ = USB cameras)
CAMERA_INDEX = 0

# Video frame dimensions
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Target frames per second
TARGET_FPS = 30

# Enable auto-focus
AUTO_FOCUS_ENABLED = True

# Frame buffer size (lower = less latency, higher = more stable)
FRAME_BUFFER_SIZE = 1

# ============================================================================
# FACE DETECTION SETTINGS (MediaPipe)
# ============================================================================

# Face Detection Model Selection
# 0 = short-range (optimized for ~2 meters, good for driving)
# 1 = full-range (optimized for ~5 meters)
FACE_DETECTION_MODEL = 0

# Minimum confidence for face detection (0.0 to 1.0)
FACE_DETECTION_CONFIDENCE = 0.5

# ============================================================================
# FACE MESH SETTINGS (Detailed Landmarks)
# ============================================================================

# Enable face mesh (detailed 468 landmarks)
ENABLE_FACE_MESH = True

# Maximum number of faces to detect
MAX_FACES = 1  # Only track driver

# Refine landmarks for better accuracy
REFINE_LANDMARKS = True

# Minimum detection confidence for face mesh
FACE_MESH_DETECTION_CONFIDENCE = 0.5

# Minimum tracking confidence for face mesh
FACE_MESH_TRACKING_CONFIDENCE = 0.5

# ============================================================================
# VISUALIZATION SETTINGS
# ============================================================================

# Draw face detection bounding boxes
DRAW_BOUNDING_BOXES = True

# Draw face mesh landmarks
DRAW_FACE_MESH = True

# Draw confidence scores
DRAW_CONFIDENCE = True

# Window display name
WINDOW_NAME = "Driver Drowsiness Detection System"

# ============================================================================
# PERFORMANCE TUNING
# ============================================================================

# Use threading for frame capture (improves FPS)
USE_THREADING = False

# Skip frames for faster processing (1 = process all, 2 = skip every 2nd, etc)
FRAME_SKIP = 1  # Set to 1 for no skipping

# Maximum queue size for frame buffer
MAX_QUEUE_SIZE = 2

# ============================================================================
# FACE ROI EXTRACTION
# ============================================================================

# Margin around face when extracting ROI (as percentage)
FACE_ROI_MARGIN = 0.1  # 10% margin around detected face

# ============================================================================
# LOGGING
# ============================================================================

# Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL = "INFO"

# Enable file logging
ENABLE_FILE_LOGGING = False

# Log file path
LOG_FILE_PATH = "drowsiness_detection.log"

# ============================================================================
# INTEGRATION SETTINGS
# ============================================================================

# Pass landmarks to Member 2 (eye detection)
PASS_TO_EYE_DETECTION = True

# Trigger alarm from Member 3
ENABLE_ALARM_INTEGRATION = True

# Send telemetry/stats
ENABLE_TELEMETRY = True

# ============================================================================
# ADVANCED SETTINGS
# ============================================================================

# Number of frames for warm-up (before detection starts)
WARMUP_FRAMES = 5

# Timeout for camera initialization (seconds)
CAMERA_INIT_TIMEOUT = 5

# Enable GPU acceleration (if available)
ENABLE_GPU = True  # Set to True for faster processing on GPU systems

# ============================================================================
# LANDMARK INDICES (For Member 2)
# ============================================================================

# These are the landmark indices you need to pass to Member 2 for eye analysis
LANDMARK_INDICES = {
    # Left eye corners
    'left_eye_left': 33,
    'left_eye_right': 133,
    
    # Right eye corners
    'right_eye_left': 362,
    'right_eye_right': 263,
    
    # Eye details (for EAR calculation)
    'left_eye_top': 159,      # Upper eyelid
    'left_eye_bottom': 145,   # Lower eyelid
    'left_eye_inner': 160,    # Inner corner details
    'left_eye_outer': 33,     # Outer corner
    
    'right_eye_top': 386,     # Upper eyelid
    'right_eye_bottom': 374,  # Lower eyelid
    'right_eye_inner': 387,   # Inner corner details
    'right_eye_outer': 263,   # Outer corner
    
    # Additional useful points
    'nose_tip': 4,
    'mouth_left': 61,
    'mouth_right': 291,
    'chin': 152,
}

# ============================================================================
# CALLBACK SETTINGS (For future extensions)
# ============================================================================

# Function to call when face is detected
ON_FACE_DETECTED_CALLBACK = None

# Function to call when face is lost
ON_FACE_LOST_CALLBACK = None

# Function to call on frame processed
ON_FRAME_PROCESSED_CALLBACK = None

# ============================================================================
# Testing Configuration
# ============================================================================

# Test duration (seconds)
TEST_DURATION = 30

# Number of test frames for performance measurement
TEST_FRAME_COUNT = 30

# Enable detailed test output
VERBOSE_TESTING = True

# ============================================================================
# DEBUGGING
# ============================================================================

# Enable debug output to console
DEBUG_MODE = False

# Print frame statistics
PRINT_FRAME_STATS = False

# Track performance metrics
TRACK_PERFORMANCE = True

# ============================================================================
# USAGE EXAMPLE
# ============================================================================

"""
How to use this config file:

1. In camera_module.py:
   from config import CAMERA_INDEX, FRAME_WIDTH, etc.
   
2. In your code:
   camera = CameraCapture(
       camera_index=CAMERA_INDEX,
       frame_width=FRAME_WIDTH,
       frame_height=FRAME_HEIGHT
   )

3. To modify settings:
   - Change values in this file
   - Restart your Python script
   - Settings will automatically apply
"""

