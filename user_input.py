from datetime import datetime  

def get_user_symbol():
    """Prompt the user to select between FNGU or FNGD."""
    print("Hello, welcome to the Automated Stock Trading program")

    while True:
        user_input = input("Please input whether you would like to select the symbol 'FNGU' or 'FNGD': ")
        cleaned_input = user_input.strip().upper()

        if cleaned_input == 'FNGU' or cleaned_input == 'FNGD':
            print(f"You have selected '{cleaned_input}'")
            return cleaned_input
        else:
            print("Invalid input. Please enter either 'FNGU' or 'FNGD'.")

def get_user_date():
    """Prompt the user to enter a date in the correct format (MM/DD/YYYY)"""
    while True:
        user_input = input("Can you please enter a date for the historical graph? Format(MM/DD/YYYY): ")
        try:
            # Try to parse the input string into a datetime object
            entered_date = datetime.strptime(user_input, "%m/%d/%Y")
            print(f"Entered date is valid: {entered_date.strftime('%m/%d/%Y')}")
            return entered_date  # Return the valid date as a datetime object
        except ValueError:
            # If parsing fails, inform the user and ask again
            print("Invalid date format. Please enter the date in the format MM/DD/YYYY.")
