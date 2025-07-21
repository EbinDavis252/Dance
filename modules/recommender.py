# modules/recommender.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_choreo_data(csv_path):
    return pd.read_csv(csv_path)

def recommend_choreos(user_input, data, top_n=3):
    data['combined'] = data['genre'] + " " + data['event_type'] + " " + data['skill_level'] + " " + data['description']

    input_combined = " ".join(user_input.values())
    
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(data['combined'].tolist() + [input_combined])
    
    cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    data['similarity'] = cosine_sim.flatten()

    recommendations = data.sort_values(by='similarity', ascending=False).head(top_n)
    return recommendations[['title', 'genre', 'event_type', 'skill_level', 'description', 'similarity']]
