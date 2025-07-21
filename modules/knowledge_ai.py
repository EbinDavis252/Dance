# modules/knowledge_ai.py

import json
from difflib import get_close_matches

def load_knowledge_base():
    with open("data/dance_knowledge.json", "r", encoding="utf-8") as f:
        return json.load(f)

def get_answer(user_question):
    kb = load_knowledge_base()
    questions = [item["question"] for item in kb]
    match = get_close_matches(user_question, questions, n=1, cutoff=0.4)
    
    if match:
        for item in kb:
            if item["question"] == match[0]:
                return item["answer"]
    return "I'm sorry, I couldn't find an answer to that. Try asking in a different way."
