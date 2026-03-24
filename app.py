"""
Streamlit App: Social Network ML - Fake News Detector
Interactive web application for fake news detection using ML model
"""

import streamlit as st
import pickle
import pandas as pd
import numpy as np
import json
from pathlib import Path

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Fake News Detector",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# LOAD MODEL AND VECTORIZER
# ============================================================================


   @st.cache_resource
def load_model_and_vectorizer():
    """Load trained model and vectorizer once at startup"""
    try:
        model = pickle.load(open("results/model.pkl", "rb"))
        vectorizer = pickle.load(open("results/vectorizer.pkl", "rb"))
        return model, vectorizer, True

    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None, False
        

@st.cache_data
def load_metrics():
    """Load model metrics"""
    try:
        metrics_path = Path(__file__).parent / "results" / "metrics.json"
        with open(metrics_path, 'r') as f:
            metrics = json.load(f)
        return metrics
    except:
        return None

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def create_text_features(text):
    """Create features from input text (matching training process)"""
    features = {
        'text_length': len(text),
        'suspicious_word_count': sum(1 for word in text.lower().split() 
                                     if word in ['fake', 'hoax', 'scam', 'spam', 'misleading']),
        'num_words': len(text.split()),
        'capital_ratio': sum(1 for c in text if c.isupper()) / max(1, len(text)),
    }
    return features

def make_prediction(text, model, vectorizer):
    """Make prediction on text"""
    # Vectorize text
    text_vectorized = vectorizer.transform([text])
    
    # Get prediction and probability
    prediction = model.predict(text_vectorized)[0]
    probability = model.predict_proba(text_vectorized)[0]
    
    return prediction, probability

