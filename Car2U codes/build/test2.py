# Validate Date entry via Parse
from dateutil.parser import parse
import datetime
while(True):
    try:
        DDate = input("Enter Date yyyymmdd: ")
        DDate = parse(DDate)  # Error Test parse
        break    # Break pulls you out of the loop
    except:
        print("INVALID Date: ",DDate)

print("Valid Date Has Been Entered: ",DDate)

#       OR

# Validate Date Entry via .strptime
while(True):
    try:
        DDate = input("Enter Date yyyymmdd: ")
        DDate = datetime.strptime(DDate, '%Y%m%d')  # Error Test .strptime
        break    # Break pulls you out of the loop
    except ValueError:
        print("INVALID Date: ",DDate)

print("Valid Date Has Been Entered: ",DDate)