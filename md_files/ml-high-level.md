# Machine Learning High-Level

## 🔍 Purpose

The Jupyter notebook analyizes market data from Kalshi to predict the price change for Polymarket. We are using the Golf Masters Tournament prediction data as a means to justify our hypothesis that Kalshi can be used to predict Polymarket prices. The data is cleaned, merged, and optionally visualized, potentially as a foundation for further modeling.

Key Note: The two databases that we use throughout the Jupyter notebook are referenced locally on Google Colab using SQLite. The later developments of real-time predictions and using our models for real-time trend tickers will involve using our ZipAdvisors database using SQLalchemy.

For now, in order to properly run our Google Colab file, you will need to re-upload the two databases in the contents every run of the file. It is tedious and inconvenient, but it is only for the short-term to showcase our findings on the trends between Polymarket and Kalshi.

---

## 🧩 Components

### 1. **Data Extraction & Merging**
- **Source:** SQLite database (`masters-tournament_kalshi.db`)
- **Goal:** Merge multiple related tables representing different versions of the same market as players are eliminated or market names change.
- **Key Steps:**
  - Connect to the database using `sqlite3`.
  - Identify and group related tables via substring matching.
  - Detect shared columns across groups.
  - Merge data with a UNION query sorted by timestamp.
  - Save merged output as a new table.
- **Source:** SQLite database (`num_2025_masters_winner_polymarket`)

### 2. **Data Visualization**
- **Libraries:** `pandas`, `matplotlib`
- **Purpose:** Plot the pricing trends for individual players or groups over time.
- **Functionality Hints:** These plots likely show the evolution of "Yes" and "No" market prices during the tournament.

---

## 📊 Model Training / Inference Pipeline (Implied)
Although explicit model training code is not included in the notebook, we infer the following future structure:

1. **Input:** Merged and timestamped market data.
2. **Feature Engineering:** Generate trends, moving averages, or price-based signals.
3. **Modeling:** Could use classification/regression to predict price movement or event outcomes.
4. **Output:** Predictive probabilities or trend analysis.
5. **Integration:** Results could feed into backend APIs for visualization or decision support.

---

## 🔗 Integration Points

- **Backend:** The SQLite tables can be queried by backend scripts (e.g., Flask/FastAPI) to serve data to the frontend.
- **Frontend:** Charts generated from the visualizations or model outputs can be embedded into dashboards or UIs.

---

## 📁 Dependencies Summary
- `pandas`, `matplotlib.pyplot` — Data manipulation and plotting
- `sqlite3` — Database operations
- `collections.defaultdict` — Efficient grouping of related tables

---

Let me know if you'd like me to expand this with example outputs, architecture diagrams, or model specs.
