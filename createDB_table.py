import sqlite3

# Create db
conn = sqlite3.connect("SeniorProject.db")
print("Database is created successfully!")
cursor = conn.cursor()
conn.commit()



cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS cost
    (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Latitude REAL,
        Longitude REAL,
        Facility_Name TEXT,
        Price REAL

    )
    """
)
print("Cost table is created successfully!")
conn.commit()


cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS venue
    (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Facility_Name TEXT,
        ODRSF_facility_type TEXT,
        Prov_Terr TEXT,
        Latitude REAL,
        Longitude REAL

    )
    """
)
print("venue table is created successfully!")
conn.commit()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS estimated_co2
    (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Latitude REAL,
        Longitude REAL,
        DateTime TEXT,
        Co2Emission REAL
    )
    """
)
print("estimated_co2 table is created successfully!")
conn.commit()

conn.close()
