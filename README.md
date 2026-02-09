# Arm Fitness Tracker

Arm Fitness Coach is a real-time AI-powered application that uses MediaPipe and OpenCV to track and analyze your arm workouts. The app provides live feedback on your form, counts your repetitions, and saves your progress to a local database.

## Features
Real-time Pose Estimation: Uses MediaPipe to track joints and calculate precise joint angles.

Exercise Detection: Specifically optimized for:

- Bicep Curls: Tracks elbow flexion and ensures full range of motion.

- Lateral Raises: Monitors shoulder height and lateral movement.

- Overhead Press: Detects vertical movement and grip width.

Intelligent Feedback Mechanism:

- Audio prompts for "Perfect" reps, "Bad form," or "Try again".

- Visual cues on screen showing current state (Curling, Up, Lowering) and angles.

Progress Tracking: Automatically saves your workout history (exercise name, reps, and timestamp) in a SQLite database.

Interactive UI: Built with Streamlit for a clean, easy-to-use dashboard.

## Technology used
- Python: Main programming language.

- MediaPipe: For high-fidelity pose tracking.

- Streamlit: For the web interface and real-time video streaming.

- OpenCV: For image processing.

- Pygame: Handles real-time audio feedback.

- SQLite: Local data storage for workout history.

## Installation and usage

#### Prerequisites: 
- Python 3.11.5 
- Mediapipe
- OpenCV
- Streamlit

#### Steps to run
1. Clone this repository
<pre>git clone https://github.com/buivan19/Arm-fitness-tracker.git</pre>
2. Install dependencies
<pre>pip install -r requirements.txt</pre>
3. Run the app
<pre>streamlit run app.py</pre>

##Result
This is a demo of our project: https://drive.google.com/drive/folders/1CVXR33rO-9UhJRl3fOpb4fWJv9LBt-kk
