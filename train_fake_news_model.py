"""
Fake News Detection Model Training
Trains a TF-IDF + Logistic Regression model on news articles
Saves model and vectorizer for Streamlit deployment
"""

import pandas as pd
import numpy as np
import pickle
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
import json


def create_results_folder():
    """Create results folder if it doesn't exist (Streamlit-compatible)"""
    results_path = Path(__file__).parent / "results"
    results_path.mkdir(exist_ok=True)
    return results_path


def load_dataset():
    """Load the fake news dataset"""
    # Load from data folder (relative path - Streamlit compatible)
    data_path = Path(__file__).parent / "data" / "social_fake_news_sample.csv"
    
    if not data_path.exists():
        raise FileNotFoundError(f"Dataset not found at {data_path}")
    
    df = pd.read_csv(data_path)
    print(f"✓ Dataset loaded: {len(df)} articles")
    print(f"  - Real articles: {(df['fake_label'] == 0).sum()}")
    print(f"  - Fake articles: {(df['fake_label'] == 1).sum()}")
    
    return df


def create_text_from_features(row):
    """Create text representation from article features (Streamlit-compatible)"""
    # Combine text_length, suspicious_word_count, and engagement into meaningful text
    text_parts = []
    
    # Add feature information as text
    text_parts.append(f"likes {int(row.get('likes', 0))}")
    text_parts.append(f"shares {int(row.get('shares', 0))}")
    text_parts.append(f"comments {int(row.get('comments', 0))}")
    text_parts.append(f"words {int(row.get('text_length', 0) / 5)}")
    
    # Add suspicious word indicators
    if row.get('suspicious_word_count', 0) > 0:
        text_parts.append("suspicious " * int(row.get('suspicious_word_count', 0)))
    
    # Create full text
    text = " ".join(text_parts)
    return text if text else "article"


def vectorize_and_train(df):
    """Vectorize features and train model"""
    print("\n📊 Preparing text features...")
    
    # Create text representations
    df['text_features'] = df.apply(create_text_from_features, axis=1)
    
    X = df['text_features']
    y = df['fake_label']
    
    print(f"✓ Text features created")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=0.3, 
        random_state=42,
        stratify=y
    )
    
    print(f"✓ Data split: {len(X_train)} train, {len(X_test)} test")
    
    # TF-IDF Vectorization
    print("\n🔤 TF-IDF Vectorization...")
    vectorizer = TfidfVectorizer(
        max_features=100,
        stop_words='english',
        lowercase=True,
        min_df=1,
        max_df=1.0
    )
    
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    print(f"✓ Vectorizer created: {X_train_tfidf.shape[1]} features")
    
    # Train Logistic Regression
    print("\n🤖 Training Logistic Regression...")
    model = LogisticRegression(
        max_iter=1000,
        random_state=42,
        solver='lbfgs',
        C=1.0
    )
    
    model.fit(X_train_tfidf, y_train)
    print("✓ Model trained")
    
    # Evaluate
    print("\n📈 Model Evaluation...")
    y_pred = model.predict(X_test_tfidf)
    y_pred_proba = model.predict_proba(X_test_tfidf)
    
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred, zero_division=0),
        'recall': recall_score(y_test, y_pred, zero_division=0),
        'f1': f1_score(y_test, y_pred, zero_division=0),
        'roc_auc': roc_auc_score(y_test, y_pred_proba[:, 1]),
        'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
    }
    
    print(f"  - Accuracy: {metrics['accuracy']*100:.1f}%")
    print(f"  - Precision: {metrics['precision']*100:.1f}%")
    print(f"  - Recall: {metrics['recall']*100:.1f}%")
    print(f"  - F1-Score: {metrics['f1']*100:.1f}%")
    print(f"  - ROC-AUC: {metrics['roc_auc']*100:.1f}%")
    
    return model, vectorizer, metrics


def save_artifacts(model, vectorizer, metrics):
    """Save model, vectorizer, and metrics (Streamlit-compatible paths)"""
    results_path = create_results_folder()
    
    print("\n💾 Saving artifacts...")
    
    # Save model
    model_path = results_path / "model.pkl"
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"✓ Model saved: {model_path}")
    
    # Save vectorizer
    vectorizer_path = results_path / "vectorizer.pkl"
    with open(vectorizer_path, 'wb') as f:
        pickle.dump(vectorizer, f)
    print(f"✓ Vectorizer saved: {vectorizer_path}")
    
    # Save metrics
    metrics_path = results_path / "metrics.json"
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"✓ Metrics saved: {metrics_path}")
    
    # Save as CSV too
    metrics_csv_path = results_path / "metrics.csv"
    metrics_df = pd.DataFrame([metrics])
    metrics_df.to_csv(metrics_csv_path, index=False)
    print(f"✓ Metrics CSV saved: {metrics_csv_path}")


def main():
    """Main training pipeline"""
    print("=" * 70)
    print("🔍 FAKE NEWS DETECTION - MODEL TRAINING")
    print("=" * 70)
    
    try:
        # Load data
        df = load_dataset()
        
        # Train model
        model, vectorizer, metrics = vectorize_and_train(df)
        
        # Save artifacts
        save_artifacts(model, vectorizer, metrics)
        
        print("\n" + "=" * 70)
        print("✅ TRAINING COMPLETE!")
        print("=" * 70)
        print(f"\nModel ready for Streamlit deployment!")
        print(f"Files saved in: results/")
        print(f"  - model.pkl")
        print(f"  - vectorizer.pkl")
        print(f"  - metrics.json")
        print(f"  - metrics.csv")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        raise


if __name__ == "__main__":
    main()
