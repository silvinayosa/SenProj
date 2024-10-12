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

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS user
    (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        FirstName   VARCHAR(20),
        LastName    VARCHAR(20),
        Email       VARCHAR(50),
        Password    VARCHAR(225),
        Verification_code   INT,
        Verified    TINYINT(1),
        Token       VARCHAR(225),
        Token_Expiry    DATETIME


    )
    """
)
print("user table is created successfully!")
conn.commit()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS admin
    (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserName VARCHAR(50),
        Email VARCHAR(50),
        Password VARCHAR(225)
    )
    """
)
print("admin table is created successfully!")

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS user_event
    (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        userID INTEGER,
        venueID INTEGER,
        EventName TEXT,
        No_of_Quest TEXT,
        Type_of_event VARCHAR(20),
        Date DATETIME,
        Email VARCHAR(50),
        Description TEXT,
        FOREIGN KEY (userID) REFERENCES user(ID),
        FOREIGN KEY (venueID) REFERENCES venue(ID)
    )
    """
)
print("user_event table is created successfully!")

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS register_event
    (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        userID INTEGER,
        usereventID INTEGER,
        EventName TEXT,
        Date DATETIME,
        MaxAudience INTEGER,
        RegistPrice REAL,
        FOREIGN KEY (userID) REFERENCES user(ID),
        FOREIGN KEY (usereventID) REFERENCES user_event(ID)
    )
    """
)
print("register_event table is created successfully!")

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS registration
    (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        userID INTEGER,
        registereventID INTEGER,
        RegistraionDate DATETIME,
        EventType VARCHAR(20),
        PaymentStatus BOOLEAN,
        AttendanceStatus BOOLEAN,
        FOREIGN KEY (userID) REFERENCES user(ID),
        FOREIGN KEY (registereventID) REFERENCES register_event(ID)
    )
    """
)
print("registration table is created successfully!")

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS economic_indicator
    (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Province TEXT,
        Type VARCHAR(20),
        YearlyAmount REAL
    )
    """
)
print("economic_indicator table is created successfully!")


conn.close()
