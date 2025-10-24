try:
    age_str=input("Enter your age: ")
    age_int=int(age_str)
    print(f"You are {age_int} years old.")
except ValueError:
    print("Invalid input. Please enter a valid integer.")
finally:
    print("Program execution completed.")