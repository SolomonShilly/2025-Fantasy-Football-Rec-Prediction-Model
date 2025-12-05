import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

# ------------------------------
# Load and Clean Data
# ------------------------------
df_wr = pd.read_csv('df.csv')
df_qb = pd.read_csv('qbdf.csv')

# Remove commas from yardage and convert to float
df_wr['recYds'] = df_wr['recYds'].astype(str).str.replace(',', '', regex=False).astype(float)

# Sort by WR and year to enable shifting
df_wr = df_wr.sort_values(by=['name', 'year']).reset_index(drop=True)

# Generate "next year" targets
df_wr['tgtsNext'] = df_wr.groupby('name')['tgts'].shift(-1)
df_wr['recNext'] = df_wr.groupby('name')['rec'].shift(-1)
df_wr['recYdsNext'] = df_wr.groupby('name')['recYds'].shift(-1)
df_wr['recTDNext'] = df_wr.groupby('name')['recTD'].shift(-1)

# Derived features
df_wr['recYdsPer'] = df_wr['recYds'] / df_wr['rec'].replace(0, pd.NA)
df_wr['yearNext'] = df_wr['year'] + 1
df_wr['qb_merge_year'] = df_wr['yearNext'] - 2  # QB stats 2 years prior

# Rename QB columns
df_qb_renamed = df_qb.rename(columns={
    'year': 'qb_year',
    'qbr': 'qb_qbr',
    'plays': 'qb_plays',
    'epa': 'qb_epa',
    'sack': 'qb_sack',
    'raw': 'qb_raw'
})

# Merge QB stats onto WR data
df_model = pd.merge(
    df_wr,
    df_qb_renamed,
    left_on=['team', 'qb_merge_year'],
    right_on=['team', 'qb_year'],
    how='left'
)

# ------------------------------
# Feature Engineering
# ------------------------------
features = [
    'rec', 'tgts', 'recYdsPer',
    'yac', 'firstDowns',
    'qb_qbr', 'qb_plays', 'qb_epa', 'qb_sack'
]

# Filter for training rows with known next-year outcomes
print("Initial rows:", df_model.shape[0])
df_model_before = df_model.copy()
df_model = df_model.dropna(subset=features + ['tgtsNext', 'recNext', 'recYdsNext', 'recTDNext'])
dropped = df_model_before.loc[~df_model_before.index.isin(df_model.index)]
print("Dropped rows due to missing data:", dropped.shape[0])
dropped.to_csv("dropped_rows.csv", index=False)

# ------------------------------
# Training / Test Splits
# ------------------------------
# Exclude 2024 from training
train_data = df_model[df_model['year'] < 2023]

X = train_data[features]
y_tgts = train_data['tgtsNext']
y_rec = train_data['recNext']
y_yds = train_data['recYdsNext']
y_td = train_data['recTDNext']

X_train_yds, X_test_yds, y_train_yds, y_test_yds = train_test_split(X, y_yds, test_size=0.2, random_state=42)
X_train_tgts, X_test_tgts, y_train_tgts, y_test_tgts = train_test_split(X, y_tgts, test_size=0.2, random_state=42)
X_train_rec, X_test_rec, y_train_rec, y_test_rec = train_test_split(X, y_rec, test_size=0.2, random_state=42)
X_train_td, X_test_td, y_train_td, y_test_td = train_test_split(X, y_td, test_size=0.2, random_state=42)

# ------------------------------
# Model Training
# ------------------------------
model_tgts = RandomForestRegressor(n_estimators=300, random_state=42).fit(X_train_tgts, y_train_tgts)
model_rec = RandomForestRegressor(n_estimators=300, random_state=42).fit(X_train_rec, y_train_rec)
model_yds = RandomForestRegressor(n_estimators=300, random_state=42).fit(X_train_yds, y_train_yds)
model_td = RandomForestRegressor(n_estimators=300, random_state=42).fit(X_train_td, y_train_td)

# ------------------------------
# Evaluation
# ------------------------------
def evaluate(model, X_test, y_test, label):
    preds = model.predict(X_test)
    print(f"\n{label} Prediction:")
    print("MSE:", mean_squared_error(y_test, preds))
    print("R² :", r2_score(y_test, preds))

evaluate(model_yds, X_test_yds, y_test_yds, "Yards")
evaluate(model_tgts, X_test_tgts, y_test_tgts, "Targets")
evaluate(model_rec, X_test_rec, y_test_rec, "Receptions")
evaluate(model_td, X_test_td, y_test_td, "Touchdowns")

