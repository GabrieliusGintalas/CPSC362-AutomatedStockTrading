def get_user_input():
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

