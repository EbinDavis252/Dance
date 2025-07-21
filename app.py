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
# ---- 2. Talent Evaluator ----
elif menu == "2. Talent Evaluator":
    st.header("🤖 AI Talent Evaluation")

    uploaded_files = os.listdir("data/video_uploads")
    if not uploaded_files:
        st.warning("No videos uploaded yet. Please upload a video first.")
    else:
        selected_video = st.selectbox("Select a video to evaluate", uploaded_files)
        video_path = os.path.join("data/video_uploads", selected_video)
        st.video(video_path)

        if st.button("Run Evaluation"):
            from modules import talent_evaluator
            with st.spinner("Analyzing video with AI..."):
                scores = talent_evaluator.analyze_dance_video(video_path)

            st.success("Evaluation Complete!")
            st.metric("Pose Accuracy Score", scores["pose_accuracy"], "out of 10")
            st.metric("Rhythm / Movement Score", scores["rhythm"], "out of 10")
            st.metric("Overall Score", scores["overall"], "out of 10")
# ---- 3. Academy Analytics ----
elif menu == "3. Academy Analytics":
    st.header("🏫 Dance Academy Student Dashboard")
    
    from modules import academy_analytics
    
    db_path = "data/student_data.db"
    model_path = "models/dropout_predictor.pkl"

    try:
        df = academy_analytics.load_students_from_db(db_path)
        df_with_risk = academy_analytics.predict_dropout_risk(df, model_path)

        st.dataframe(df_with_risk)

        high_risk_count = df_with_risk[df_with_risk["dropout_flag"] == "⚠️ High Risk"].shape[0]
        st.warning(f"⚠️ {high_risk_count} student(s) are at high risk of dropout.")
    except Exception as e:
        st.error("Failed to load data or model. Please check database or model file.")
        st.text(str(e))
        
