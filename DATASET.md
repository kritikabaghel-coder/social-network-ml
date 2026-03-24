# Dataset Documentation

## Dataset Information

- **Name**: Social Network Analysis - Fake News Classification Dataset
- **Format**: CSV (Comma-Separated Values)
- **Size**: Small sample (~5 KB) - 30 articles
- **License**: Open data for educational purposes

## How to Access

### Option 1: Local Dataset (Included)
```bash
# Dataset location
data/social_fake_news_sample.csv

# Already included in repository for quick start
```

### Option 2: Auto-download (If Expanded)
```bash
python scripts/data/download_dataset.py
```

### Option 3: Manual Download
If using a larger dataset:
1. Download from [Kaggle](https://www.kaggle.com) or [UCI ML](https://archive.ics.uci.edu/ml/)
2. Place in `data/raw/`
3. Run preprocessing: `python scripts/preprocess.py`

## Dataset Structure

### CSV Columns

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| post_id | int | Unique post identifier | 1, 2, 3... |
| author | string | Username of article poster | user_1, user_2 |
| mentioned_user | string | User referenced in article | user_3, user_5 |
| likes | int | Number of likes received | 45, 120, 95 |
| shares | int | Number of shares/retweets | 10, 40, 30 |
| comments | int | Number of comments | 12, 18, 15 |
| text_length | int | Character count of article | 140, 90, 88 |
| suspicious_word_count | int | Count of flagged suspicious words | 1, 6, 5 |
| fake_label | int | Target: 0=Real, 1=Fake | 0, 1, 1 |

### Data Statistics

```
Total Rows: 30 articles
Columns: 9 features
Missing Values: None (clean dataset)

Label Distribution:
  - Real (0): 18 articles (60%)
  - Fake (1): 12 articles (40%)

Engagement Range:
  - Likes: 26 to 152
  - Shares: 4 to 57
  - Comments: 5 to 24
```

## Data Dictionary

### Post Information
- **post_id**: Unique identifier for each article
- **author**: Creator/poster of the article
- **mentioned_user**: Other account referenced in the article

### Engagement Metrics
- **likes**: Direct engagement measure (higher = more popular)
- **shares**: Viral measure (higher = more spread)
- **comments**: Discussion measure (higher = more discussion)

### Content Features
- **text_length**: Article length in characters
  - Short: < 100 characters
  - Medium: 100-130 characters
  - Long: > 130 characters

- **suspicious_word_count**: Number of words flagged as suspicious
  - Low: 0-2 words
  - Medium: 3-5 words
  - High: 6+ words

### Target Variable
- **fake_label**: Classification target
  - 0 = Real news article
  - 1 = Fake news article

## Key Insights

### Fake vs Real Articles
| Metric | Fake | Real |
|--------|------|------|
| Average Likes | 127 | 48 |
| Average Shares | 44 | 11 |
| Average Comments | 19 | 10 |
| Avg Suspicious Words | 5.8 | 0.9 |

**Pattern**: Fake articles tend to have higher engagement AND more suspicious language!

## Data Quality

✅ **Strengths**:
- Complete (no missing values)
- Balanced classes (60/40 split)
- Clean (no duplicates)
- Well-formatted

⚠️ **Limitations**:
- Small sample size (30 articles)
- One network domain
- Limited text features
- Simulated data for education

## How to Load the Dataset

### Python - Pandas
```python
import pandas as pd

# Load dataset
df = pd.read_csv('data/social_fake_news_sample.csv')

# Basic info
print(df.head())
print(df.info())
print(df.describe())
```

### Python - Direct
```python
# Load features and labels
X = df.drop('fake_label', axis=1)
y = df['fake_label']
```

## Data Preprocessing

### Cleaning Steps (Already Done)
1. ✅ Removed duplicates
2. ✅ Checked for missing values
3. ✅ Validated data types
4. ✅ Created test/train split

### Feature Engineering Ideas
- Engagement ratio (shares/likes)
- Dominance score (suspicious_word_count/text_length)
- Network centrality features (from graph analysis)

## Citation

If using this dataset in research or projects, cite as:

```
Social Network Fake News Dataset
Description: Small dataset for demonstration and learning
Date: 2026-03-24
Domain: Social media and news classification
```

## License & Usage

- **License**: Open data for educational use
- **Restrictions**: None for learning projects
- **Commercial Use**: Allowed with attribution
- **Modification**: Free to modify for your needs

## Related Resources

- [Kaggle Fake News Datasets](https://www.kaggle.com/search?q=fake+news)
- [UCI ML Repository](https://archive.ics.uci.edu/ml/)
- [Hugging Face Datasets](https://huggingface.co/datasets)

## Questions?

Check `README.md` for project overview, or see individual scripts for data loading examples.

---

**Dataset Last Updated**: 2026-03-24  
**Version**: 1.0 (Sample/Educational)
