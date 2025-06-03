import json
# Allows for reading and writing 'habit' data to a .json file

import os
# For file and directory management
# To check if a file (like, data.json) already exits.

from datetime import datetime, timedelta
# To track when a habit was last completed, and manage streaks

# loads data from JSON file or creates a new one (data), if it doesn't exits
def load_data():
    if not os.path.exists("data.json") or os.path.getsize("data.json") == 0:
        return {"habits": []}
    with open("data.json", "r") as file:
        return json.load(file)

# saves data back to a JSON file
def save_data(data):
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

def add_habit(data):
    name = input("Enter the name of new habit: ").strip()
    category = input("Enter the category (e.g., fitness, faith, learning): ").strip()
    # Check if habit already exists
    for habit in data["habits"]:
        if habit["name"].lower() == name.lower():
            print("That habit already exists.")
            return
    # If not found, add new habit 
    habit = {
        "name": name,
        "streak": 0,
        "last_completed": None,
        "created": datetime.now().strftime("%d/%m/%Y")    
    }
    
    # Add to the list and save updated list
    data["habits"].append(habit)
    save_data(data)
    print(f"Habit '{name}' added successfully.")
    
# Mark Habit as Done
def mark_habit_done(data):
    if not data["habits"]:
        print("You have no habits to mark.")
        return
    
    print("\nWhich habit(s) did you compelete today?")
    for i, habit in enumerate(data["habits"], start=1):
        print(f"{i}. {habit['name']} (Streak: {habit['streak']})")
    
    try:
        choice = int(input("Enter the number of the habit: ").strip())
        if choice < 1 or choice > len(data["habits"]):
            print("Invalid choice.")
            return
    except ValueError:
        print("Please enter a number.")
    
    habit = data["habits"][choice - 1]

    today = datetime.now().strftime("%d/%m/%Y")
     
    if habit["last_completed"] == today:
        print(f"You've already marked '{habit["name"]}' as done today.")
        return
    
    yesterday = (datetime.now().date() - timedelta(days=1)).strftime("%d/%m/%Y")
    if habit["last_completed"] == yesterday:
        habit["streak"] += 1
    else:
        habit["streak"] = 1

    habit["last_completed"] = today
    save_data(data)
    print(f"Marked '{habit['name']}' as done! Streak: {habit['streak']}")

# View Today’s Habits and Status
def view_today(data):
    if not data["habits"]:
        print("No habits to display.")
        return
    
    today = datetime.now().strftime("%d/%m/%Y")
    print("\nToday's Habit Status.")  
    
    for habit in data["habits"]:
        done = habit["last_completed"] == today
        status = "✅ Done" if done else "❌ Not Done"
        print(f"- {habit["name"]}: {status} (Streak: {habit["streak"]})")   

# Edit or Delete a Habit
def edit_or_delete_habit(data):
    if not data["habits"]:
        print("No habits to edit or delete.")
        return 
    
    print("\nWhich habit would you like to edit or delete?")
    for i, habit in enumerate(data["habits"], start=1):
        print(f"{i}. {habit["name"]}")
        
    try:
        choice = int(input("Enter the numer: ").strip())
        if choice < 1 or choice > len(data["habits"]):
            print("Invalid choice.")
            return 
    except ValueError:
        print("Please enter a valid number.")
        return 
    
    habit = data["habits"][choice - 1]
    
    print(f"\nSelceted: {habit["name"]}")
    print("1. Rename")
    print("2. Delete")
    sub_choice = input("Choose an option: ").strip()
    
    if sub_choice == "1":
        new_name = input("Enter the new name: ")
        habit["name"] = new_name
        print("Habit renamed.")
    elif sub_choice == "2":
        confirm = input("Are you sure you want to delete this habit? (yes/no): ").strip().lower()
        if confirm == "yes":
            data["habits"].pop(choice - 1)
            print("Habit deleted.")
        else:
            print("Deletion canceled.")
    else:
        print("Invalid option")
    
    save_data(data)
    
def main():
    data = load_data()
    print("Welcome to the Habit Tracker!")
   
    # Shows a menu that let's users;
    while True:
        print("\nWhat would you like to do?")
        print("1. View today's habits")
        print("2. Add a new habit")
        print("3. Mark habit as done")
        print("4. Edit or delete habit")
        print("5. Exit")


        choice = input("Enter your choice (1-4): ").strip()

        # 1. view existing habits,
        if choice == "1":
            view_today(data)
        # 2. add new habits,
        elif choice == "2":
            add_habit(data)
        # 3. mark habit as done,
        elif choice == "3":
            mark_habit_done(data)
        # 4. edit or delete habit.   
        elif choice == "4":
            edit_or_delete_habit(data) 
        # 5. exit
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
        
if __name__ == "__main__":
    main()
