import sqlite3
import pandas as pd
from pymoo.algorithms.moo.spea2 import SPEA2
from pymoo.termination import get_termination
from pymoo.optimize import minimize
from pymoo.core.problem import ElementwiseProblem
import numpy as np
#########################################################

##################################################
# Change the province abbreviations to full names #
##################################################

# def connect_to_db():
#     conn = sqlite3.connect("../database/SeniorProject.db", check_same_thread=False)
#     return conn

# df = pd.read_sql_query("SELECT * FROM venue", connect_to_db())

# province_mapping = {
#     "on": "Ontario",
#     "bc": "British Columbia",
#     "ab": "Alberta",
#     "mb": "Manitoba",
#     "sk": "Saskatchewan",
#     "qc": "Quebec",
#     "ns": "Nova Scotia",
#     "nb": "New Brunswick",
#     "nl": "Newfoundland and Labrador",
#     "pe": "Prince Edward Island",
#     "yt": "Yukon",
#     "nt": "Northwest Territories",
#     "nu": "Nunavut"
# }

# # Replace province abbreviations with full names
# df['Prov_terr'] = df['Prov_terr'].map(province_mapping)

# # Verify the changes
# print("with province name", df.head(20))

# df["Facility_Name"] = df["Facility_Name"].replace(["unknown", "Unknown Name"], pd.NA)
# # Generate new Facility_Name using full province names
# df["Facility_Name"] = df.apply(
#     lambda row: (
#         f"{row['Prov_terr']} {row['ODRSF_facility_type']}" 
#         if pd.isna(row['Facility_Name']) 
#         else row['Facility_Name']
#     ),
#     axis=1,
# )

# # Add numbering for duplicate combinations
# name_counts = {}

# def generate_name(row):
#     key = (row["Prov_terr"], row["ODRSF_facility_type"])
#     if key not in name_counts:
#         name_counts[key] = 1
#     else:
#         name_counts[key] += 1
#     suffix = f" {name_counts[key]}" if name_counts[key] > 1 else ""
#     return f"{row['Prov_terr']} {row['ODRSF_facility_type']}{suffix}"

# df["Facility_Name"] = df.apply(generate_name, axis=1)

# # Verify the updated DataFrame
# print("new df", df.head(20))

# # Save the updated DataFrame to a new CSV file
# df.to_csv('venue.csv', index=False)

# df = pd.read_csv('venue.csv')
# print(df['ODRSF_facility_type'].unique())

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
    # connect db
    conn = connect_to_db()
    print("Database is connect successfully!")
    venue = pd.read_csv('venue.csv')
    
    venue2 = venue[
    (venue['Price'] <= user_budget) &  # Price is within budget
    (venue['Prov_terr'] == user_province) &  # Province matches
    (venue['Max_audience'] >= user_guest)  # Can accommodate the number of guests
]

    venue2 = venue2[venue2["ODRSF_facility_type"].isin([facility for facility, events in event_type_mapping.items() if event_type in events])]
    
    
    co2_query = """
    SELECT venueID, MAX(Date) AS Date, CO2
    FROM co2
    GROUP BY Latitude, Longitude
    ORDER BY Latitude, Longitude
"""
    co2 = pd.read_sql_query(co2_query, conn)
    
    
    venue2 = venue2[['ID', 'Latitude', 'Longitude', 'Facility_Name', 'Price', 'ODRSF_facility_type']]

    # Merge the result with co2_data on 'Latitude' and 'Longitude'
    merged_data = pd.merge(venue2, co2, left_on='ID', right_on='venueID', how = 'left')
    merged_data = merged_data.drop(columns=['venueID'])
    
    print("merged_data:",merged_data.columns)
    data = merged_data.dropna()
    print("ok")
    # Run the SPEA2 optimization process and get the pareto front
    # SPEA2 optimization is performed first
    problem = MyProblem(data)  
    algorithm = SPEA2(pop_size=100)
    termination = get_termination("n_gen", 50)
    res = minimize(problem, algorithm, termination, seed=1, save_history=True)

    # Extract indices and objectives
    pareto_indices = res.X[:, 0].astype(int)
    pareto_front = pd.DataFrame(res.F, columns=['Price', 'CO2'])

    # Retrieve solutions and calculate distance
    pareto_solutions = merged_data.iloc[pareto_indices].reset_index(drop=True)
    pareto_solutions['Distance'] = np.sqrt(
        (pareto_solutions['Latitude'] - user_location[0])**2 +
        (pareto_solutions['Longitude'] - user_location[1])**2
    )

    # Sort by distance and select the closest solutions
    sorted_solutions = pareto_solutions.sort_values(by='Distance')
    closest_solutions = sorted_solutions.head(10)

    # Combine with objectives
    closest_venues = pd.concat([closest_solutions, pareto_front.iloc[closest_solutions.index]], axis=1)

    # Display results
    print("closest_venues:", closest_venues)
    print("closest_venues:", closest_venues.info())
    
    closest_venues['Facility_Name'] = closest_venues['Facility_Name'].fillna(closest_venues['ODRSF_facility_type'].astype(str) + str(user_province))


    # You can convert the closest venues to a list of dictionaries for JSON response
    closest_venues_list = closest_venues.to_dict(orient='records')
    
    return closest_venues_list

result = optimize_venues([49.8951, -97.1384], 'Manitoba', 'Parties', 1000, 100)

print(result)