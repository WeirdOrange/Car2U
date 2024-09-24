import sqlite3

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def carInsert(carNo, name, seats, gear, pricepday, photo, roadtax):
    try:
        sqliteConnection = sqlite3.connect('car2u.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        sqlite_check = """ CREATE TABLE IF NOT EXISTS CAR (
                                carPlateNo varchar(12) PRIMARY KEY NOT NULL,
                                name VARCHAR(50) NOT NULL,
                                seats INT(2) NOT NULL,
                                transmission VARCHAR(10) NOT NULL,
                                pricePerDay FLOAT(5,2),
                                CarImage BLOB,
                                roadtax DATE NOT NULL)"""
        
        sqlite_insert_blob_query = """ INSERT INTO CAR
                                  (carPlateNo,name,seats,transmission,pricePerDay,carImage,roadtax) VALUES (?, ?, ?, ?, ?, ?, ?)"""

        carPhoto = convertToBinaryData(photo)
        # Convert data into tuple format
        data_tuple = (carNo, name, seats,gear,pricepday,carPhoto,roadtax)
        cursor.execute(sqlite_check)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqliteConnection.commit()
        print("Image and file inserted successfully as a BLOB into a table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")

def userInsert(custid,name,dob,email,contact,passw,pfp):
    try:
        sqliteConnection = sqlite3.connect('car2u.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        sqlite_code = """CREATE TABLE IF NOT EXISTS CUSTUSER(
                            custID varchar(5) PRIMARY KEY NOT NULL,
                            name varchar(50) NOT NULL,
                            dob date NOT NULL,
                            email varchar(100) NOT NULL,
                            contactNo varchar(15),
                            userPassword varchar(50) NOT NULL,
                            profilePic BLOB )"""
        
        sqlite_insert_blob_query = """ INSERT INTO CUSTUSER
                                  (custID,name,dob,email,contactNo,userPassword,profilePic) VALUES (?, ?, ?, ?, ?, ?, ?)"""

        profile = convertToBinaryData(pfp)
        # Convert data into tuple format
        data_tuple = (custid,name,dob,email,contact,passw,profile)
        cursor.execute(sqlite_code)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqliteConnection.commit()
        print("Image and file inserted successfully as a BLOB into a table")
        cursor.close()
    
    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")

carInsert("PGF475","Kenari",'5',"Manual",'40.00',"D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\props\loginbg.png","2026-04-01")
userInsert("C0001","Ivan Lai","2005-03-24","ivan05@gmail.com","0164075284","abcd","D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\props\signupbg.png")