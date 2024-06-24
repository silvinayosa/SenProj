import sqlite3
import csv
# Create db
conn = sqlite3.connect("SeniorProject.db")
print("Database is connect successfully!")
cursor = conn.cursor()
conn.commit()




def insert_csv_data(csv_file_name):
    with open(csv_file_name, 'r',encoding='utf-8') as csvFile:
        venue = csv.reader(csvFile)
        next(venue) 
        for row in venue:
            Facility_Name,ODRSF_facility_type,Prov_Terr,Latitude,Longitude= row
            cursor.execute(
                """
                INSERT INTO venue (Facility_Name,ODRSF_facility_type,Prov_Terr,Latitude,Longitude) 
                VALUES (?, ?, ?, ?,?)
                """,
                (Facility_Name,ODRSF_facility_type,Prov_Terr,Latitude,Longitude)
            )


insert_csv_data("updated_venue.csv")
conn.commit()
print("Data are inserted into DB table successfully!")
conn.close()