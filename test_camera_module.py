"""
Testing Guide for Member 1 - Camera & Face Detection Module
Run this file to test individual components
"""

import cv2
import logging
from camera_module import DrownessDetectionCamera, CameraCapture, FaceDetector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_camera_access():
    """Test 1: Basic camera access"""
    print("\n" + "="*50)
    print("TEST 1: Camera Access")
    print("="*50)
    
    try:
        camera = CameraCapture(camera_index=0)
        print("✓ Camera initialized successfully")
        
        # Try to get a frame
        ret, frame = camera.get_frame()
        if ret and frame is not None:
            print(f"✓ Frame captured successfully")
            print(f"  - Frame shape: {frame.shape}")
            print(f"  - Frame dtype: {frame.dtype}")
        else:
            print("✗ Failed to capture frame")
            return False
        
        camera.release()
        print("✓ Camera released successfully")
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_face_detection():
    """Test 2: Face detection on static image"""
    print("\n" + "="*50)
    print("TEST 2: Face Detection")
    print("="*50)
    
    try:
        # Create a sample image (640x480, all blue)
        test_frame = cv2.imread("../../../path/to/real/image.jpg")  # Use real image
        
        # Or use camera frame
        camera = CameraCapture()
        ret, test_frame = camera.get_frame()
        
        if test_frame is None:
            print("✗ No frame available")
            return False
        
        detector = FaceDetector()
        print("✓ Face detector initialized")
        
        # Test face detection
        detected_frame, detections, face_found = detector.detect_face(test_frame)
        if face_found:
            print(f"✓ Face detected!")
            print(f"  - Detections: {len(detections)}")
        else:
            print("⚠ No face detected (might be due to angle/lighting)")
        
        # Test face mesh
        mesh_frame, landmarks, landmarks_found = detector.get_face_landmarks(test_frame)
        if landmarks_found:
            print(f"✓ Face landmarks detected!")
            num_landmarks = len(landmarks.multi_face_landmarks[0].landmark)
            print(f"  - Landmarks found: {num_landmarks}")
        else:
            print("⚠ No face landmarks detected")
        
        detector.release()
        camera.release()
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_real_time_detection():
    """Test 3: Real-time face detection (live camera)"""
    print("\n" + "="*50)
    print("TEST 3: Real-Time Detection (30 seconds)")
    print("="*50)
    print("Press 'q' to quit or wait 30 seconds")
    
    try:
        camera_module = DrownessDetectionCamera(camera_index=0)
        print("✓ Camera module initialized")
        
        frame_count = 0
        face_detected_count = 0
        
        import time
        start_time = time.time()
        
        while True:
            frame, face_detected, landmarks = camera_module.capture_and_detect()
            
            if frame is None:
                print("✗ Failed to capture frame")
                break
            
            frame_count += 1
            if face_detected:
                face_detected_count += 1
            
            # Add status text
            status = "FACE DETECTED" if face_detected else "NO FACE"
            color = (0, 255, 0) if face_detected else (0, 0, 255)
            cv2.putText(frame, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                       1, color, 2)
            cv2.putText(frame, f"Frame: {frame_count}", (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Display
            camera_module.display_frame(frame)
            
            # Check time and quit
            if time.time() - start_time > 30:
                print("Test completed (30 seconds reached)")
                break
            
            # Check for quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Test completed (user quit)")
                break
        
        # Results
        detection_rate = (face_detected_count / frame_count * 100) if frame_count > 0 else 0
        print(f"\n✓ Test Results:")
        print(f"  - Total frames: {frame_count}")
        print(f"  - Face detected frames: {face_detected_count}")
        print(f"  - Detection rate: {detection_rate:.1f}%")
        
        camera_module.release()
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_integration():
    """Test 4: Integration with main.py"""
    print("\n" + "="*50)
    print("TEST 4: System Integration")
    print("="*50)
    
    try:
        # Import main system
        from main import DrownessDetectionSystem
        
        system = DrownessDetectionSystem(camera_index=0)
        print("✓ System initialized")
        
        status = system.get_system_status()
        print("✓ System Status:")
        for key, value in status.items():
            print(f"  - {key}: {value}")
        
        print("✓ Integration test passed")
        system.camera_module.release()
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_performance():
    """Test 5: Performance metrics"""
    print("\n" + "="*50)
    print("TEST 5: Performance Metrics")
    print("="*50)
    
    try:
        import time
        camera_module = DrownessDetectionCamera(camera_index=0)
        
        # Warm up
        for _ in range(5):
            camera_module.capture_and_detect()
        
        # Measure time for 30 frames
        frame_count = 30
        start_time = time.time()
        
        for i in range(frame_count):
            frame, face_detected, landmarks = camera_module.capture_and_detect()
            if frame is None:
                break
        
        elapsed_time = time.time() - start_time
        fps = frame_count / elapsed_time
        ms_per_frame = (elapsed_time / frame_count) * 1000
        
        print(f"✓ Performance Results:")
        print(f"  - Total time: {elapsed_time:.2f}s")
        print(f"  - Frames processed: {frame_count}")
        print(f"  - FPS: {fps:.1f}")
        print(f"  - Time per frame: {ms_per_frame:.1f}ms")
        
        camera_module.release()
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def run_all_tests():
    """Run all tests in sequence"""
    print("\n" + "="*60)
    print("DRIVER DROWSINESS DETECTION - MEMBER 1 TEST SUITE")
    print("="*60)
    
    results = {}
    
    # Test 1: Camera Access
    results['Camera Access'] = test_camera_access()
    
    # Test 2: Face Detection
    results['Face Detection'] = test_face_detection()
    
    # Test 3: Real-Time Detection
    results['Real-Time Detection'] = test_real_time_detection()
    
    # Test 4: Integration
    results['System Integration'] = test_integration()
    
    # Test 5: Performance
    results['Performance'] = test_performance()
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, result in results.items():
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    total_tests = len(results)
    passed_tests = sum(1 for r in results.values() if r)
    
    print(f"\nTotal: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("\n✓ ALL TESTS PASSED!")
    else:
        print(f"\n⚠ {total_tests - passed_tests} test(s) failed")


if __name__ == "__main__":
    """
    Usage:
    python test_camera_module.py
    
    This will run all tests in sequence. Each test will provide feedback.
    """
    run_all_tests()
