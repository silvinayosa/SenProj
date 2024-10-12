import sqlite3
import csv
# Create db
conn = sqlite3.connect("SeniorProject.db")
print("Database is connect successfully!")
cursor = conn.cursor()
conn.commit()




def insert_csv_data(csv_file_name):
    with open(csv_file_name, 'r',encoding='utf-8') as csvFile:
        cost = csv.reader(csvFile)
        next(cost) 
        for row in cost:
            Latitude,Longitude,Facility_Name,Price = row
            cursor.execute(
                """
                INSERT INTO cost (Latitude,Longitude,Facility_Name,Price) 
                VALUES (?, ?, ?, ?)
                """,
                (Latitude,Longitude,Facility_Name,Price)
            )


insert_csv_data("new_cost.csv")
conn.commit()
print("Data are inserted into DB table successfully!")
conn.close()