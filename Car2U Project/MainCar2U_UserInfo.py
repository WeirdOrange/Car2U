userInfo = ""
messages = []

def fetch_file_path():
    file_path = "D:\\Ivan\\Ivan\\Ivan\\Deg CS\\ALL Project\\Car2U\\Car2U Project\\assets"
    return file_path

def set_user_info(userid):
    global userInfo
    userInfo = userid

def get_user_info():
    return userInfo

def set_CarID(carID):
    global carInfo
    carInfo = carID
    
def get_Car_info():
    return carInfo

def set_BookingID(bookingID):
    global bookInfo
    bookInfo = bookingID

def get_BookingInfo():
    return bookInfo

def setRenter(agency):
    global agencyName
    agencyName = str(agency).replace(" ","")

def getRenter():
    return agencyName

def store_messages(message):
    global messages
    messages.append(message)

def fetch_messages():
    return messages