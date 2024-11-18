import sqlite3
import pandas as pd

# def connect_to_db():
#     conn = sqlite3.connect("../database/SeniorProject.db", check_same_thread=False)
#     return conn

# df = pd.read_sql_query("SELECT * FROM venue", connect_to_db())
# df.to_csv('venue.csv', index=False)

# df = pd.read_sql_query("SELECT * FROM co2", connect_to_db())
# df.to_csv('co2.csv', index=False)

df = pd.read_csv('venue.csv')

print(df['Prov_terr'].unique())