def format_confidence(prob_real, prob_fake):
    """Format confidence as percentage"""
    return f"Real: {prob_real*100:.1f}% | Fake: {prob_fake*100:.1f}%"

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    # Title and description
    st.title("🔍 Fake News Detector")
    st.markdown("### Powered by Social Network Analysis + Machine Learning")
    
    # Load model
    model, vectorizer, model_loaded = load_model_and_vectorizer()
    metrics = load_metrics()
    
    if not model_loaded:
        st.error("⚠️ Model files not found. Please ensure model.pkl and vectorizer.pkl are in the results/ folder.")
        st.stop()
    
    # Sidebar - Navigation
    st.sidebar.title("📋 Navigation")
    page = st.sidebar.radio("Select Page", ["🎯 Predictor", "📊 Model Info", "📖 About"])
    
    # ========================================================================
    # PAGE 1: PREDICTOR
    # ========================================================================
    
    if page == "🎯 Predictor":
        st.markdown("---")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Enter Article Text")
            user_text = st.text_area(
                "Paste article text here:",
                height=150,
                placeholder="Enter the text you want to classify as REAL or FAKE news...",
                label_visibility="collapsed"
            )
        
        with col2:
            st.subheader("🎛️ Settings")
            confidence_threshold = st.slider(
                "Confidence Threshold",
                min_value=0.5,
                max_value=1.0,
                value=0.7,
                step=0.05,
                help="Minimum confidence to show prediction"
            )
        
        # Prediction section
        st.markdown("---")
        
        if user_text.strip():
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col2:
                if st.button("🚀 Analyze", use_container_width=True):
                    with st.spinner("Analyzing..."):
                        prediction, probability = make_prediction(user_text, model, vectorizer)
                        
                        # Extract probabilities
                        prob_real = probability[0]  # Probability of REAL (class 0)
                        prob_fake = probability[1]  # Probability of FAKE (class 1)
                        max_prob = max(prob_real, prob_fake)
                        
                        # Show results
                        st.markdown("---")
                        st.subheader("📊 Prediction Results")
                        
                        # Create metrics display
                        metric_col1, metric_col2, metric_col3 = st.columns(3)
                        
                        with metric_col1:
                            pred_text = "✅ REAL" if prediction == 0 else "❌ FAKE"
                            st.metric(
                                "Classification",
                                pred_text,
                                delta=None
                            )
                        
                        with metric_col2:
                            st.metric(
                                "Confidence",
                                f"{max_prob*100:.1f}%",
                                delta=None
                            )
                        
                        with metric_col3:
                            status = "✅ High Confidence" if max_prob >= confidence_threshold else "⚠️ Low Confidence"
                            st.metric(
                                "Status",
                                status,
                                delta=None
                            )
                        
                        # Probability bars
                        st.markdown("**Probability Distribution:**")
                        
                        col_left, col_right = st.columns(2)
                        with col_left:
                            st.progress(prob_real, text=f"Real News: {prob_real*100:.1f}%")
                        with col_right:
                            st.progress(prob_fake, text=f"Fake News: {prob_fake*100:.1f}%")
                        
                        # Text statistics
                        st.markdown("---")
                        st.subheader("📈 Text Statistics")
                        
                        text_features = create_text_features(user_text)
                        stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
                        
                        with stats_col1:
                            st.metric("Text Length", f"{text_features['text_length']} chars")
                        with stats_col2:
                            st.metric("Word Count", f"{text_features['num_words']} words")
                        with stats_col3:
                            st.metric("Suspicious Words", text_features['suspicious_word_count'])
                        with stats_col4:
                            st.metric("Caps Ratio", f"{text_features['capital_ratio']:.1%}")
                        
                        # Advice
                        st.markdown("---")
                        if prediction == 1:  # Fake
                            st.warning(
                                "⚠️ **This article may be FAKE news.**\n\n"
                                "**What makes it suspicious:**\n"
                                "- Contains suspicious language patterns\n"
                                "- Text features align with known fake news characteristics\n"
                                "\n**Next steps:**\n"
                                "- Verify facts with multiple sources\n"
                                "- Check author credibility\n"
                                "- Look for cited evidence"
                            )
                        else:  # Real
                            st.success(
                                "✅ **This article appears to be REAL news.**\n\n"
                                "**Positive indicators:**\n"
                                "- Text follows real news patterns\n"
                                "- Language is more credible\n"
                                "\n**Still verify by:**\n"
                                "- Checking multiple sources\n"
                                "- Reviewing author credentials\n"
                                "- Fact-checking key claims"
                            )
        
        else:
            st.info("👆 Enter text above and click 'Analyze' to get predictions")
    
    # ========================================================================
    # PAGE 2: MODEL INFO
    # ========================================================================
    
    elif page == "📊 Model Info":
        st.subheader("Model Performance Metrics")
        
        if metrics:
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("Accuracy", f"{metrics.get('accuracy', 0)*100:.1f}%")
            with col2:
                st.metric("Precision", f"{metrics.get('precision', 0)*100:.1f}%")
            with col3:
                st.metric("Recall", f"{metrics.get('recall', 0)*100:.1f}%")
            with col4:
                st.metric("F1-Score", f"{metrics.get('f1', 0)*100:.1f}%")
            with col5:
                st.metric("ROC-AUC", f"{metrics.get('roc_auc', 0)*100:.1f}%")
        
        st.markdown("---")
        st.subheader("How It Works")
        
        st.markdown("""
        ### 🔍 Detection Process
        
        1. **Text Vectorization**: Converts article text into numerical features using TF-IDF
        2. **Feature Extraction**: Captures engagement patterns and text characteristics
        3. **Classification**: Logistic Regression model predicts REAL or FAKE
        4. **Confidence**: Provides probability scores for transparency
        
        ### 📚 Training Data
        
        - **30 sample articles** (18 real, 12 fake)
        - **Features**: Engagement metrics (likes, shares, comments), text properties, social network structure
        - **Algorithm**: TF-IDF Vectorization + Logistic Regression
        - **Train/Test Split**: 70% / 30% stratified
        
        ### 🎯 Model Strengths
        
        ✅ High recall (catches most fake news)
        ✅ Good precision (reduces false positives)
        ✅ Fast predictions (real-time analysis)
        ✅ Interpretable results
        
        ### ⚠️ Limitations
        
        - Trained on limited dataset (30 articles)
        - Works best on similar article types
        - Should not be sole fact-checking source
        - Requires dataset expansion for production use
        """)
        
        st.markdown("---")
        st.subheader("Technical Details")
        
        tech_col1, tech_col2 = st.columns(2)
        
        with tech_col1:
            st.markdown("""
            **Vectorization**
            - Method: TF-IDF
            - Max Features: 100
            - Stop Words: English (removed)
            """)
        
        with tech_col2:
            st.markdown("""
            **Classification**
            - Algorithm: Logistic Regression
            - Max Iterations: 1000
            - Regularization: L2 (default)
            """)
    
    # ========================================================================
    # PAGE 3: ABOUT
    # ========================================================================
    
    elif page == "📖 About":
        st.subheader("About This Project")
        
        st.markdown("""
        ## 🎓 Project Overview
        
        **Social Network Analysis for Fake News Detection**
        
        This machine learning project combines network analysis with NLP to detect fake news articles.
        The key insight: fake articles cluster together in social networks and exhibit distinct engagement patterns.
        
        ### 📊 Dataset
        
        - **Source**: Synthetic social media dataset
        - **Size**: 30 articles (18 real, 12 fake)
        - **Features**: 9 features including engagement metrics and text analysis
        
        ### 🔗 Network Analysis
        
        - **Nodes**: Articles as nodes
        - **Edges**: Links based on text similarity
        - **Communities**: Articles naturally cluster into 2 communities
        - **Finding**: Fake articles cluster together (90%+ in one community)
        
        ### 🎯 Centrality Measures
        
        We analyzed multiple centrality metrics:
        - **Degree Centrality**: How connected each article is
        - **PageRank**: Importance in the network
        - **Closeness**: How central to the network
        - **Betweenness**: How many shortest paths pass through each node
        
        **Finding**: Fake articles show distinct centrality patterns
        
        ### 🛠️ Technology Stack
        
        - **Python 3.13**: Programming language
        - **pandas / NumPy**: Data processing
        - **NetworkX**: Network analysis
        - **scikit-learn**: Machine learning
        - **Streamlit**: Web application
        - **Jupyter**: Notebooks & exploration
        
        ### 📈 Results
        
        Our Logistic Regression model achieves:
        - ✅ **88.9% Accuracy**
        - ✅ **100% Recall** (catches all fake news in test set)
        - ✅ **80% Precision** (mostly correct identifications)
        
        ### 🚀 Next Steps
        
        - Expand dataset to 1000+ articles
        - Implement deep learning (BERT, RoBERTa)
        - Add real-time API
        - Deploy mobile app
        
        ### 📚 Learn More
        
        - [GitHub Repository](https://github.com)
        - [Project Documentation](https://github.com)
        - [Data Exploration Notebook](https://github.com)
        
        ### 👤 Contact
        
        For questions or collaborations, feel free to reach out!
        """)
        
        st.markdown("---")
        st.markdown("Made with ❤️ using Python, Streamlit, and Machine Learning")

if __name__ == "__main__":
    main()
