# Real-Time Drowsiness Monitoring System

## Project Description
This project detects driver drowsiness in real time using a webcam.  
It monitors the driver's eyes and calculates the Eye Aspect Ratio (EAR).  
If the eyes remain closed for a few seconds, the system identifies drowsiness, triggers an alarm, and stores the alert in a local database.

## Features
- Real-time camera access
- Face and eye detection
- Eye Aspect Ratio (EAR) calculation
- Drowsiness detection logic
- Alarm alert system
- Local database to store alert records

## Technologies Used
- Python
- OpenCV
- MediaPipe
- NumPy
- SQLite (Local Database)
- Kivy

## Database
The system stores:
- Date of alert
- Time of alert
- Duration of eye closure
- Status of detection

The database used is SQLite and is stored locally on the device.

## How to Run

1. Clone the repository:
   git clone <repository-link>

2. Go to the project folder:
   cd <project-folder>

3. Install required libraries:
   pip install -r requirements.txt

4. Run the program:
   python main.py

## APK Generation (Optional)
To build the Android APK using Buildozer:
   buildozer android debug

## Team Contribution
This project was developed as part of academic coursework.  
All team members contributed equally to development, database integration, and testing
