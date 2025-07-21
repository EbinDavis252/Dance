# app.py

import streamlit as st
import os
from modules import utils

st.set_page_config(page_title="Dance Intelligence Platform", layout="wide")

# App Title and Sidebar
st.sidebar.image("assets/logo.png", width=200)
st.sidebar.title("Dance Intelligence Platform (DIP)")

menu = st.sidebar.radio("Go to", [
    "1. Upload Dance Video",
    "2. Talent Evaluator",
    "3. Academy Analytics",
    "4. Choreography Recommender",
    "5. Pose Correction",
    "6. Event Performance Analytics",
    "7. Dance Culture AI",
    "8. Admin Panel"
])

st.title("🎵 Welcome to Dance Intelligence Platform (DIP)")

# ---- 1. Upload Module ----
if menu == "1. Upload Dance Video":
    st.header("📤 Upload Your Dance Video")
    
    uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov"])
    if uploaded_file is not None:
        file_path = utils.save_video(uploaded_file)
        st.success(f"Uploaded to: {file_path}")
        st.video(file_path)

        st.info("Your video is saved and ready for Talent Evaluation and Pose Correction.")
