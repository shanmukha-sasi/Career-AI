import os
import numpy as np
import joblib
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline

def build_models():
    print("Initializing Machine Learning Build Sequence...")
    os.makedirs('ml_models', exist_ok=True)

    # ---------------------------------------------------------
    # 1. K-Means Clustering Model (Skill Gap Analyzer)
    # ---------------------------------------------------------
    print("Training Skill Clusterer (K-Means)...")
    np.random.seed(42)
    X_skills = np.random.randint(1, 6, size=(1000, 5)) 
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    kmeans.fit(X_skills)
    joblib.dump(kmeans, 'ml_models/skill_clusterer.pkl')
    print("✅ skill_clusterer.pkl saved.")

    # ---------------------------------------------------------
    # 2. Random Forest Regressor (Viral Score Predictor)
    # ---------------------------------------------------------
    print("Training Engagement Model (Random Forest)...")
    
    # ADVANCED SYNTHETIC DATASET (Sasi's Logic Implemented)
    synthetic_posts = [
        # High Engagement (Deep Tech, Wins, Open Source)
        "Thrilled to announce our team won 1st place at the Solasta Hackathon! We built an autonomous AI agent using Gemini 1.5 Flash and Supabase. #HackathonWinner",
        "Just open-sourced my Kubernetes deployment pipeline. It reduces CI/CD build times by 40%. Check out the GitHub repo below!",
        "Deep dive into System Design: How does Netflix handle global scale? Here is my breakdown of their microservices architecture.",
        "Deployed a full-stack Next.js app with a Python backend today. Overcame major CORS issues and learned a lot about JWT authentication.",

        # Medium Engagement (Struggles, generic updates)
        "Midnight struggles with React useEffect hooks... why does it keep re-rendering?! Finally fixed it after 3 hours. #codinglife",
        "Completed the 100 Days of Code challenge! It was a long journey but I learned a lot about web development.",
        "Attended an amazing workshop on Generative AI today. Excited to try out these new tools.",

        # Low Engagement (Low effort, begging, no value)
        "Looking for a software engineering job. Please refer me. I know Java.",
        "Just learned python. It is a good language.",
        "Hello network.",
        "I am doing a project.",
        "Need help."
    ] * 20 # Expanded dataset size
    
    synthetic_scores = [
        98.0, 92.0, 88.0, 85.0, # High scores
        65.0, 55.0, 45.0,       # Medium scores
        15.0, 12.0, 5.0, 8.0, 10.0 # Low scores
    ] * 20 

    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=100)),
        ('rf', RandomForestRegressor(n_estimators=50, random_state=42))
    ])
    
    pipeline.fit(synthetic_posts, synthetic_scores)
    joblib.dump(pipeline, 'ml_models/engagement_model.pkl')
    print("✅ engagement_model.pkl saved.")
    print("\nAll models built successfully. Ready for UI integration.")

if __name__ == "__main__":
    build_models()