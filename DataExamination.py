import pandas as pd

df1 = pd.read_csv('WRstats2018.csv')
df2 = pd.read_csv('WRstats2019.csv')
df3 = pd.read_csv('WRstats2020.csv')
df4 = pd.read_csv('WRstats2021.csv')
df5 = pd.read_csv('WRstats2022.csv')
df6 = pd.read_csv('WRstats2023.csv')
df7 = pd.read_csv('WRstats2024.csv')

df1['targets_per_game'] = df1['tgts'] / df1['gp'] # Convert recYds from object to int
df2['targets_per_game'] = df2['tgts'] / df2['gp'] # Convert recYds from object to int and yac
df3['targets_per_game'] = df3['tgts'] / df3['gp'] # recYds
df4['targets_per_game'] = df4['tgts'] / df4['gp']
df5['targets_per_game'] = df5['tgts'] / df2['gp']
df6['targets_per_game'] = df6['tgts'] / df3['gp']
df7['targets_per_game'] = df7['tgts'] / df4['gp']

df2['yac'] = df2['yac'].str.replace(',', '')
df2['yac'] = df2['yac'].astype(int)

# Started with 100 rec threshold, and dropped to 95
#print(df1[df1['rec']>=95].head(15).sort_values(by='tgts', ascending=False))
#print(df2[df2['rec']>=95].head(15).sort_values(by='tgts', ascending=False))
#print(df3[df3['rec']>=95].head(15).sort_values(by='tgts', ascending=False))
#print(df4[df4['rec']>=95].head(15).sort_values(by='tgts', ascending=False))

print(df1[df1['yac']>=480].sort_values(by='tgts', ascending=False))
print(df2[df2['yac']>=480].sort_values(by='tgts', ascending=False))
print(df3[df3['yac']>=480].sort_values(by='tgts', ascending=False))
print(df4[df4['yac']>=480].sort_values(by='tgts', ascending=False))

# Step 1: Filter each DataFrame
f1 = df1[df1['yac'] >= 480]
f2 = df2[df2['yac'] >= 480]
f3 = df3[df3['yac'] >= 480]
f4 = df4[df4['yac'] >= 480]

# Step 2: Get sets of names (assuming the column is called 'name')
names1 = set(f1['name'])
names2 = set(f2['name'])
names3 = set(f3['name'])
names4 = set(f4['name'])

# Step 3: Find intersection (names present in all 4)
matching_names = names2 & names4

print("Matching names across all dataframes:")
print(matching_names)

# Add a year column if not already present
df1['year'] = 2018
df2['year'] = 2019
df3['year'] = 2020
df4['year'] = 2021
df5['year'] = 2022
df6['year'] = 2023
df7['year'] = 2024

# Combine into one DataFrame
df = pd.concat([df1,df2, df3, df4, df5, df6, df7], ignore_index=True)

dfSorted = df.sort_values(by=['name', 'year']).reset_index(drop=True)
dfSorted.to_csv('df.csv')
