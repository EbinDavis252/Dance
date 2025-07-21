# modules/academy_analytics.py

import pandas as pd
import numpy as np
import sqlite3
import pickle

def load_students_from_db(db_path):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM students", conn)
    conn.close()
    return df

def predict_dropout_risk(df, model_path):
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    features = df[['attendance_percent', 'engagement_score']]
    df['dropout_risk'] = model.predict_proba(features)[:, 1]
    df['dropout_flag'] = df['dropout_risk'].apply(lambda x: "⚠️ High Risk" if x > 0.5 else "✅ Safe")
    df['dropout_risk'] = df['dropout_risk'].round(2)
    return df
