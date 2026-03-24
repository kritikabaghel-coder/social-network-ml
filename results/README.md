# ML Project Results

## Files in This Directory

### Model Files
- **model.pkl** - Trained Logistic Regression model (binary pickle format)
- **vectorizer.pkl** - TF-IDF vectorizer to convert text to features

### Results Files
- **metrics.json** - Model performance metrics in JSON format
- **metrics.csv** - Model performance metrics in CSV format
- **PROJECT_SUMMARY.md** - Detailed project summary and analysis

## Quick Start

### Load and Use the Model
```python
import pickle

# Load model and vectorizer
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

# Make predictions
text = "your article text here"
X = vectorizer.transform([text])
prediction = model.predict(X)[0]  # 0=REAL, 1=FAKE
```

### Understanding the Results
- **Accuracy**: Overall correctness
- **Precision**: Of all predicted fakes, how many are truly fake?
- **Recall**: Of all actual fakes, how many did we catch?
- **F1-Score**: Balanced metric between precision and recall

## Model Performance
The model achieves excellent performance on the test set with high accuracy, precision, recall, and F1-score.

## Contact
For questions or improvements, refer to the project scripts.
