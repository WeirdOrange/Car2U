import sqlite3

# Connect to the SQLite database (create one if it doesn't exist)
conn = sqlite3.connect("CAR2U2.db")
cursor = conn.cursor()

# Enable foreign key constraints
cursor.execute("PRAGMA foreign_keys = ON;")

# Table Creation with Dropping Existing Tables
cursor.executescript("""
DROP TABLE IF EXISTS Reviews;
DROP TABLE IF EXISTS BookingDetails;
DROP TABLE IF EXISTS CarDetails;
DROP TABLE IF EXISTS RentalAgency;
DROP TABLE IF EXISTS UserDetails;

CREATE TABLE UserDetails (
    userID INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    gender BINARY,
    dob DATE NOT NULL,
    contactNo VARCHAR(15) NOT NULL,
    nationality VARCHAR(100),
    profilePic BLOB,
    dateCreated DATETIME DEFAULT CURRENT_TIMESTAMP
);
                  
CREATE TABLE RentalAgency (
    agencyID INTEGER PRIMARY KEY AUTOINCREMENT,
    agencyName VARCHAR(30) NOT NULL,
    agencyLocation VARCHAR(100) NOT NULL,
    agencyEmail VARCHAR(150) NOT NULL UNIQUE,
    agencyPassword VARCHAR(100) NOT NULL,
    agencyContactNo VARCHAR(15) NOT NULL,
    agencyLogo BLOB,
    dateCreated DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE CarDetails (
    carID INTEGER PRIMARY KEY AUTOINCREMENT,
    registrationNo VARCHAR(10) UNIQUE,
    model VARCHAR(20) NOT NULL,
    colour VARCHAR(20) NOT NULL,
    fuelType VARCHAR(20) NOT NULL,
    seatingCapacity VARCHAR(20) NOT NULL,
    transmissionType VARCHAR(20) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    carImage BLOB,
    agencyID INTEGER NOT NULL,
    dateCreated DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (agencyID) REFERENCES RentalAgency(agencyID)
);

CREATE TABLE BookingDetails (
    bookingID INTEGER PRIMARY KEY AUTOINCREMENT,
    carID INTEGER NOT NULL,
    userID INTEGER NOT NULL,
    pickupDate DATE NOT NULL,
    pickupTime TIME NOT NULL,
    pickupLocation VARCHAR(100) NOT NULL,
    dropoffDate DATE NOT NULL,
    dropoffTime TIME NOT NULL,
    dropoffLocation VARCHAR(100) NOT NULL,
    numberOfDays INTEGER GENERATED ALWAYS AS (JULIANDAY(dropoffDate) - JULIANDAY(pickupDate)),
    totalAmount REAL,
    bookingStatus VARCHAR(30),
    bookingRemark VARCHAR(100),
    dateCreated DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (carID) REFERENCES CarDetails(carID),
    FOREIGN KEY (userID) REFERENCES UserDetails(userID)
);

CREATE TABLE Reviews (
    reviewID INTEGER PRIMARY KEY AUTOINCREMENT,
    ratings REAL NOT NULL,
    statement VARCHAR(200),
    bookingID INTEGER NOT NULL,
    dateCreated DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (bookingID) REFERENCES BookingDetails(bookingID)
);
""")



# Insert data into RentalAgency (Parent of CarDetails)
cursor.executemany("""
INSERT INTO RentalAgency(agencyName, agencyLocation, agencyEmail, agencyPassword, agencyContactNo) 
VALUES (?, ?, ?, ?, ?);
""", [
    ('J&C Agency', '1, Jalan Dumbar, 61300 Selangor', 'jc@gmail.com', 'jc12345', '60168346728'),
    ('Wheels Agency', '3, Jalan Othman, 61300 Selangor', 'wheels@gmail.com', 'wheels12345', '60121134587'),
    ('Auto Agency', '18, Jalan Dato Keramat, 63500 Selangor', 'auto@gmail.com', 'auto12345', '60115562546')
])

# Insert data into UserDetails (Parent of BookingDetails)
cursor.executemany("""
INSERT INTO UserDetails(name, email, password, gender, dob, contactNo, nationality) 
VALUES (?, ?, ?, ?, ?, ?, ?);
""", [
    ('Adriana Lim', 'adriana@gmail.com', 'adriana12345', 1, '2001-07-15', '60112348647', 'Malaysian'),
    ('Faiz Fitri', 'faiz@gmail.com', 'faiz12345', 0, '1975-03-02', '60186472253', 'Malaysian'),
    ('Pravin Kumar', 'pravin@gmail.com', 'pravin12345', 0, '1998-09-05', '60126657390', 'Malaysian')
])

# Insert data into CarDetails (Child of RentalAgency)
cursor.executemany("""
INSERT INTO CarDetails(registrationNo, model, colour, fuelType, seatingCapacity, transmissionType, price, agencyID) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?);
""", [
    ('PNQ 5595', 'MAZDA CX-5', 'Red', 'Petrol', '4-seater', 'Automatic', 160.00, 1),
    ('VPQ 8195', 'TOYOTA COROLLA', 'White', 'Petrol', '4-seater', 'Automatic', 180.00, 2),
    ('VQK 3099', 'MAZDA MX-5', 'Grey', 'Petrol', '2-seater', 'Manual', 220.00, 3),
    ('PQR 7466', 'TOYOTA ALPHARD', 'Copper', 'Petrol', '6-seater', 'Automatic', 200.00, 1)
])

# Insert data into BookingDetails (Child of UserDetails and CarDetails)
cursor.executemany("""
INSERT INTO BookingDetails(carID, userID, pickupDate, pickupTime, pickupLocation, dropoffDate, dropoffTime, dropoffLocation) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?);
""", [
    (2, 3, '2024-12-13', '12:30:00', 'Penang International Airport', '2024-12-30', '14:00:00', 'Penang International Airport'),
    (3, 2, '2024-11-13', '8:30:00', 'Subang International Airport', '2024-12-30', '18:00:00', 'Subang International Airport'),
    (1, 3, '2025-12-13', '9:30:00', 'Penang International Airport', '2025-12-30', '14:00:00', 'Langkawi International Airport'),
    (1, 2, '2025-11-13', '12:30:00', 'Subang International Airport', '2025-12-30', '15:00:00', 'Kuala Lumpur Sentral'),
    (2, 1, '2024-02-13', '12:30:00', 'Ipoh Railway Station', '2024-02-30', '14:00:00', 'Ipoh Railway Station'),
    (3, 1, '2024-03-01', '8:30:00', 'Penang International Airport', '2024-03-03', '18:00:00', 'Penang International Airport'),
    (2, 2, '2024-06-01', '12:30:00', 'Langkawi Ferry Terminal', '2024-06-05', '14:00:00', 'Langkawi Ferry Terminal'),
    (3, 3, '2024-07-13', '8:30:00', 'Penang Sentral', '2024-07-25', '18:00:00', 'Penang Sentral')
])

# Insert data into Reviews (Child of BookingDetails)
cursor.executemany("""
INSERT INTO Reviews(ratings, statement, bookingID) 
VALUES (?, ?, ?);
""", [
    (5, 'Great car', 1),
    (5, 'Ok', 2),
    (5, 'Ok', 3),
    (4, 'Just ok', 4),
    (5, 'Fantastic', 5),
    (3, 'Meh', 6),
    (5, 'Nice', 7),
    (2, 'Bad experience', 8)
])


# Commit changes and close the connection
conn.commit()
conn.close()

print("Database setup and data insertion completed successfully.")
