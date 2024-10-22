import easygui
import random, string

"""
# Predefined variable to compare against
predefined_variable = "my_secret_value"

# Ask the user for input
user_input = easygui.enterbox("Enter something to compare:", "Input Box")

# Create custom buttons for OK, Compare, and Show Variable
choice = easygui.buttonbox("What would you like to do next?", "Options", choices=["OK", "Compare", "Show Variable"])

if choice == "OK":
    print(f"User entered: {user_input}")
elif choice == "Compare":
    if user_input == predefined_variable:
        easygui.msgbox("The input matches the predefined value!", "Comparison Result")
    else:
        easygui.msgbox("The input does not match the predefined value.", "Comparison Result")
elif choice == "Show Variable":
    easygui.msgbox(f"The predefined variable is: {predefined_variable}", "Variable Display")
"""
otp = ""
for x in range(5):
        otp = otp + str(random.choice(string.ascii_letters))
print(otp)