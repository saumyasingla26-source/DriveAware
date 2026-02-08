"""
Camera & Face Detection Module (OpenCV Haar Cascade Version)
Handles real-time video capture and face detection for driver drowsiness detection system
Member 1: Camera & Face Detection Module

Note: Uses OpenCV Haar Cascade (alternative to MediaPipe for compatibility)
"""

import cv2
import numpy as np
from threading import Thread
from queue import Queue
from typing import Tuple, List, Optional
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FaceDetector:
    """
    Detects faces in video frames using OpenCV Haar Cascade
    Provides face bounding boxes for further analysis
    """
    
    def __init__(self):
        """Initialize OpenCV Haar Cascade Face Detector"""
        # Load Haar Cascade classifier for face detection
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
        # Load eye cascade for additional validation
        eye_cascade_path = cv2.data.haarcascades + 'haarcascade_eye.xml'
        self.eye_cascade = cv2.CascadeClassifier(eye_cascade_path)
        
        if self.face_cascade.empty():
            raise RuntimeError("Failed to load Haar Cascade classifier")
        
        logger.info("Face Detection module initialized successfully using Haar Cascade")
    
    def detect_face(self, frame: np.ndarray) -> Tuple[np.ndarray, Optional[list], bool]:
        """
        Detect faces in the given frame using Haar Cascade
        
        Args:
            frame: Input video frame (BGR format from OpenCV)
            
        Returns:
            Tuple containing:
            - Processed frame with face detection visualization
            - List of detection results (bounding boxes)
            - Boolean indicating if face was detected
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Multi-scale detection for better accuracy
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        frame_bgr = frame.copy()
        face_detected = False
        detections = None
        
        if len(faces) > 0:
            face_detected = True
            # Keep only the largest face (driver)
            faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)[:1]
            detections = faces
            
            # Draw bounding box
            for (x, y, w, h) in faces:
                cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame_bgr, "Face", (x, y - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return frame_bgr, detections, face_detected
    
    def get_face_landmarks(self, frame: np.ndarray, face_region: Optional[np.ndarray] = None) \
            -> Tuple[np.ndarray, Optional[dict], bool]:
        """
        Detect eyes in face region and create landmark data structure
        Compatible with the interface expected by Member 2
        
        Args:
            frame: Input video frame (BGR format)
            face_region: Face ROI for eye detection
            
        Returns:
            Tuple containing:
            - Processed frame with landmarks
            - Facial landmark results (dictionary format)
            - Boolean indicating if landmarks were detected
        """
        frame_bgr = frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        landmarks_detected = False
        landmarks_data = None
        
        if face_region is not None:
            # Detect eyes in the face region
            eyes = self.eye_cascade.detectMultiScale(face_region)
            
            if len(eyes) >= 2:
                landmarks_detected = True
                
                # Create landmark data structure compatible with Member 2
                landmarks_data = {
                    'eyes': eyes,
                    'eye_count': len(eyes),
                    'face_region': face_region
                }
                
                # Draw eye regions
                for (x, y, w, h) in eyes:
                    cv2.rectangle(face_region, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
        return frame_bgr, landmarks_data, landmarks_detected
    
    def extract_face_roi(self, frame: np.ndarray, detection: tuple) -> Optional[np.ndarray]:
        """
        Extract Region of Interest (ROI) containing the detected face
        
        Args:
            frame: Input video frame
            detection: Tuple of (x, y, w, h) from Haar Cascade
            
        Returns:
            Cropped face ROI or None if extraction fails
        """
        if detection is None or len(detection) < 4:
            return None
        
        x, y, w, h = detection
        h_frame, w_frame, c = frame.shape
        
        # Add margin around face
        margin = int(0.1 * w)
        x_min = max(0, x - margin)
        y_min = max(0, y - margin)
        x_max = min(w_frame, x + w + margin)
        y_max = min(h_frame, y + h + margin)
        
        try:
            face_roi = frame[y_min:y_max, x_min:x_max]
            return face_roi
        except:
            return None
    
    def release(self):
        """Clean up resources"""
        logger.info("Face Detection resources released")


class CameraCapture:
    """
    Handles real-time camera capture and frame processing
    Supports both USB cameras and built-in webcams
    """
    
    def __init__(self, camera_index: int = 0, frame_width: int = 640, frame_height: int = 480):
        """
        Initialize camera capture
        
        Args:
            camera_index: Index of camera device (0 for default/built-in)
            frame_width: Width of captured frames
            frame_height: Height of captured frames
        """
        self.camera_index = camera_index
        self.frame_width = frame_width
        self.frame_height = frame_height
        
        self.cap = cv2.VideoCapture(camera_index)
        
        # Set camera properties for better performance
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        if not self.cap.isOpened():
            raise RuntimeError(f"Failed to open camera at index {camera_index}")
        
        self.is_running = False
        self.frame_queue = Queue(maxsize=2)
        self.current_frame = None
        
        logger.info(f"Camera initialized successfully at index {camera_index}")
    
    def get_frame(self) -> Tuple[bool, Optional[np.ndarray]]:
        """
        Get the most recent captured frame
        
        Returns:
            Tuple of (success, frame)
        """
        ret, frame = self.cap.read()
        if ret:
            self.current_frame = frame
        return ret, frame
    
    def release(self):
        """Release camera resources"""
        self.is_running = False
        if self.cap is not None:
            self.cap.release()
        logger.info("Camera released")


class DrownessDetectionCamera:
    """
    Main camera module that integrates face detection with video capture
    Provides interface for other modules to access face data
    """
    
    def __init__(self, camera_index: int = 0):
        """
        Initialize the complete camera and detection system
        
        Args:
            camera_index: Index of camera to use (0 for default)
        """
        self.camera = CameraCapture(camera_index=camera_index)
        self.face_detector = FaceDetector()
        self.face_landmarks_data = None
        self.face_detected = False
        self.last_face_region = None
        
        logger.info("Drowsiness Detection Camera module initialized")
    
    def capture_and_detect(self) -> Tuple[np.ndarray, bool, Optional[dict]]:
        """
        Capture frame and perform face detection
        
        Returns:
            Tuple containing:
            - Frame with detection visualizations
            - Boolean indicating if face was detected
            - Facial landmark data for eye analysis
        """
        ret, frame = self.camera.get_frame()
        
        if not ret:
            logger.error("Failed to capture frame")
            return None, False, None
        
        # Detect face
        frame_with_detection, detections, face_detected = self.face_detector.detect_face(frame)
        
        # Extract face ROI and detect landmarks
        landmarks_data = None
        if face_detected and detections is not None and len(detections) > 0:
            # Extract face region
            face_roi = self.face_detector.extract_face_roi(frame, detections[0])
            self.last_face_region = face_roi
            
            # Get landmarks (eyes) from face region
            frame_with_landmarks, landmarks_data, landmarks_detected = \
                self.face_detector.get_face_landmarks(frame_with_detection, face_roi)
            
            # Use frame with landmarks visualization
            annotated_frame = frame_with_landmarks
            self.face_detected = landmarks_detected if landmarks_data else face_detected
            self.face_landmarks_data = landmarks_data
        else:
            self.face_detected = False
            self.face_landmarks_data = None
            annotated_frame = frame_with_detection
        
        return annotated_frame, self.face_detected, self.face_landmarks_data
    
    def get_face_landmarks(self) -> Optional[dict]:
        """
        Get the latest face landmarks data
        
        Returns:
            Facial landmark data or None
        """
        return self.face_landmarks_data
    
    def is_face_detected(self) -> bool:
        """
        Check if face is currently detected
        
        Returns:
            Boolean indicating face detection status
        """
        return self.face_detected
    
    def display_frame(self, frame: np.ndarray, window_name: str = "Driver Drowsiness Detection"):
        """
        Display the frame in a window
        
        Args:
            frame: Frame to display
            window_name: Name of the display window
        """
        if frame is not None:
            cv2.imshow(window_name, frame)
    
    def release(self):
        """Release all resources"""
        self.camera.release()
        self.face_detector.release()
        cv2.destroyAllWindows()
        logger.info("All camera resources released")


# Example usage and testing
if __name__ == "__main__":
    try:
        # Initialize camera module
        camera_module = DrownessDetectionCamera(camera_index=0)
        
        print("Camera module initialized. Press 'q' to quit.")
        
        while True:
            # Capture and detect
            frame, face_detected, landmarks = camera_module.capture_and_detect()
            
            if frame is None:
                break
            
            # Display detection status
            status = "FACE DETECTED" if face_detected else "NO FACE"
            cv2.putText(frame, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                       1, (0, 255, 0) if face_detected else (0, 0, 255), 2)
            
            # Display frame
            camera_module.display_frame(frame)
            
            # Press 'q' to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Cleanup
        camera_module.release()
        print("Camera module closed successfully")
        
    except Exception as e:
        print(f"Error: {e}")
        logger.exception("Exception occurred in camera module")
