
# Linear Regression Model Documentation

## Overview
This linear regression model uses lagged features from Kalshi markets to predict Polymarket's "yes_price". The model is implemented using `sklearn.linear_model.LinearRegression`.

---

## Data Preprocessing

### Feature Selection
- Features: 
  - `lag_1_kalshi_yes` to `lag_5_kalshi_yes`
- Target:
  - The first `yes_price` column from Polymarket data.

### Train/Test Split
- 20% of the data (from the beginning) is used for training.
- The remaining 80% is used for testing.

---

## Model Details

### Model
```python
from sklearn.linear_model import LinearRegression
model = LinearRegression()
```

### Training
```python
model.fit(X_train, y_train)
```

---

## Evaluation

### Metrics
```python
from sklearn.metrics import mean_squared_error, r2_score
```
- R² Score
- RMSE (Root Mean Squared Error)

### Output
```python
print(f"R² Score: {r2_score(y_test, y_pred):.4f}")
print(f"RMSE: {rmse:.4f}")
```

---

## Coefficients
The coefficients show the influence of each lag feature:

```python
for feature, coef in zip(X.columns, model.coef_):
    print(f"  {feature}: {coef:.4f}")
```

---

## Versioning & Deployment
- `sklearn` version: compatible with `1.0+`
- Model is lightweight and suitable for deployment in minimal Python environments.

## Limitations
- Assumes linear relationships between lag features and the target.
- May underperform if the actual relationships are non-linear.
