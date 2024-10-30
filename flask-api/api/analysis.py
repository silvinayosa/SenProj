import pandas as pd

df1 = pd.read_csv('../Database/database-csv/co2-csv/Alberta_avg_co2.csv')
df2 = pd.read_csv('../Database/database-csv/co2-csv/British Columbia_avg_co2.csv')
df3 = pd.read_csv('../Database/database-csv/co2-csv/New Brunswick_avg_co2.csv')
df4 = pd.read_csv('../Database/database-csv/co2-csv/Nova Scotia_avg_co2.csv')
df5 = pd.read_csv('../Database/database-csv/co2-csv/Ontario_avg_co2.csv')
df6 = pd.read_csv('../Database/database-csv/co2-csv/Quebec_avg_co2.csv')

# Store all DataFrames in a list
dfs = [df1, df2, df3, df4, df5, df6]

avg=[]

# Loop through each DataFrame in the dfs list
for i, df in enumerate(dfs, start=1):
    avg.append(df['CO2'].mean())

print(avg)
