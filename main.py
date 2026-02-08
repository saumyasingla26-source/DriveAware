"""
Driver Drowsiness Detection System - Main Integration
Member 1: Camera & Face Detection Module Integration
"""

import cv2
import sys
import logging
from camera_module import DrownessDetectionCamera

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DrownessDetectionSystem:
    """
    Main system that integrates all modules
    Member 1 (Camera): Captures video and detects faces
    Member 2 (Eye Analysis): Analyzes eyes and determines drowsiness
    Member 3 (Alarm & UI): Displays alerts and UI
    """
    
    def __init__(self, camera_index: int = 0):
        """
        Initialize the complete drowsiness detection system
        
        Args:
            camera_index: Index of camera to use
        """
        logger.info("Initializing Driver Drowsiness Detection System...")
        
        # Member 1: Initialize camera and face detection
        self.camera_module = DrownessDetectionCamera(camera_index=camera_index)
        
        # Placeholders for other modules (to be integrated by other members)
        self.eye_detector = None  # Member 2: Eye detection module
        self.alarm_system = None  # Member 3: Alarm and UI module
        
        # System state
        self.is_running = False
        self.frame_count = 0
        
        logger.info("System initialization complete")
    
    def integrate_eye_detection_module(self, eye_detector):
        """
        Integrate eye detection module from Member 2
        
        Args:
            eye_detector: Eye detection module instance
        """
        self.eye_detector = eye_detector
        logger.info("Eye detection module integrated")
    
    def integrate_alarm_module(self, alarm_system):
        """
        Integrate alarm and UI module from Member 3
        
        Args:
            alarm_system: Alarm system module instance
        """
        self.alarm_system = alarm_system
        logger.info("Alarm system module integrated")
    
    def process_frame(self, frame):
        """
        Process frame through the detection pipeline
        
        Args:
            frame: Input frame to process
            
        Returns:
            Processed frame and detection results
        """
        # Member 1: Face detection
        face_detected = False
        landmarks = None
        
        if frame is not None:
            # Get face landmarks from camera module
            landmarks = self.camera_module.get_face_landmarks()
            face_detected = self.camera_module.is_face_detected()
            
            # Member 2: Eye analysis (to be integrated)
            drowsiness_status = None
            if self.eye_detector and landmarks:
                try:
                    drowsiness_status = self.eye_detector.analyze_eyes(landmarks)
                except Exception as e:
                    logger.warning(f"Eye detection error: {e}")
            
            # Member 3: Alarm trigger (to be integrated)
            if self.alarm_system and drowsiness_status is not None:
                try:
                    if drowsiness_status:  # If drowsiness detected
                        self.alarm_system.trigger_alert()
                except Exception as e:
                    logger.warning(f"Alarm system error: {e}")
        
        return face_detected, landmarks
    
    def start_detection(self):
        """Start the detection loop"""
        self.is_running = True
        logger.info("Starting drowsiness detection...")
        
        try:
            while self.is_running:
                # Member 1: Capture and detect faces
                frame, face_detected, landmarks = self.camera_module.capture_and_detect()
                
                if frame is None:
                    logger.error("Failed to capture frame")
                    break
                
                self.frame_count += 1
                
                # Process frame through pipeline
                self.process_frame(frame)
                
                # Display frame
                self.camera_module.display_frame(frame)
                
                # Check for quit command
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == 27:  # 'q' or ESC
                    logger.info("Quit command received")
                    break
        
        except KeyboardInterrupt:
            logger.info("Detection interrupted by user")
        except Exception as e:
            logger.error(f"Error in detection loop: {e}")
        finally:
            self.stop_detection()
    
    def stop_detection(self):
        """Stop the detection loop and cleanup resources"""
        self.is_running = False
        logger.info(f"Detection stopped. Processed {self.frame_count} frames")
        
        # Cleanup
        self.camera_module.release()
        
        if self.alarm_system:
            try:
                self.alarm_system.shutdown()
            except:
                pass
        
        cv2.destroyAllWindows()
        logger.info("System shutdown complete")
    
    def get_camera_module(self):
        """
        Get the camera module for direct access
        Useful for testing and integration
        
        Returns:
            DrownessDetectionCamera instance
        """
        return self.camera_module
    
    def get_system_status(self):
        """
        Get current system status
        
        Returns:
            Dictionary with system information
        """
        return {
            'running': self.is_running,
            'frames_processed': self.frame_count,
            'face_detected': self.camera_module.is_face_detected(),
            'eye_detector_integrated': self.eye_detector is not None,
            'alarm_system_integrated': self.alarm_system is not None
        }


def main():
    """Main entry point for the system"""
    
    # Create system instance
    system = DrownessDetectionSystem(camera_index=0)
    
    # Note: Members 2 and 3 will integrate their modules here like:
    # system.integrate_eye_detection_module(eye_detector_instance)
    # system.integrate_alarm_module(alarm_system_instance)
    
    # Start detection
    system.start_detection()


if __name__ == "__main__":
    main()
