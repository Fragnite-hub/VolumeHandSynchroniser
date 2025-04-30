# 🖐️ Hand Tracking & Distance Estimation with MediaPipe and OpenCV

This project uses **MediaPipe** and **OpenCV** to perform real-time **hand detection** and **distance estimation** via a webcam. It visualizes hand landmarks, calculates distance between fingers and displays volume or proximity feedback interactively.

## 🚀 Features

- 📸 Real-time hand tracking with MediaPipe
- 📏 Finger-to-finger distance calculation
- 🧠 Calibrated hand distance estimation in centimeters
- 🔊 Volume bar and percentage visualization
- ⚠️ Warnings if hand is too close or too far
- 📈 FPS counter for performance monitoring



## 📦 Requirements

Make sure you have Python 3.x installed, then:

```bash
pip install opencv-python mediapipe numpy

- ▶️ How to Run
python main.py

📂 File Structure
├── main.py               # Main script for real-time detection
├── handTrackingModule.py # Class module for hand detection

📊 Distance Calculation Formula
distCM = a * lenCalc**2 + b * lenCalc + c

🧠 Credits
	•	MediaPipe for hand tracking
	•	OpenCV for video capture and visualization
