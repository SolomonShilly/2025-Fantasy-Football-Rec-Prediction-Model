# 2025 WR & TE Fantasy Football Prediction Model

## Overview
This project predicts Wide Receiver (WR) and Tight End (TE) stats for the 2025-2026 NFL season. Using historical player statistics and quarterback performance, the model ranks players and projects targets, receptions, yards, and touchdowns.  

The model performed very well in ranking players accurately, although the exact projected statistics need further refinement. In other words, the top-ranked players align closely with real-world outcomes, but the numerical projections differ slightly.  

The goal is to provide a foundation for impactful fantasy football predictions and demonstrate data-driven decision-making.

---

## Data Collection
The project uses **web scraping** to gather player statistics:

- `StatsScrapper.py` – Collects WR stats from ESPN for multiple seasons.  
- `QBInfoScrap.py` – Collects quarterback stats for multiple seasons.  

Scraped data is stored in CSV files for later processing.

---

## Data Cleaning & Preparation
Scripts clean and merge the raw data:

- `DataCleaning.py` & `QBDataCleaning.py` – Standardize and merge WR and QB datasets.  
- `DataExamination.py` – Filters, inspects, and prepares data for modeling.  

Key transformations include:
- Converting yardage and targets to numeric types.
- Shifting stats to align each WR season with their following year's performance.
- Merging QB stats from prior seasons for contextual features.

---

## Model & Predictions
The prediction model uses **Random Forest Regressors** to forecast:
- Targets (`tgts`)
- Receptions (`rec`)
- Receiving yards (`recYds`)
- Touchdowns (`recTD`)
- Fantasy points (PPR scoring)

Scripts involved:
- `RecModel.py` & `RecPred.py` – Train models, evaluate accuracy, and generate 2025 projections.  

**Evaluation Metrics:**
- Mean Squared Error (MSE)
- R² score
- Spearman Rank Correlation for ranking accuracy
- Top-10 overlap between predicted and actual outcomes  

The model outputs a ranked list of projected players in CSV format for further analysis.

---

## Results
- Player rankings match closely with expected performance.  
- Numerical projections require refinement but provide a strong baseline.  
- CSV outputs include:
  - `FantasyProjections_2025.csv` – Ranked WR/TE projections.
  - `Predictions2024_B.csv` – Detailed projection metrics.
  - `BrandNewPredictions20244.csv` – Latest consolidated projections.  

---

## Next Steps
- Refine statistical projections to reduce deviation from actual results.
- Explore alternative machine learning models or feature engineering techniques.
- Expand analysis to include additional positional stats or advanced metrics.

---

## How to Use
1. Clone the repository.
2. Install dependencies: `pandas`, `selenium`, `scikit-learn`.
3. Run `StatsScrapper.py` and `QBInfoScrap.py` to gather data.
4. Clean and merge datasets with `DataCleaning.py` and `QBDataCleaning.py`.
5. Train and predict using `RecModel.py` or `RecPred.py`. ("RecPred.py is recommended)
6. Analyze output CSV files to view projected rankings and stats.

---

## Goal
This project demonstrates **data-driven sports analytics**. It serves as a tool for fantasy football predictions.
