# modules/talent_evaluator.py

import cv2
import mediapipe as mp
import numpy as np

def analyze_dance_video(video_path):
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    cap = cv2.VideoCapture(video_path)

    total_frames = 0
    keypoints_detected = 0
    movement_score = []

    success, frame = cap.read()
    prev_landmarks = None

    while success:
        total_frames += 1
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        if results.pose_landmarks:
            keypoints_detected += 1

            current_landmarks = np.array([
                [lm.x, lm.y, lm.z] for lm in results.pose_landmarks.landmark
            ])

            if prev_landmarks is not None:
                movement = np.linalg.norm(current_landmarks - prev_landmarks)
                movement_score.append(movement)

            prev_landmarks = current_landmarks

        success, frame = cap.read()

    cap.release()
    pose.close()

    detection_ratio = keypoints_detected / total_frames if total_frames > 0 else 0
    movement_avg = np.mean(movement_score) if movement_score else 0

    # Convert to scores out of 10
    rhythm_score = round(min(movement_avg * 5, 10), 2)
    pose_accuracy_score = round(detection_ratio * 10, 2)
    overall_score = round((rhythm_score + pose_accuracy_score) / 2, 2)

    return {
        "pose_accuracy": pose_accuracy_score,
        "rhythm": rhythm_score,
        "overall": overall_score
    }
