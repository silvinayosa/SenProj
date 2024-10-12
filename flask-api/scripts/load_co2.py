import sqlite3
import csv
# Create db
conn = sqlite3.connect("SeniorProject.db")
print("Database is connect successfully!")
cursor = conn.cursor()
conn.commit()




def insert_csv_data(csv_file_name):
    with open(csv_file_name, 'r',encoding='utf-8') as csvFile:
        estimated_co2 = csv.reader(csvFile)
        next(estimated_co2) 
        for row in estimated_co2:
            Latitude,Longitude,DateTime,Co2Emission = row
            cursor.execute(
                """
                INSERT INTO estimated_co2 (Latitude,Longitude,DateTime,Co2Emission) 
                VALUES (?, ?, ?, ?)
                """,
                (Latitude,Longitude,DateTime,Co2Emission)
            )


insert_csv_data("estimated_co2.csv")
conn.commit()
print("Data are inserted into DB table successfully!")
conn.close()