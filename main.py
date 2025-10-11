"""
Goal Tracker
A simple command-line application to track personal goals. (currently)

Features:
- Add & save goals to a file
- view goals 
- finish goals

Future intended features:
- adding date and time to goals (e.g. time of creation and deadline/time)
- migrate from text-based to GUI-based application 
- track success rate of goals
- categorization --> e.g. personal, school, health, etc..; tags; urgency/importance (kinda similar to the reminders app --> !, !!, !!!, etc. (maybe more efficent way?) )
- proof that you actually did it? (unrealistic perhaps but could work --> e,g, upload a photo & something analyzes it to confirm that ur not bsing it)
- maybe a calendar view
- maybe collaboration with others?
"""


import datetime
import os
import time
import json

goals = []

""" Save to a file """

# ------------------------- Save Goals -------------------------
def save_goals():
    with open("goals.json", "w") as f:
        json.dump(goals, f, indent = 4)

# ------------------------- Load Goals -------------------------
def load_goals():
    global goals
    try:
        with open("goals.json", "r") as f:
            goals = json.load(f)
    except FileNotFoundError:
        print("file not found error.")
        goals = []
    except json.JSONDecodeError:
        print("json.JSONDecode Error")
        goals = []

# ------------------------- Add Goal -------------------------
def add_goal():
    goal = input("Enter a goal: ")
    goals.append(goal)

    save_goals()

    print("Saved Successfully!")

# ------------------------- View Goals -------------------------
def view_goals():
    if not goals:
        print("No goals yet!")
    else:
        print("Your goals are:")
        for i in range(len(goals)):
            print(f"{i + 1}. {goals[i]}")

# ------------------------- Finish a Goal -------------------------
def finished_goal():
    view_goals()

    if not goals:
        return
    
    try:
        num = int(input("Which goal did you finish? (number): "))
        if 1 <= num <= len(goals):
            finished = input("Did you finish this goal? (y/n): ").strip().lower()
            while finished not in ['y', 'n']:
                finished = input("Please enter 'y' or 'n' for yes or no respectively: ").strip().lower()
            if finished == 'y':
                removed_goal = goals.pop(num - 1)
                save_goals()
                print(f"Great job on finishing: {removed_goal}!")
            elif finished == 'n':
                print("Maybe next time!")
                remove_yes_no = input("Do you want to remove this goal regardless? (y/n): ").strip().lower()
                if remove_yes_no == 'y' or remove_yes_no == 'yes':
                    removed_goal = goals.pop(num - 1)
                    save_goals()
                else:
                    print("Goal not removed.")
            else:
                print("Invalid input. Please enter 'y' or 'n'.")
    except:
        print("Please enter a valid number.")

def main():
    running = True
    load_goals()

    while running:

        time.sleep(1)
        print("\n ------------------------------ Goal Tracker ------------------------------")
        print("1. Add a Goal")
        print("2. View Goals")
        print("3. Finish a Goal")
        print("4. Exit")

        choice = input("Choose an option (1-4): ").strip()

        if choice == '1':
            add_goal()
        elif choice == '2':
            view_goals()
        elif choice == '3':
            finished_goal()
        elif choice == '4':
            running = False
            print("Exiting Goal Tracker.")
        else:
            print("Invalid choice. Please select a number between 1 and 4.")

if __name__ == "__main__":
    main()