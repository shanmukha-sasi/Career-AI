import os
import numpy as np
import joblib
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline

def build_models():
    print("Initializing Machine Learning Build Sequence (V2)...")
    os.makedirs('ml_models', exist_ok=True)

    # ---------------------------------------------------------
    # 1. K-Means Clustering (10 CSE Archetypes)
    # Features: [DSA, OOPS, DBMS, OS, System_Design] (Scale 1-5)
    # ---------------------------------------------------------
    print("Generating Synthetic Persona Data & Training Clusterer...")
    
    # Define the 10 archetypes centers
    centroids = {
        0: [5, 3, 2, 2, 1], # Competitive Programmer
        1: [4, 5, 5, 3, 4], # Backend Architect
        2: [2, 3, 4, 5, 4], # DevOps / SRE
        3: [2, 2, 5, 4, 2], # Database Admin (DBA)
        4: [4, 4, 2, 5, 3], # Systems Programmer
        5: [3, 4, 3, 3, 3], # Core Generalist
        6: [2, 3, 2, 1, 1], # UI/Frontend Specialist
        7: [1, 2, 1, 1, 1], # Academic Beginner
        8: [3, 5, 4, 2, 3], # Enterprise OOPs Dev
        9: [5, 5, 5, 5, 5]  # The FAANG Unicorn
    }
    
    X_skills = []
    np.random.seed(42)
    
    # Generate 200 synthetic profiles per archetype using normal distribution
    for cluster_id, center in centroids.items():
        noise = np.random.normal(0, 0.6, (200, 5)) # Add slight variations
        samples = np.array(center) + noise
        samples = np.clip(np.round(samples), 1, 5) # Ensure it stays within 1-5 bounds
        X_skills.extend(samples)
        
    X_skills = np.array(X_skills)
    
    # Train the 10-Cluster Model
    kmeans = KMeans(n_clusters=10, random_state=42, n_init=10)
    kmeans.fit(X_skills)
    joblib.dump(kmeans, 'ml_models/skill_clusterer.pkl')
    print("✅ skill_clusterer.pkl saved (10 Personas mapped).")

    # ---------------------------------------------------------
    # 2. Random Forest Regressor (Viral Score Predictor)
    # ---------------------------------------------------------
    print("Training Engagement Model (Random Forest)...")
    synthetic_posts = [
        "Thrilled to announce our team won 1st place at the Solasta Hackathon! We built an autonomous AI agent using Gemini 1.5 Flash and Supabase. #HackathonWinner",
        "Just open-sourced my Kubernetes deployment pipeline. It reduces CI/CD build times by 40%. Check out the GitHub repo below!",
        "Deep dive into System Design: How does Netflix handle global scale? Here is my breakdown of their microservices architecture.",
        "Midnight struggles with React useEffect hooks... why does it keep re-rendering?! Finally fixed it after 3 hours. #codinglife",
        "Completed the 100 Days of Code challenge! It was a long journey but I learned a lot.",
        "Looking for a software engineering job. Please refer me. I know Java.",
        "Just learned python. It is a good language."
    ] * 30 
    
    synthetic_scores = [98.0, 92.0, 88.0, 65.0, 55.0, 15.0, 12.0] * 30 

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