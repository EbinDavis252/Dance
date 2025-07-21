# modules/pose_feedback.py

import cv2
import mediapipe as mp
import tempfile
import os

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def analyze_dance_video(video_path):
    cap = cv2.VideoCapture(video_path)
    results_summary = []
    
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.pose_landmarks:
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                posture_quality = "Good"
                tips = "Maintain balance and keep shoulders aligned."
            else:
                posture_quality = "Pose not detected"
                tips = "Ensure clear lighting and full body in frame."

            results_summary.append({
                "frame": len(results_summary),
                "feedback": posture_quality,
                "tips": tips
            })

            if len(results_summary) > 10:  # Limit to 10 frames
                break

        cap.release()

    return results_summary
