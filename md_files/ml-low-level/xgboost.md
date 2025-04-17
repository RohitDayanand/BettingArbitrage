
# XGBoost Model Documentation

## Overview
This XGBoost regression model leverages multiple lagged features from both Kalshi and Polymarket markets to predict Polymarket's `yes_price`.

---

## Data Preprocessing

### Feature Selection
Includes 20 lagged features:
- 5 lags each for:
  - `kalshi_yes`, `kalshi_no`
  - `polymarket_yes`, `polymarket_no`

### Missing Value Handling
- Rows with any missing values are dropped.

---

## Model Details

### Model
```python
from xgboost import XGBRegressor
xgb_model = XGBRegressor(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=4,
    random_state=42
)
```

### Training
```python
xgb_model.fit(X_train.values, y_train.values)
```

---

## Evaluation

### Metrics
```python
from sklearn.metrics import r2_score, mean_squared_error
```
- R² Score
- RMSE

### Output
```python
print(f"R² Score: {r2:.4f}")
print(f"RMSE: {rmse:.4f}")
```

---

## Feature Importance

Top 10 features by importance:

```python
for name, importance in sorted(zip(feature_cols, xgb_model.feature_importances_), key=lambda x: -x[1])[:10]:
    print(f"  {name}: {importance:.4f}")
```

---

## Versioning & Deployment
- `xgboost` version: >=1.0
- Well-suited for cloud deployment or integration in larger ML pipelines.

## Limitations
- Can overfit on small datasets.
- Model interpretability is lower than linear regression.
