Project Title

Gesture-Based Human–Computer Interaction System

Overview

This project implements hand gesture recognition using MediaPipe and OpenCV to control computer operations without physical input devices. It provides brightness control, swipe-based navigation, scrolling, clicking, double-clicking, and drag-and-drop interactions. A Tkinter interface is used to launch different gesture modes.

File Structure
GESTURE_CONTROL/
│
├── src/
│   ├── gestures/
│   │   ├── brightness.py      # Controls screen brightness based on finger distance
│   │   ├── control.py         # Handles swipe, tap, drag, and scrolling gestures
│   │
│   ├── main.py                # Tkinter launcher interface
│
├── .gitignore
└── README.md

Requirements

Install the required libraries:

pip install opencv-python mediapipe numpy pyautogui screen-brightness-control

How to Run

Launch the interface:

python src/main.py


From the UI:

Select Brightness Control to adjust brightness using thumb-index distance.

Select Window Scrolling & Tapping to perform swipes, clicks, and drag gestures.

Gesture Summary

Pinch → Click

Double pinch → Double Click

Pinch and hold → Drag

Swipe left/right → Tab navigation

Swipe up/down → Scrolling

Thumb-index distance → Brightness control

Notes

Keep your hand in good lighting.

Ensure the camera is unobstructed.

Press Q in any gesture window to exit.