# ------------------------------
# Predict for 2025 Season
# ------------------------------
# Use WRs from 2024 to predict their 2025 season
df_2024 = df_wr[df_wr['year'] == 2023].copy()
df_2024['qb_merge_year'] = 2022  # merge with 2023 QB stats

df_2025 = pd.merge(
    df_2024,
    df_qb_renamed,
    left_on=['team', 'qb_merge_year'],
    right_on=['team', 'qb_year'],
    how='left'
).rename(columns={'name': 'player'})

# Drop rows with missing features
df_2025 = df_2025.dropna(subset=features)

# Predict stats
X_2025 = df_2025[features]
df_2025['projTgts_2025'] = model_tgts.predict(X_2025)
df_2025['projRec_2025'] = model_rec.predict(X_2025)
df_2025['projYds_2025'] = model_yds.predict(X_2025)
df_2025['projTD_2025'] = model_td.predict(X_2025)

# Fantasy points (PPR scoring)
df_2025['projFantasyPts_2025'] = (
    df_2025['projRec_2025'] +
    (df_2025['projYds_2025'] / 10) #+
    #(df_2025['projTD_2025'] * 6)
)

# ------------------------------
# Output
# ------------------------------
df_2025_sorted = df_2025.sort_values(by='projFantasyPts_2025', ascending=False)
df_2025_sorted = df_2025.sort_values(by='projYds_2025', ascending=False)
df_2025_sorted.to_csv("FantasyProjections_2025.csv", index=False)
df_2025_sorted = df_2025_sorted.rename(columns={'name_x': 'player', 'name_y': 'qb'})


print("\nTop 20 Projected WRs for 2025:")
print(df_2025_sorted[['player', 'team', 'projTgts_2025', 'projRec_2025',
                      'projYds_2025', 'projTD_2025', 'projFantasyPts_2025']].head(20))
print(df_2025_sorted[['player', 'team', 'projTgts_2025', 'projRec_2025',
                      'projYds_2025']].head(20))

df_actual_2024 = pd.read_csv("WRstats2024.csv")  # must include player, team, rec, recYds, recTD, etc.
# Suppose these are the columns you want numeric
cols = ['recYds']
for col in cols:
    df_actual_2024[col] = df_actual_2024[col].astype(str).str.replace(',', '', regex=False)

df_compare = pd.merge(
    df_2025_sorted[['player', 'team', 'projRec_2025', 'projYds_2025', 'projTD_2025']],
    df_actual_2024[['player', 'team', 'rec', 'recYds', 'recTD']],
    on=['player', 'team'],
    how='inner'
)

# Receiving Yards
mae_yds = mean_absolute_error(df_compare['recYds'], df_compare['projYds_2025'])
mse_yds = mean_squared_error(df_compare['recYds'], df_compare['projYds_2025'])
r2_yds = r2_score(df_compare['recYds'], df_compare['projYds_2025'])

print(f"Yards - MAE: {mae_yds:.1f}, R²: {r2_yds:.2f}")
mae_rec = mean_absolute_error(df_compare['rec'], df_compare['projRec_2025'])
r2_rec = r2_score(df_compare['rec'], df_compare['projRec_2025'])

mae_td = mean_absolute_error(df_compare['recTD'], df_compare['projTD_2025'])
r2_td = r2_score(df_compare['recTD'], df_compare['projTD_2025'])

print(f"Receptions - MAE: {mae_rec:.1f}, R²: {r2_rec:.2f}")
print(f"Touchdowns - MAE: {mae_td:.1f}, R²: {r2_td:.2f}")

from scipy.stats import spearmanr

# Merge predicted 2025 projections (used for comparison) with actual 2024 data
df_compare = pd.merge(
    df_2025_sorted[['player', 'team', 'projYds_2025']],
    df_actual_2024[['player', 'team', 'recYds']],
    left_on=['player', 'team'],
    right_on=['player', 'team'],
    how='inner'
)

# Spearman rank correlation
spearman_corr, _ = spearmanr(df_compare['projYds_2025'], df_compare['recYds'])
print(f"Spearman Rank Correlation: {spearman_corr:.2f}")

# Top-10 overlap
top10_model = set(df_2025_sorted['player'].head(10))
top10_actual = set(df_actual_2024['player'].head(10))
top10_overlap = len(top10_model & top10_actual)
print(f"Top-10 Overlap: {top10_overlap}/10")
