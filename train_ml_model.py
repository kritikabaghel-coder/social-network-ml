"""
Simple ML Model: TF-IDF + Logistic Regression
==============================================
Classify articles as FAKE or REAL using:
- TF-IDF: Convert text to numerical vectors
- Logistic Regression: Simple, interpretable classifier
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    roc_auc_score,
)
import warnings

warnings.filterwarnings("ignore")


def load_and_prepare_data(csv_path: str) -> tuple:
    """Load data and create text features."""
    print("Step 1: Loading data...")
    df = pd.read_csv(csv_path)

    # Create synthetic clean text from features
    # (In real projects, you'd have actual article text)
    def create_clean_text(row):
        """Create text representation from numerical features."""
        engagement = "high" if row["likes"] > 80 else "low"
        suspicion = "suspicious" if row["suspicious_word_count"] > 3 else "normal"
        length = "long" if row["text_length"] > 120 else "short"
        shares = "shared" if row["shares"] > 25 else "quiet"

        # Create text-like features
        text = f"{engagement} engagement {suspicion} content {length} article {shares} widely"
        return text

    df["clean_text"] = df.apply(create_clean_text, axis=1)
    df["label"] = df["fake_label"]

    print(f"   ✓ Loaded {len(df)} articles")
    print(f"   ✓ Created clean_text column")
    print(f"   ✓ Real: {(df['label']==0).sum()}, Fake: {(df['label']==1).sum()}\n")

    return df


def show_sample_data(df: pd.DataFrame) -> None:
    """Display sample data."""
    print("Step 2: Sample data")
    print("-" * 70)
    for i in range(min(3, len(df))):
        text = df["clean_text"].iloc[i]
        label = "REAL" if df["label"].iloc[i] == 0 else "FAKE"
        print(f"  Article {i+1}: '{text}'")
        print(f"    → Label: {label}\n")


def tfidf_vectorization(X_train: pd.Series, X_test: pd.Series) -> tuple:
    """
    Convert text to numerical vectors using TF-IDF.

    TF-IDF = Term Frequency - Inverse Document Frequency
    - TF: How often a word appears in a document
    - IDF: How unique/important a word is across all documents
    - Higher score = more important word
    """
    print("Step 3: TF-IDF Vectorization")
    print("-" * 70)

    vectorizer = TfidfVectorizer(
        max_features=100,      # Keep only top 100 words
        lowercase=True,        # Convert to lowercase
        stop_words="english",  # Remove common words
        min_df=1,             # Word must appear in at least 1 document
    )

    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    print(f"  ✓ Created {X_train_vec.shape[1]} features from text")
    print(f"  ✓ Training set: {X_train_vec.shape[0]} samples")
    print(f"  ✓ Test set: {X_test_vec.shape[0]} samples")

    # Show top features
    feature_names = vectorizer.get_feature_names_out()
    print(f"\n  Top 10 important words: {', '.join(feature_names[:10])}\n")

    return X_train_vec, X_test_vec


def train_logistic_regression(X_train: np.ndarray, y_train: np.ndarray) -> LogisticRegression:
    """
    Train Logistic Regression model.

    Why Logistic Regression?
    - Simple and fast
    - Interpretable (see which words predict FAKE vs REAL)
    - Works well for text classification
    - Outputs probability scores (0 to 1)
    """
    print("Step 4: Train Logistic Regression")
    print("-" * 70)

    model = LogisticRegression(
        max_iter=1000,      # Maximum iterations
        random_state=42,    # For reproducibility
        C=1.0,             # Regularization strength (lower = more regularization)
    )

    model.fit(X_train, y_train)
    print("  ✓ Model trained successfully\n")

    return model


def evaluate_model(model: LogisticRegression, X_test: np.ndarray, y_test: np.ndarray) -> dict:
    """Evaluate model on test data."""
    print("Step 5: Model Evaluation")
    print("-" * 70)

    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]

    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_proba)

    print(f"  Accuracy:  {accuracy:.3f}  (out of 1.0)")
    print(f"  Precision: {precision:.3f}  (% of predicted FAKE that are correct)")
    print(f"  Recall:    {recall:.3f}  (% of actual FAKE we found)")
    print(f"  F1-Score:  {f1:.3f}  (balance between precision & recall)")
    print(f"  ROC-AUC:   {roc_auc:.3f}  (overall ranking ability)\n")

    # Confusion matrix
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()

    print("Confusion Matrix:")
    print(f"  True Negatives (correctly identified REAL):   {tn}")
    print(f"  False Positives (incorrectly labeled FAKE):   {fp}")
    print(f"  False Negatives (incorrectly labeled REAL):   {fn}")
    print(f"  True Positives (correctly identified FAKE):   {tp}\n")

    print("Classification Report:")
    print(classification_report(y_test, y_pred, target_names=["REAL", "FAKE"]))

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "roc_auc": roc_auc,
    }


def make_predictions(model: LogisticRegression, vectorizer: TfidfVectorizer) -> None:
    """Make predictions on new sample texts."""
    print("Step 6: Make Predictions on New Text")
    print("-" * 70)

    sample_texts = [
        "high engagement suspicious content long article shared widely",
        "low engagement normal content short article quiet widely",
        "high engagement suspicious content short article shared widely",
    ]

    for text in sample_texts:
        X_sample = vectorizer.transform([text])
        prediction = model.predict(X_sample)[0]
        probability = model.predict_proba(X_sample)[0]

        label = "FAKE" if prediction == 1 else "REAL"
        fake_prob = probability[1]

        print(f"\n  Text: '{text}'")
        print(f"  Prediction: {label}")
        print(f"  Confidence: {fake_prob*100:.1f}% confidence it's FAKE")


def save_model_results(model_results: dict, output_file: str = "data/model_results.txt") -> None:
    """Save model results to file."""
    with open(output_file, "w") as f:
        f.write("LOGISTIC REGRESSION MODEL RESULTS\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Accuracy:  {model_results['accuracy']:.3f}\n")
        f.write(f"Precision: {model_results['precision']:.3f}\n")
        f.write(f"Recall:    {model_results['recall']:.3f}\n")
        f.write(f"F1-Score:  {model_results['f1']:.3f}\n")
        f.write(f"ROC-AUC:   {model_results['roc_auc']:.3f}\n")

    print(f"\n✓ Results saved to {output_file}\n")


def main() -> None:
    """Main execution pipeline."""
    print("\n" + "=" * 70)
    print("FAKE NEWS CLASSIFICATION WITH ML")
    print("=" * 70 + "\n")

    # Load data
    df = load_and_prepare_data("data/social_fake_news_sample.csv")

    # Show samples
    show_sample_data(df)

    # Split data
    print("Step 2.5: Split data into train/test")
    print("-" * 70)
    X_train, X_test, y_train, y_test = train_test_split(
        df["clean_text"],
        df["label"],
        test_size=0.3,      # 30% for testing
        random_state=42,
        stratify=df["label"],
    )
    print(f"  ✓ Train: {len(X_train)} samples")
    print(f"  ✓ Test: {len(X_test)} samples\n")

    # Vectorize
    X_train_vec, X_test_vec = tfidf_vectorization(X_train, X_test)

    # Train
    model = train_logistic_regression(X_train_vec, y_train)

    # Evaluate
    results = evaluate_model(model, X_test_vec, y_test)

    # Predict
    from sklearn.feature_extraction.text import TfidfVectorizer

    vectorizer = TfidfVectorizer(
        max_features=100,
        lowercase=True,
        stop_words="english",
        min_df=1,
    )
    vectorizer.fit(df["clean_text"])
    make_predictions(model, vectorizer)

    # Save
    save_model_results(results)

    print("=" * 70)
    print("✓ ML Pipeline Complete!")
    print("=" * 70)
    print("\n📌 Key Takeaways:")
    print("  1. TF-IDF converts text → numbers")
    print("  2. Logistic Regression learns to classify")
    print("  3. Metrics show how well it works")
    print("  4. Model can predict on new text\n")


if __name__ == "__main__":
    main()
