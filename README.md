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

## Result
This is a demo of our project: https://drive.google.com/drive/folders/1CVXR33rO-9UhJRl3fOpb4fWJv9LBt-kk
#### App layout
<img width="338" height="172" alt="01" src="https://github.com/user-attachments/assets/699a4ce9-4e8c-4aec-bef9-59498df0fa37" />
<img width="368" height="181" alt="02" src="https://github.com/user-attachments/assets/5e3f61af-79b4-47ea-a7fd-7fbe8b201b4c" />
<img width="356" height="178" alt="03" src="https://github.com/user-attachments/assets/99cadd95-e68b-462a-a12b-e7c0582426ee" />

#### Bicep curl
<img width="161" height="124" alt="04" src="https://github.com/user-attachments/assets/ea69a51e-454c-4b82-8daa-0d9c2fc89dcb" />
<img width="169" height="126" alt="05" src="https://github.com/user-attachments/assets/517c03d3-900f-49ed-b651-a3f6469e87be" />

#### Lateral raise
<img width="202" height="139" alt="06" src="https://github.com/user-attachments/assets/02f62505-f678-4657-9ed9-24040c073491" />
<img width="202" height="141" alt="07" src="https://github.com/user-attachments/assets/1c4bb8b2-541c-4b18-8daa-c953c8f1fae3" />

#### Overhead press
<img width="176" height="129" alt="08" src="https://github.com/user-attachments/assets/b1eb0d43-c9e1-46c3-8f79-870e391fff78" />
<img width="174" height="130" alt="09" src="https://github.com/user-attachments/assets/eced6ea1-872d-4c14-91eb-ed348b83c7cc" />




