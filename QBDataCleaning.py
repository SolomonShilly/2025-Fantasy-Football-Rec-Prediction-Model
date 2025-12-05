import pandas as pd

df1 = pd.read_csv('QBstats2018.csv')
df2 = pd.read_csv('QBstats2019.csv')
df3 = pd.read_csv('QBstats2020.csv')
df4 = pd.read_csv('QBstats2021.csv')
df5 = pd.read_csv('QBstats2022.csv')
df6 = pd.read_csv('QBstats2023.csv')
df7 = pd.read_csv('QBstats2024.csv')

df = pd.concat([df1, df2, df3, df4, df5, df6, df7], ignore_index=True)
print(df.dtypes)
dfSorted = df.sort_values(by=['name', 'year']).reset_index(drop=True)
dfSorted.to_csv('QBdf.csv')

