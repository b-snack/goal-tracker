"""
Add goals, finish goals, and clear goals. 
"""

from view_goals_helper import view_goals, view_finished_goals
from save_load_helper import save_goals, load_goals
from category_helper import create_category
import datetime
import json


# ------------------------- Add Goal -------------------------
def add_goal():
    import main

    goal_text = input("Enter a goal: ")
    time_added = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    goal_priority = input("How important is this task? (!!!, !! or !): ")

    while goal_priority not in ["!!!", "!!", "!"]:
        print("Invalid input.")
        goal_priority = input("Please try again: ")
    
    has_due_date = input("Does this goal have a due date? (y/n)" ).strip().lower()
    due_date = None

    if has_due_date in ['y', 'yes']:
        ask = True
        while ask:
            due_date_input = input("How many days from now? (leave blank for n/a): ")
            if not due_date_input:
                break
            days = int(due_date_input)
            while days < 0:
                due_date_input = input("Please enter a valid number: ")
                days = int(due_date_input)
            due_date_obj = datetime.datetime.now() + datetime.timedelta(days=days)
            due_date = due_date_obj.strftime("%Y-%m-%d")
            break
    else:
        while has_due_date not in ['y', 'n', 'yes', 'n']:
            has_due_date = input("Please enter a valid input").strip().lower()
    
    has_repeat = input("Does this goal repeat? (y/n): ").strip().lower()

    is_repeating = False
    repeat_interval = None

    while has_repeat not in ['y', 'n']:
        has_repeat = input("Please enter a valid input: ")
    if has_repeat == 'y':
        is_repeating = True
        interval = input("How often does this repeat? (# of days)? ").strip()

        run = True
        while run:
            try:
                days = int(interval)
                if days > 0:
                    repeat_interval = days
                    run = False
                else:
                    interval = input("Please enter a positive number").strip()
            except ValueError:
                interval = input("Please enter a valid number: ").strip()
            
    category = create_category()
    
    goal = {
        "text": goal_text,
        "priority": goal_priority,
        "created_at": time_added,
        "completed_at": None,
        "due_date": due_date, 
        "is_repeating": is_repeating,
        "repeat_interval": repeat_interval,
        "category": category
    }

    main.goals.append(goal)
    save_goals()

    print("Saved Successfully!")



# ------------------------- Finish a Goal -------------------------
def finished_goal():
    import main

    view_goals(show_prompt = False)

    if not main.goals:
        return
    
    running = True
    while running:
        try:
            num = int(input("\nWhich goal did you finish? (number): "))
            if 1 <= num <= len(main.goals):
                finished = input("Did you finish this goal? (y/n): ").strip().lower()
                while finished not in ['y', 'n']:
                    finished = input("Please enter 'y' or 'n' for yes or no respectively: ").strip().lower()
                if finished == 'y':
                    goal = main.goals[num-1]
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
                    
                    if goal.get('is_repeating'):
                        new_goal = goal.copy()
                        new_goal['completed_at'] = None
                        new_goal['created_at'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                        if new_goal.get('due_date') and new_goal.get('repeat_interval'):
                            old_due = datetime.datetime.strptime(goal['due_date'], "%Y-%m-%d")
                            new_due = old_due + datetime.timedelta(days = new_goal['repeat_interval'])
                            new_goal['due_date'] = new_due.strftime("%Y-%m-%d")
                        
                        main.goals.append(new_goal)
                        print(f"Repeating goal recreated! Next due: {new_goal.get('due_date', 'N/A')}")

                    removed_goal = main.goals.pop(num - 1)
                    save_goals()
                    print(f"Great job on finishing: {removed_goal['text']}")
                    running = False
                
                elif finished == 'n':
                    print("Maybe next time!")
                    remove_yes_no = input("Do you want to remove this goal regardless? (y/n): ").strip().lower()
                    if remove_yes_no == 'y' or remove_yes_no == 'yes':
                        removed_goal = main.goals.pop(num - 1)
                        save_goals()
                    else:
                        print("Goal not removed.")
                    running = False
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")
            else:
                print(f"Invalid number. Please choose between 1 and {len(main.goals)}")
        except ValueError:
            print("Please enter a valid number.")

def clear_goals():
    import main

    clear = (input("Are you sure you want to clear your goals? (y/n): ")).strip().lower()
    if clear == 'y' or clear == 'yes':
        main.goals = []
        save_goals()
        print("All your goals have been cleared! ")

def edit_goal():
    import main
    from view_goals_helper import view_goals

    view_goals(show_prompt=False)

    if not main.goals:
        return

    try:
        goal_num = input("Which goal would you like to edit?")
        if 1 <= goal_num <= len(main.goals):
            goal = main.goals[goal_num-1]

            print(f"\nEditing: {goal['text']}")
            print("\nWhat do you want to edit?")
            print("1. Goal text")
            print("2. Priority")
            print("3. Due date")
            print("4. Category")
            print("5. Repeat settings")
            print("6. Cancel")

            choice = input("\nChoose option (1-6): ").strip()

            if choice == '1':
                new_text = input(f"Current: {goal['text']} \nNew text (or press enter to keep): ").strip()
                if new_text:
                    goal['text'] = new_text
                    print("Test updated!")
            
            elif choice == '2':
                new_priority = input(f"Current: {goal.get('priority', 'N/A')}\nNew priority (!!!, !! or !): ").strip()
                while new_priority not in ["!!!", "!!", "!"]:
                    new_priority = input("Invalid. Please enter !!!, !! or !: ").strip()
                goal['priority'] = new_priority
                print("Priority updated!")
            
            elif choice == '3':
                change = input(f"Current due date: {goal.get('due_date', 'None')}\nChange due date? (y/n): ").strip().lower()
                if change == 'y':
                    days_input = input("How many days from now? (leave blank to remove due date): ").strip()
                    if not days_input:
                        goal['due_date'] = None
                        print("Due date removed")
                    else:
                        try:
                            days = int(days_input)
                            if days < 0:
                                print("Invalid number")
                            else:
                                due_date_obj = datetime.datetime.now() + datetime.timedelta(days=days)
                                goal['due_date'] = due_date_obj.strftime("%Y-%m-%d")
                                print("Due date updated!")                            
                        except ValueError:
                            print("Invalid input")

            elif choice == '4':
                from category_helper import create_category
                print(f"Current category: {goal.get('category', 'None')}")
                new_category = create_category()
                goal['category'] = new_category
                print("Category updated!")
            
            elif choice == '5':
                current_repeat = "Yes" if goal.get('is_repeating') else "No"
                print(f"Current: Repeating = {current_repeat}, Interval = {goal.get('repeat_interval', 'N/A')} days")

                change_repeat = input("Change repeat settings? (y/n): ").strip().lower()
                if change_repeat == 'y':
                    is_repeat = input("Should this goal repeat? (y/n): ").strip().lower()
                    if is_repeat == 'y':
                        interval = input("How often? (# of days): ").strip()
                        try:
                            days = int(interval)
                            if days > 0:
                                goal['is_repeating'] = True
                                goal['repeat_interval'] = days
                                print("Repeat settings updated!")
                            else:
                                print("Invalid number.")
                        except ValueError:
                            print("Invalid input.")
                    else:
                        goal['is_repeating'] = False
                        goal['repeat_interval'] = None
                        print("Repeat removed")
            elif choice == '6':
                print("Edit cancelled")
                return
            
            else:
                print("Invalid choice.")
                return
            
            save_goals()
            print("\nGoal saved!")

        else:print(f"Invalid number. Please choose between 1 and {len(main.goals)}")

    except ValueError:
        print("Enter a valid number")

