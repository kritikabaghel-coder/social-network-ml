# Social Network Analysis & Fake News Detection �🔍

[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/ML-scikit--learn-orange)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## 🌐 Live Demo

**[Try the app here!](https://social-network-ml-jofnq9nhcfbgw3gf7dsaga.streamlit.app/)** 🎯

Enter article text to get real-time fake news predictions powered by machine learning.

---

A machine learning project that detects fake news by combining **social network analysis** with **NLP text classification**. Includes data exploration, graph analysis, centrality measures, and a trained ML model.

## 🎯 Problem

How can we detect fake news articles using engagement patterns and network structure? Fake news often spreads differently than real news—it may have different engagement metrics and network communities. This project explores these patterns using ML.

## 📊 Approach

1. **Data Exploration** - Analyze 30 sample articles with engagement metrics
2. **Network Analysis** - Build graphs where nodes are articles and edges represent text similarity
3. **Centrality Analysis** - Calculate degree, PageRank, closeness, and betweenness centrality
4. **Feature Engineering** - Combine network features with engagement metrics
5. **Classification** - Train TF-IDF + Logistic Regression classifier
6. **Evaluation** - Measure precision, recall, F1-score, and ROC-AUC

## 📈 Results

| Metric | Score |
|--------|-------|
| **Accuracy** | 88.9% |
| **Precision** | 80.0% |
| **Recall** | 100.0% |
| **F1-Score** | 88.9% |
| **ROC-AUC** | 100.0% |

**Key Finding**: Fake articles cluster together in the network and show higher engagement + more suspicious language.

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Data Processing** | Pandas, NumPy |
| **Network Analysis** | NetworkX |
| **ML Classification** | scikit-learn |
| **Vectorization** | TF-IDF |
| **Visualization** | Matplotlib, Seaborn |
| **Notebooks** | Jupyter |

## 🚀 Quick Start

### 1. Setup
```bash
# Clone and navigate
git clone https://github.com/yourusername/social-network-ml.git
cd social-network-ml

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Analysis
```bash
# Full pipeline (data → model → results)
python scripts/train_ml_model.py

# Or run individual steps:
python scripts/explore_and_preprocess.py      # Data exploration
python scripts/build_social_network_graph.py  # Network analysis
python scripts/analyze_centrality.py          # Centrality measures
python scripts/simple_accuracy.py             # Quick accuracy check
```

### 3. Use Trained Model
```python
import pickle

# Load model
with open('results/models/model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('results/models/vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

# Predict
text = "suspicious article with high engagement"
X = vectorizer.transform([text])
prediction = model.predict(X)[0]  # 0=REAL, 1=FAKE
```

## 📁 Project Structure

```
├── data/
│   └── social_fake_news_sample.csv       # 30 sample articles
├── scripts/
│   ├── explore_and_preprocess.py        # Data EDA
│   ├── build_social_network_graph.py    # Network construction
│   ├── analyze_centrality.py            # Network metrics
│   ├── train_ml_model.py                # ML pipeline
│   └── save_results.py                  # Export artifacts
├── results/
│   ├── models/                          # Trained model.pkl
│   ├── metrics/                         # metrics.json
│   └── PROJECT_SUMMARY.md               # Full report
├── notebooks/
│   └── ML_Project_GitHub_Setup.ipynb    # Interactive guide
├── README.md                             # This file
├── DATASET.md                            # Dataset documentation
└── requirements.txt                      # Dependencies
```

## 📊 Dataset

**30 articles** with engagement metrics and network relationships:
- **Features**: likes, shares, comments, text_length, suspicious_word_count, author interactions
- **Split**: 18 real (60%) vs 12 fake (40%)
- **All clean**: no missing values

See [DATASET.md](DATASET.md) for details.

## 🔬 Key Methods

### Network Analysis
- **Graph Construction**: Articles as nodes, text similarity as edges
- **Community Detection**: Grouping similar articles
- **Centrality Measures**: Degree, PageRank, betweenness, closeness

### Classification
- **Vectorizer**: TF-IDF (top 100 features)
- **Model**: Logistic Regression
- **Cross-validation**: Stratified train-test split (70/30)

## 📚 Learn More

- [DATASET.md](DATASET.md) - Data structure & sources
- [GITHUB_SETUP_CHECKLIST.md](GITHUB_SETUP_CHECKLIST.md) - Project setup guide
- [results/PROJECT_SUMMARY.md](results/PROJECT_SUMMARY.md) - Detailed results
- Individual scripts have full docstrings and comments

## 🎓 Skills Demonstrated

✅ Data exploration & preprocessing (pandas)  
✅ Graph analysis & visualization (NetworkX)  
✅ Network centrality calculations  
✅ Feature engineering  
✅ TF-IDF text vectorization  
✅ Logistic regression classification  
✅ Model evaluation (precision, recall, F1)  
✅ Project organization & GitHub ready  

## 💡 Potential Extensions

- Larger datasets (Kaggle, Twitter)
- Advanced models (Random Forest, Neural Networks)
- Real-time predictions (Flask API)
- Sentiment analysis integration
- Topic modeling (LDA, BERTopic)

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Found a bug or have ideas? Open an issue or submit a PR!

## ✉️ Questions?

Check documentation files or open an issue on GitHub.

---

**Status**: ✅ Complete | **Last Updated**: March 24, 2026
