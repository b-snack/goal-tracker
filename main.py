"""
Goal Tracker
A simple command-line application to track personal goals. (currently)

Features:
- Add & save goals to a file
- view goals 
- finish goals

Future intended features (ranked by difficulty: kinda):
- edit goals
- categorization --> e.g. personal, school, health, etc..; tags; urgency/importance (kinda similar to the reminders app --> !, !!, !!!, etc. (maybe more efficent way?) )
- migrate from text-based to GUI-based application 
- colour coding for priority levels
- track success rate of goals -> using graphs or stats or etc.
- proof that you actually did it? (unrealistic perhaps but could work --> e,g, upload a photo & something analyzes it to confirm that ur not bsing it)
- maybe a calendar view
- maybe collaboration with others?

Fri Oct 10, 2025: 
Added:
- Add & save goals to a file
- view goals 
- finish goals

Sat Oct 11, 2025:
- added priority + timestamps to goals
- added finished.json file for completed goals

Sat Oct 12, 2025:
- moved functions to different files for organization
- due dates 
- repeating goals (only every n days tho, not very customizable)

"""


import datetime
import os
import time
import json
from save_load_helper import save_goals, load_goals
from add_remove_helper import add_goal, finished_goal, clear_goals
from view_goals_helper import view_finished_goals, view_goals, view_by_category

goals = []

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
            view_by_category()
        elif choice == '7':
            print("Exiting program")
            running = False
        else:
            print("Invalid choice. Please select a number between 1 and 6.")

if __name__ == "__main__":
    main()