import pandas as pd


import sqlite3
# connect db
conn = sqlite3.connect("SeniorProject.db")
print("Database is connect successfully!")
cursor = conn.cursor()

co2 = pd.read_sql_query("SELECT * FROM estimated_co2", conn)
venue = pd.read_sql_query("SELECT * FROM venue", conn)
cost = pd.read_sql_query("SELECT * FROM cost", conn)


# Load the datasets
# cost = pd.read_csv('Dataset/new_cost.csv')
# venue = pd.read_csv('Dataset/updated_venue.csv')
# co2 = pd.read_csv('Dataset/estimated_co2.csv')

# Checking every dataset
# print('venue')
# print(venue.head(10))
# print('########')
# print()

# print('cost')
# print(cost.head(10))
# print('########')
# print()

# print('co2')
# print(co2.head(10))
# print('########')
# print()

# modify co2 to take the latest data only
co2 = co2.drop_duplicates(subset=['Latitude', 'Longitude'], keep='last')
# print(co2.head(10))
# print('########')
# print(co2.tail(10))

# Merge venue & cost on 'Latitude' and 'Longitude'
merged_data = pd.merge(venue, cost, on=['Latitude', 'Longitude'])
# print('venue & cost')
# print(merged_data.head(10))
# print(merged_data.dtypes)

# Merge the result with co2_data on 'Latitude' and 'Longitude'
merged_data = pd.merge(merged_data, co2, on=['Latitude', 'Longitude'])
# Filter required columns for optimization
merged_data = merged_data[['Latitude', 'Longitude','Facility_Name_x', 'Price', 'Co2Emission']]
# print('venue & cost & co2')
# print(merged_data.head(10))
# print(merged_data.dtypes)
# print(merged_data.tail(10))

# Check for missing values
# print(merged_data.isna().sum())

# Drop rows with missing values
data = merged_data.dropna()
print("ok")
# Import necessary modules
from pymoo.algorithms.moo.spea2 import SPEA2
from pymoo.termination import get_termination
from pymoo.optimize import minimize
from pymoo.core.problem import ElementwiseProblem
import numpy as np


# Define the optimization problem
class MyProblem(ElementwiseProblem):
    def __init__(self, data):
        # Get the bounds correctly
        xl = data[['Latitude', 'Longitude']].min().values # lower bound (min value of latitude and longitude)
        xu = data[['Latitude', 'Longitude']].max().values # upper bound (max value of latitude and longitude) 
        super().__init__(n_var=2, n_obj=2, n_constr=0, xl=xl, xu=xu) 
        # n_var = number of variables (latitude and longitude)
        # n_obj = number of objectives (price and co2)
        self.data = data

    def _evaluate(self, x, out, *args, **kwargs):
        # Find the closest point in the dataset
        dist = np.sqrt((self.data['Latitude'] - x[0])**2 + (self.data['Longitude'] - x[1])**2)
        idx = dist.idxmin()
        price = self.data.loc[idx, 'Price']
        co2 = self.data.loc[idx, 'Co2Emission']
        out["F"] = [price, co2]

# Create the problem instance
problem = MyProblem(data)

# Define the SPEA2 algorithm
algorithm = SPEA2(pop_size=100)

# Define the termination criterion
termination = get_termination("n_gen", 50)

# Optimize the problem and store the result in res
res = minimize(problem, algorithm, termination, seed=1, save_history=True)

# Extract the results by storing the pareto front and solutions
pareto_front = res.F # pareto front - objective variable (price and co2)
pareto_solutions = res.X # pareto solutions - design variable (latitude and longitude)

# What is pareto front and pareto solutions?
# Pareto front: A set of non-dominated solutions in the objective space.
# Pareto solutions: A set of non-dominated solutions in the design space.

# Print the results
pareto_front = pd.DataFrame(pareto_front, columns=['Price', 'Co2Emission'])
# print('Pareto Front (Optimized Price & Co2Emission):')
# print(pareto_front)
# print('number of pareto front: ', pareto_front.count())
# print("#"*50)
# print()

pareto_solutions = pd.DataFrame(pareto_solutions, columns=['Latitude', 'Longitude'])
# print('Pareto Solutions (Optimized Latitude & Longitude):')
# print(pareto_solutions)
# print("#"*50)
# print()

solutions = pd.merge(pareto_solutions, pareto_front, right_index=True, left_index=True)
# solutions.to_csv('SPEA2_solutions.csv', index=False)



# IMPLEMENTATION METHOD 1: Find the closest venues to the user's location based on the current pareto front
user_location = [43.16758482, -80.24294547] # Could be user's input

# Calculate the distance between the user's home and all venues
data['Distance'] = np.sqrt((solutions['Latitude'] - user_location[0])**2 + (solutions['Longitude'] - user_location[1])**2)

# Sort the venues based on the distance
sorted_data = data.sort_values(by='Distance')

# Select the closest venues
closest_venues = sorted_data.head(10)  # You can adjust the number of venues as needed

# this will give you the 10 closest venues to the user's location from the pareto front
print(closest_venues)
print('done')


# IMPLEMENTATION METHOD 2: Perform SPEA2 on sorted latitude and longitude distances