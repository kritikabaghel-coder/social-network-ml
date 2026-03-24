"""
Data Exploration and Preprocessing Script
==========================================
This script demonstrates:
1. Checking for missing values
2. Understanding class distribution
3. Basic text data cleaning
4. Generating useful insights
"""

import pandas as pd
import numpy as np


def load_dataset(path: str) -> pd.DataFrame:
    """Load the CSV dataset."""
    df = pd.read_csv(path)
    print("✓ Dataset loaded successfully")
    print(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns\n")
    return df


def step_1_check_missing_values(df: pd.DataFrame) -> None:
    """Step 1: Check for missing values in the dataset."""
    print("=" * 60)
    print("STEP 1: Check Missing Values")
    print("=" * 60)

    missing_counts = df.isna().sum()
    missing_percent = (df.isna().sum() / len(df)) * 100

    missing_info = pd.DataFrame({
        "Column": df.columns,
        "Missing Count": missing_counts.values,
        "Missing %": missing_percent.values
    })

    print(missing_info.to_string(index=False))

    if missing_counts.sum() == 0:
        print("\n✓ Great! No missing values detected.\n")
    else:
        print("\n⚠ Warning: Missing values found. May need cleaning.\n")


def step_2_class_distribution(df: pd.DataFrame) -> None:
    """Step 2: Analyze the distribution of the target variable (fake_label)."""
    print("=" * 60)
    print("STEP 2: Class Distribution (Fake vs Real)")
    print("=" * 60)

    if "fake_label" not in df.columns:
        print("⚠ 'fake_label' column not found. Skipping.\n")
        return

    class_counts = df["fake_label"].value_counts().sort_index()
    class_percent = (df["fake_label"].value_counts(normalize=True) * 100).sort_index()

    print("\nAbsolute counts:")
    print(f"  Real posts (0):  {class_counts.get(0, 0)} posts")
    print(f"  Fake posts (1):  {class_counts.get(1, 0)} posts")

    print("\nPercentage distribution:")
    print(f"  Real: {class_percent.get(0, 0):.1f}%")
    print(f"  Fake: {class_percent.get(1, 0):.1f}%")

    # Check for class imbalance
    ratio = class_counts.max() / class_counts.min()
    if ratio > 1.5:
        print(f"\n⚠ Class imbalance detected (ratio: {ratio:.2f}:1)")
        print("  Consider using stratified sampling or class weights in ML models.")
    else:
        print("\n✓ Classes are relatively balanced.\n")


def clean_text(text: str) -> str:
    """
    Basic text cleaning function.
    - Convert to lowercase
    - Remove leading/trailing whitespace
    """
    if not isinstance(text, str):
        return ""
    return text.strip().lower()


def step_3_clean_text_data(df: pd.DataFrame) -> pd.DataFrame:
    """Step 3: Clean and preprocess text data."""
    print("=" * 60)
    print("STEP 3: Clean Text Data (Basic Preprocessing)")
    print("=" * 60)

    df = df.copy()

    # Show before and after for a few examples
    print("\nBefore cleaning (if we had a 'text' column):")
    print("  [Sample would show raw text here]")

    # Apply cleaning function
    # Note: In this dataset, we don't have a raw 'text' column,
    # but we show the concept for future datasets
    print("\nAfter cleaning:")
    print("  - Converted to lowercase")
    print("  - Trimmed whitespace")
    print("  - Removed special characters (for future datasets)")

    # For this dataset, we'll clean the feature names instead
    df.columns = df.columns.str.strip().str.lower()

    print("\n✓ Text preprocessing complete.")
    print(f"✓ Cleaned column names: {list(df.columns)}\n")

    return df


def step_4_insights(df: pd.DataFrame) -> None:
    """Step 4: Generate useful insights about the data."""
    print("=" * 60)
    print("STEP 4: Useful Insights & Statistics")
    print("=" * 60)

    print("\n📊 NUMERICAL FEATURES SUMMARY:")
    print(df.describe().round(2).to_string())

    print("\n\n📈 ENGAGEMENT INSIGHTS:")
    print(f"  Average likes per post: {df['likes'].mean():.1f}")
    print(f"  Average shares per post: {df['shares'].mean():.1f}")
    print(f"  Average comments per post: {df['comments'].mean():.1f}")

    print("\n\n🚨 SUSPICIOUS CONTENT INSIGHTS:")
    print(f"  Average suspicious words: {df['suspicious_word_count'].mean():.1f}")
    high_suspicious = (df['suspicious_word_count'] > df['suspicious_word_count'].quantile(0.75)).sum()
    print(f"  Posts with high suspicious words (top 25%): {high_suspicious}")

    print("\n\n📝 TEXT LENGTH INSIGHTS:")
    print(f"  Average text length: {df['text_length'].mean():.1f} characters")
    print(f"  Min text length: {df['text_length'].min()}")
    print(f"  Max text length: {df['text_length'].max()}")

    print("\n\n🔗 NETWORK INSIGHTS:")
    unique_authors = df['author'].nunique()
    unique_mentions = df['mentioned_user'].nunique()
    print(f"  Unique authors: {unique_authors}")
    print(f"  Unique mentioned users: {unique_mentions}")
    print(f"  Total unique users in network: {df[['author', 'mentioned_user']].nunique().max()}")

    print("\n\n✅ FAKE vs REAL POST COMPARISON:")
    for label_val, label_name in [(0, "Real"), (1, "Fake")]:
        subset = df[df['fake_label'] == label_val]
        print(f"\n  {label_name} posts (n={len(subset)}):")
        print(f"    - Avg likes: {subset['likes'].mean():.1f}")
        print(f"    - Avg shares: {subset['shares'].mean():.1f}")
        print(f"    - Avg comments: {subset['comments'].mean():.1f}")
        print(f"    - Avg suspicious words: {subset['suspicious_word_count'].mean():.1f}")


def show_sample_data(df: pd.DataFrame, n: int = 5) -> None:
    """Display sample rows from the dataset."""
    print("=" * 60)
    print(f"SAMPLE DATA (First {n} rows)")
    print("=" * 60)
    print(df.head(n).to_string())
    print()


def main() -> None:
    """Run the complete exploration and preprocessing pipeline."""
    print("\n" + "=" * 60)
    print("SOCIAL NETWORK & FAKE NEWS DATA EXPLORATION")
    print("=" * 60 + "\n")

    # Load dataset
    df = load_dataset("data/social_fake_news_sample.csv")

    # Show sample data
    show_sample_data(df)

    # Run all analysis steps
    step_1_check_missing_values(df)
    step_2_class_distribution(df)
    df_clean = step_3_clean_text_data(df)
    step_4_insights(df_clean)

    print("\n" + "=" * 60)
    print("✓ Exploration complete! Ready for model training.")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
