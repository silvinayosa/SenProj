import sqlite3
import pandas as pd
from pymoo.algorithms.moo.spea2 import SPEA2
from pymoo.termination import get_termination
from pymoo.optimize import minimize
from pymoo.core.problem import ElementwiseProblem
import numpy as np

event_type_mapping = {
    "playground": ["Parties"],
    "pool": ["Parties", "Fundraisers"],
    "trail": ["Fundraisers"],
    "park": ["Parties", "Weddings", "Fundraisers"],
    "community centre": ["Corporate Events", "Parties", "Seminars", "Weddings", "Fundraisers"],
    "gym": ["Corporate Events", "Parties"],
    "athletic park": ["Fundraisers", "Corporate Events"],
    "arena": ["Corporate Events", "Fundraisers", "Parties"],
    "rink": ["Corporate Events", "Fundraisers"],
    "skate park": ["Parties"],
    "splash pad": ["Parties"],
    "stadium": ["Corporate Events", "Fundraisers"],
    "beach": ["Parties", "Weddings"],
    "marina": ["Parties", "Weddings"],
    "casino": ["Corporate Events", "Parties", "Fundraisers"],
    "race track": ["Corporate Events", "Fundraisers"],
    "miscellaneous": ["Corporate Events", "Parties", "Fundraisers", "Weddings"],
    "sports field": ["Corporate Events", "Fundraisers", "Parties"],
    "studio": ["Corporate Events", "Parties", "Seminars", "Weddings"]
}

class MyProblem(ElementwiseProblem):
    def __init__(self, data):
        super().__init__(n_var=1, n_obj=2, n_constr=0, xl=0, xu=len(data)-1)  # Use row indices as variables
        self.data = data

    def _evaluate(self, x, out, *args, **kwargs):
        # Convert the index (x[0]) to the corresponding row
        idx = int(x[0])  # Ensure x is an integer
        price = self.data.iloc[idx]['Price']
        co2 = self.data.iloc[idx]['CO2']
        out["F"] = [price, co2]


def connect_to_db():
    conn = sqlite3.connect("../database/SeniorProject.db", check_same_thread=False)
    return conn

def optimize_venues(user_location, user_province, event_type, user_budget, user_guest):
    conn = connect_to_db()
    print("Database is connect successfully!")
    venue = pd.read_csv('venue.csv')
    # sort venue columns
    venue = venue[venue['Prov_terr'] == user_province]
    venue = venue[venue['Price'] <= user_budget]
    venue = venue[venue['Max_audience'] >= user_guest]
    venue2 = venue[venue["ODRSF_facility_type"].isin([facility for facility, events in event_type_mapping.items() if event_type in events])]
    venue2 = venue2[['ID', 'Latitude', 'Longitude', 'Facility_Name', 'Price', 'ODRSF_facility_type']]
    
    # Step 1: Get the list of IDs from venue2
    venue_ids = venue2['ID'].tolist()
    
    # Step 2: Convert the list of IDs to a string for use in the SQL query
    id_string = ', '.join(map(str, venue_ids))  # Convert list of integers to comma-separated string
    
    co2_query = f"""
    SELECT venueID, MAX(Date) AS Date, CO2
    FROM co2
    WHERE venueID IN ({id_string})
    GROUP BY venueID
    ORDER BY venueID
    """
    
    co2 = pd.read_sql_query(co2_query, conn)
    merged_data = pd.merge(venue2, co2, left_on='ID', right_on='venueID', how='inner')
    merged_data = merged_data.drop(columns=['venueID'])
    merged_data.sort_values(by='ID', inplace=True)
    print("merged_data:", merged_data)
    
    problem = MyProblem(merged_data)  
    algorithm = SPEA2(pop_size=100)
    termination = get_termination("n_gen", 50)
    res = minimize(problem, algorithm, termination, seed=1, save_history=True)

    # Extract indices and objectives
    pareto_indices = res.X[:, 0].astype(int)
    pareto_front = pd.DataFrame(res.F, columns=['Price', 'CO2'])

    pareto_solutions = merged_data.iloc[pareto_indices].reset_index(drop=True)
    
    closest_venues = pd.concat([pareto_solutions, pareto_front], axis=1)

    # Display results
    print("closest_venues:", closest_venues)
    print("closest_venues:", closest_venues.info())
    closest_venues = closest_venues.groupby('ID', as_index=False).first()


    # You can convert the closest venues to a list of dictionaries for JSON response
    closest_venues_list = closest_venues.to_dict(orient='records')
    
    return closest_venues_list
    
    
solution = optimize_venues([49.84654685,-99.94693864], 'Manitoba', 'Parties', 1500, 10)
solution = pd.DataFrame(solution)
solution.to_csv('solution.csv')
print(solution)