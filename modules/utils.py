# modules/utils.py

import os
import uuid

def save_video(uploaded_file):
    folder = "data/video_uploads"
    os.makedirs(folder, exist_ok=True)
    
    file_id = str(uuid.uuid4())
    file_path = os.path.join(folder, f"{file_id}_{uploaded_file.name}")
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return file_path
