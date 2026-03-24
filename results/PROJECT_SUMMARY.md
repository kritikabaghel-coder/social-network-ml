# Machine Learning Project Summary
## Fake News Classification Using TF-IDF + Logistic Regression

### Project Date
2026-03-24 13:25:01

### Dataset
- Total articles: 30
- Real articles: 18 (60%)
- Fake articles: 12 (40%)

### Model Configuration
- **Algorithm**: Logistic Regression
- **Vectorization**: TF-IDF (max 100 features)
- **Test Size**: 30%
- **Train-Test Split**: 21 train / 9 test

### Model Performance

#### Key Metrics
| Metric | Score |
|--------|-------|
| **Accuracy** | 88.9% |
| **Precision** | 80.0% |
| **Recall** | 100.0% |
| **F1-Score** | 88.9% |
| **ROC-AUC** | 100.0% |

#### Confusion Matrix
| | Predicted Real | Predicted Fake |
|---|---|---|
| **Actual Real** | 4 | 1 |
| **Actual Fake** | 0 | 4 |

### Interpretation
- **Accuracy**: 88.9% - The model correctly classifies articles as fake or real
- **Precision**: 80.0% - When predicting FAKE, the model is correct 80.0% of the time
- **Recall**: 100.0% - The model catches 100.0% of all actual fake articles
- **F1-Score**: 88.9% - Overall balance between precision and recall

### Output Files Generated
- `model.pkl` - Trained Logistic Regression model
- `vectorizer.pkl` - TF-IDF vectorizer for text processing
- `metrics.json` - Model metrics in JSON format
- `metrics.csv` - Model metrics in CSV format
- `PROJECT_SUMMARY.md` - This summary report

### How to Use the Saved Model
See README.md for code examples on loading and using the model.

### Project Scripts
1. `explore_and_preprocess.py` - Data exploration and cleaning
2. `build_social_network_graph.py` - Network analysis
3. `analyze_centrality.py` - Centrality measure analysis
4. `train_ml_model.py` - Complete ML pipeline
5. `simple_accuracy.py` - Quick accuracy check

### Conclusion
The logistic regression model successfully classifies fake vs. real articles with 89% accuracy using TF-IDF features.
The model is ready for deployment and can be loaded from the saved pickle files.

---
**Project completed**: 2026-03-24
