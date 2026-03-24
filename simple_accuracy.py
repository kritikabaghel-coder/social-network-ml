"""
Simple Accuracy Evaluation
==========================
Minimal script to train model and print accuracy
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import warnings

warnings.filterwarnings("ignore")


def main():
    """Simple accuracy evaluation pipeline."""
    
    # Step 1: Load and prepare data
    df = pd.read_csv("data/social_fake_news_sample.csv")
    
    # Create text features
    def create_text(row):
        engagement = "high" if row["likes"] > 80 else "low"
        suspicion = "suspicious" if row["suspicious_word_count"] > 3 else "normal"
        return f"{engagement} {suspicion} article"
    
    df["clean_text"] = df.apply(create_text, axis=1)
    df["label"] = df["fake_label"]
    
    # Step 2: Split data
    X_train, X_test, y_train, y_test = train_test_split(
        df["clean_text"],
        df["label"],
        test_size=0.3,
        random_state=42,
        stratify=df["label"],
    )
    
    # Step 3: Vectorize with TF-IDF
    vectorizer = TfidfVectorizer(max_features=100, stop_words="english")
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    # Step 4: Train model
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train_vec, y_train)
    
    # Step 5: Evaluate accuracy
    y_pred = model.predict(X_test_vec)
    accuracy = accuracy_score(y_test, y_pred)
    
    print("\n" + "=" * 50)
    print("ACCURACY EVALUATION")
    print("=" * 50)
    print(f"\n✓ Final Accuracy Score: {accuracy:.1%}\n")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()
