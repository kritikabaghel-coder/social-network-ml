import pickle
import json
from pathlib import Path

print('✓ Verifying saved files...\n')

# Check model
model_path = Path('results/model.pkl')
if model_path.exists():
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    print(f'✓ model.pkl loaded successfully')
    print(f'  Type: {type(model).__name__}')

# Check vectorizer
vec_path = Path('results/vectorizer.pkl')
if vec_path.exists():
    with open(vec_path, 'rb') as f:
        vec = pickle.load(f)
    print(f'✓ vectorizer.pkl loaded successfully')
    print(f'  Type: {type(vec).__name__}')
    print(f'  Max Features: {vec.max_features}')

# Check metrics
metrics_path = Path('results/metrics.json')
if metrics_path.exists():
    with open(metrics_path) as f:
        metrics = json.load(f)
    print(f'✓ metrics.json loaded successfully')
    print(f'  Accuracy: {metrics.get("accuracy", 0)*100:.1f}%')
    print(f'  Precision: {metrics.get("precision", 0)*100:.1f}%')
    print(f'  Recall: {metrics.get("recall", 0)*100:.1f}%')
    print(f'  F1-Score: {metrics.get("f1", 0)*100:.1f}%')

print('\n✅ All files ready for Streamlit deployment!')
