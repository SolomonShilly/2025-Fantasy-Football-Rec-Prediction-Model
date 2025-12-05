import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Load data
df_wr = pd.read_csv('df.csv')
df_qb = pd.read_csv('QBdf.csv')
print(df_qb.dtypes)
print(df_wr.dtypes)
# Clean WR data
df_wr['recYds'] = df_wr['recYds'].astype(str).str.replace(',', '').astype(float)

df_wr = df_wr.sort_values(by=['name', 'year']).reset_index(drop=True)
df_wr['tgtsNext'] = df_wr.groupby('name')['tgts'].shift(-1)
df_wr['recNext'] = df_wr.groupby('name')['rec'].shift(-1)
df_wr['recYdsNext'] = df_wr.groupby('name')['recYds'].shift(-1)
df_wr['yearNext'] = df_wr['year'] + 1  # We'll match QB from two years prior
df_wr['recTDNext'] = df_wr.groupby('name')['recTD'].shift(-1)


# Prepare QB data to join: rename year for clarity
df_qb_renamed = df_qb.rename(columns={
    'year': 'qb_year',
    'qbr': 'qb_qbr',
    'plays': 'qb_plays',
    'epa': 'qb_epa',
    'sack': 'qb_sack',
    'raw': 'qb_raw'
})

# Merge QB stats from 2 years before the WR's "target" year
df_wr['qb_merge_year'] = df_wr['yearNext'] - 2

df_model = pd.merge(
    df_wr,
    df_qb_renamed,
    left_on=['team', 'qb_merge_year'],
    right_on=['team', 'qb_year'],
    how='left'
)

# Only keep rows where we *know* the next year's tgts and rec
df_model = df_model.dropna(subset=['tgtsNext', 'recNext'])

features = [
    'gp', 'tgts',
    'yac', 'firstDowns',
    'qb_qbr', 'qb_plays', 'qb_epa', 'qb_sack'
]

# Drop rows with missing QB stats
df_model = df_model.dropna(subset=features)
df_model = df_model.dropna(subset=['tgtsNext', 'recNext', 'recYdsNext'])
df_model = df_model.dropna(subset=['recTDNext'])


X = df_model[features]
y_tgts = df_model['tgtsNext']
y_rec = df_model['recNext']
y_yds = df_model['recYdsNext']
y_td = df_model['recTDNext']

X_train_yds, X_test_yds, y_train_yds, y_test_yds = train_test_split(X, y_yds, test_size=0.18, random_state=42)
X_train, X_test, y_train_tgts, y_test_tgts = train_test_split(X, y_tgts, test_size=0.18, random_state=42)
X_train_rec, X_test_rec, y_train_rec, y_test_rec = train_test_split(X, y_rec, test_size=0.18, random_state=42)
X_train_td, X_test_td, y_train_td, y_test_td = train_test_split(X, y_td, test_size=0.18, random_state=42)

model_td = RandomForestRegressor(n_estimators=50, random_state=42)
model_td.fit(X_train_td, y_train_td)


# Train separate models
model_yds = RandomForestRegressor(n_estimators=50, random_state=42)
model_yds.fit(X_train_yds, y_train_yds)

model_tgts = RandomForestRegressor(n_estimators=50, random_state=42)
model_tgts.fit(X_train, y_train_tgts)

model_rec = RandomForestRegressor(n_estimators=50, random_state=42)
model_rec.fit(X_train_rec, y_train_rec)

# Evaluate
print("\nYards Prediction:")
print("MSE:", mean_squared_error(y_test_yds, model_yds.predict(X_test_yds)))
print("R²:", r2_score(y_test_yds, model_yds.predict(X_test_yds)))

print("Targets Prediction:")
print("MSE:", mean_squared_error(y_test_tgts, model_tgts.predict(X_test)))
print("R²:", r2_score(y_test_tgts, model_tgts.predict(X_test)))

print("\nReceptions Prediction:")
print("MSE:", mean_squared_error(y_test_rec, model_rec.predict(X_test_rec)))
print("R²:", r2_score(y_test_rec, model_rec.predict(X_test_rec)))

print("\nTouchdowns Prediction:")
print("MSE:", mean_squared_error(y_test_td, model_td.predict(X_test_td)))
print("R²:", r2_score(y_test_td, model_td.predict(X_test_td)))

# Get only 2024 WR data
df_2024 = df_wr[df_wr['year'] == 2023].copy()

# Attach 2023 QB data (for 2025 prediction)
df_2024['qb_merge_year'] = 2024 - 2  # 2023
df_2025 = pd.merge(
    df_2024,
    df_qb_renamed,
    left_on=['team', 'qb_merge_year'],
    right_on=['team', 'qb_year'],
    how='left'
)

# Drop rows missing QB features
df_2025 = df_2025.dropna(subset=features)

X_2025 = df_2025[features]
df_2025['projYds_2025'] = model_yds.predict(X_2025)
df_2025['projTgts_2025'] = model_tgts.predict(X_2025)
df_2025['projRec_2025'] = model_rec.predict(X_2025)
df_2025['projTD_2025'] = model_td.predict(X_2025)

# Fantasy points: 1 pt per 10 yds, 1 per rec, 6 per TD
df_2025['projFantasyPts_2025'] = (df_2025['projYds_2025'] / 10) + df_2025['projRec_2025'] + (df_2025['projTD_2025'] * 6)


# Sort by most projected fantasy points
df_2025_sorted = df_2025.sort_values(by='projFantasyPts_2025', ascending=False)

# Show top 20
print(df_2025_sorted[['name_x', 'team', 'projTgts_2025', 'projRec_2025', 'projYds_2025', 'projTD_2025', 'projFantasyPts_2025']].head(20))
df_2025_sorted[['name_x', 'team', 'projTgts_2025', 'projRec_2025', 'projYds_2025', 'projTD_2025', 'projFantasyPts_2025']].to_csv("Predictions2024.csv")
