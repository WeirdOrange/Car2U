import sqlite3

def Database(): #creating connection to database and creating table
    global conn, cursor
    conn = sqlite3.connect("car2u.db")
    # Enable access to columns by name
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

def next(i):
    i = i + 6
    cursor.execute(f"""SELECT * FROM CarDetails WHERE carID > '{i}' LIMIT 6""")
    result = cursor.fetchall()
    return i, result

def carlist():
    Database()
    cursor.execute("""SELECT * FROM CarDetails LIMIT 6""")
    result = cursor.fetchall()
    x=1
    ask = 1
    i=6

    while ask == 1:
        next(i)
        x=1
        while x < 7 :
            for row in result:
                if result == None:
                    break
                else:
                    frame = "item_frame"+str(x)
                    name_car = row['model'] #Fetching data from database
                    seaters_car = row['seatingCapacity']
                    transmission_car = row['transmissionType']
                    price_car = row['price']
                    print(f"{frame}. Username: {name_car}, Age: {seaters_car}, Email: {transmission_car},price: {price_car}")
                    x=x+1
        ask = int(input("next:"))
    

carlist()