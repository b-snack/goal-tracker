"""
Goal Tracker
A simple command-line application to track personal goals. (currently)

Features:
- Add & save goals to a file
- view goals 
- finish goals

Future intended features:
- due dates
- edit goals
- colour coding for priority levels
- migrate from text-based to GUI-based application 
- track success rate of goals -> using graphs or stats or etc.
- categorization --> e.g. personal, school, health, etc..; tags; urgency/importance (kinda similar to the reminders app --> !, !!, !!!, etc. (maybe more efficent way?) )
- proof that you actually did it? (unrealistic perhaps but could work --> e,g, upload a photo & something analyzes it to confirm that ur not bsing it)
- maybe a calendar view
- maybe collaboration with others?
- repeating goals/events

Fri Oct 10, 2025: 
Added:
- Add & save goals to a file
- view goals 
- finish goals

Sat Oct 11, 2025:
- added priority + timestamps to goals
- added finished.json file for completed goals

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
    goal_text = input("Enter a goal: ")
    time_added = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    goal_priority = input("How important is this task? (!!!, !! or !): ")
    while goal_priority not in ["!!!", "!!", "!"]:
        print("Invalid input.")
        goal_priority = input("Please try again: ")
    
    goal = {
        "text": goal_text,
        "priority": goal_priority,
        "created_at": time_added,
        "completed_at": None
    }

    goals.append(goal)
    save_goals()

    print("Saved Successfully!")

# ------------------------- View Goals -------------------------
def view_goals(show_prompt = True):
    if not goals:
        print("No goals yet!")
    else:
        print("Your goals are:")
        for i in range(len(goals)):
            goal = goals[i]
            if isinstance(goal, str):
                print(f"{i+1}, {goal}")
            else:
                print(f"\nGoal {i+1}: \n  {goal['text']}  \n Priority: {goal.get('priority', 'N/A')} \n  Created: {goal.get('created_at', 'N/A')}")
                if goal.get('completed_at'):
                    print(f"Completed: {goal['completed_at']}")
    
    time.sleep(0.5)
    
    if show_prompt:
        proceed_to_next= input("\nEnter a character if you want to exit this screen: ")
        if proceed_to_next:
            return
    
# ------------------------ View Finished Goals ----------------------
def view_finished_goals():
    try: 
        with open("finished.json", "r") as f:
            finished_goals = json.load(f)
    except(FileNotFoundError, json.JSONDecodeError):
        finished_goals = []
    
    if not finished_goals:
        print("No finished goals yet!")
    else:
        print("Your finished goals are:")
        for i in range(len(finished_goals)):
            goal = finished_goals[i]
            print(f"\nGoal {i+1}: \n  {goal['text']}  \n Priority: {goal.get('priority', 'N/A')} \n  Created: {goal['created_at']} \n  Completed: {goal.get('completed_at', 'N/A')}")

    time.sleep(0.5)
    proceed = input("\n Press enter to return to menu")

# ------------------------- Finish a Goal -------------------------
def finished_goal():
    view_goals(show_prompt = False)

    if not goals:
        return
    
    running = True
    while running:
        try:
            num = int(input("\nWhich goal did you finish? (number): "))
            if 1 <= num <= len(goals):
                finished = input("Did you finish this goal? (y/n): ").strip().lower()
                while finished not in ['y', 'n']:
                    finished = input("Please enter 'y' or 'n' for yes or no respectively: ").strip().lower()
                if finished == 'y':
                    goal = goals[num-1]
                    goal['completed_at'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    finished_goals = []
                    try:
                        with open("finished.json", "r") as f:
                            finished_goals = json.load(f)
                    except (FileNotFoundError, json.JSONDecodeError):
                        finished_goals = []
                    
                    finished_goals.append(goal)

                    with open("finished.json", "w") as f:
                        json.dump(finished_goals, f, indent=4)
                    
                    removed_goal = goals.pop(num - 1)
                    save_goals()
                    print(f"Great job on finishing: {removed_goal['text']}")
                    running = False
                
                elif finished == 'n':
                    print("Maybe next time!")
                    remove_yes_no = input("Do you want to remove this goal regardless? (y/n): ").strip().lower()
                    if remove_yes_no == 'y' or remove_yes_no == 'yes':
                        removed_goal = goals.pop(num - 1)
                        save_goals()
                    else:
                        print("Goal not removed.")
                    running = False
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")
            else:
                print(f"Invalid number. Please choose between 1 and {len(goals)}")
        except ValueError:
            print("Please enter a valid number.")

def clear_goals():
    clear = (input("Are you sure you want to clear your goals? (y/n): ")).strip().lower()
    if clear == 'y' or clear == 'yes':
        global goals
        goals = []
        save_goals()
        print("All your goals have been cleared! ")

def main():
    running = True
    load_goals()

    while running:
        time.sleep(1)
        print("\n=== Goal Tracker ===")
        print("")
        print("1. Add Goal")
        print("2. View Goals")
        print("3. Finish Goal")
        print("4. View Finished Goals")
        print("5. Clear All")
        print("6. Exit")
        print("")
        print("=" * 20)

        choice = input("\nChoose an option (1-6): ").strip()
        print("")

        if choice == '1':
            add_goal()
        elif choice == '2':
            view_goals()
        elif choice == '3':
            finished_goal()
        elif choice == '4':
            view_finished_goals()
        elif choice == '5':
            clear_goals()
        elif choice == '6':
            print("Exiting program")
            running = False
        else:
            print("Invalid choice. Please select a number between 1 and 6.").strip()

if __name__ == "__main__":
    main()