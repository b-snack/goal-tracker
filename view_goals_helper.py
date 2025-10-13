import time
import datetime
import json
from collections import Counter

def get_priority_value(goal):
    priority_order = {"!!!": 1, "!!": 2, "!": 3}
    return priority_order.get(goal.get('priority', '!'), 4)

def separate_overdue(goals):
    import main
    
    today = datetime.datetime.now().date()
    overdue = []
    not_overdue = []

    for goal in main.goals:
        if goal.get('due_date'):
            try:
                due_date = datetime.datetime.strptime(goal['due_date'], "%Y-%m-%d").date()
                if due_date < today:
                    days_overdue = (today - due_date).days
                    overdue.append((goal, days_overdue))
                else:
                    not_overdue.append(goal)
            except:
                not_overdue.append(goal)
        else:
            not_overdue.append(goal)
    
    return overdue, not_overdue

def display_goal(goal, number, show_overdue_days = None):
    print(f"\nGoal {number}:")
    print(f"    {goal['text']}")
    print(f"    Priority: {goal.get('priority', 'N/A')}")

    if show_overdue_days:
        print(f"    Due: {goal['due_date']}  ({show_overdue_days} day(s) overdue!)")
    elif goal.get('due_date'):
        print(f"    Due: {goal['due_date']}")
    if goal.get('category'):
        print(f"Category: {goal['category']}")
    if goal.get('is_repeating'):
        print(f"    Repeats every {goal.get('repeat_interval', 'N/A')} day(s)")
    if goal.get('created_at') and not show_overdue_days:
        print(f"    Created: {goal['created_at']}")
    

# ------------------------- View Goals -------------------------
def view_goals(show_prompt = True):
    import main
    if not main.goals:
        print("No goals yet!")

    else:
        overdue, not_overdue = separate_overdue(main.goals)

        overdue.sort(key=lambda x: (get_priority_value(x[0]), -x[1]))
        not_overdue.sort(key=get_priority_value)

        if overdue:
            print(f"WARNING: You have {len(overdue)} overdue goal(s)! \n")
            print("--- OVERDUE GOALS ---")
            for i, (goal, days_overdue) in enumerate(overdue, 1):
                display_goal(goal, i, show_overdue_days=days_overdue)
        
        if not_overdue:
            if overdue:
                print("\n" + "-" * 40)
            print("\n--- GOALS ACTIVE (sort by priority) ---")
            for i, goal in enumerate(not_overdue, 1):
                display_goal(goal, i + len(overdue))
    
    time.sleep(0.5)
    
    if show_prompt:
        proceed_to_next= input("\nEnter a character if you want to exit this screen: ")
        if proceed_to_next:
            return
    
# ------------------------ View Finished Goals ----------------------
def view_finished_goals():
    import main
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
            print(f"\nGoal {i+1}: \n  {goal['text']}  \n Priority: {goal.get('priority', 'N/A')} \n  Created: {goal['created_at']} \n  Completed: {goal.get('completed_at', 'N/A')} \n")
            if goal.get('category'):
                print((f"Category: {goal['category']} "))
            if goal.get('is_repeating'):
                print(f"Repeats: Every {goal.get('repeat_interval', 'N/A')} day(s)")

    time.sleep(0.5)
    proceed = input("\n Press enter to return to menu")

def view_by_category():
    import main

    if not main.goals:
        print("no goals yet!")
    
    else:
        categorized = {}
        for goal in main.goals:
            cat = goal.get('category', 'Uncategorized')
            if cat not in categorized:
                categorized[cat] = []
            categorized[cat].append(goal)

        for category, goals in categorized.items():
            print(f'\n--- {category} ---')
            for i, goal in enumerate(goals, 1):
                print(f"\n{i}. {goal['text']}")
                print(f"   Priority: {goal.get('priority', 'N/A')}")
                if goal.get('due_date'):
                    print(f"   Due: {goal['due_date']}")
                if goal.get('is_repeating'):
                    print(f"   Repeats: Every {goal.get('repeat_interval', 'N/A')} day(s)")
    input("\nPress enter to return to menu")

def view_stats():
    import main

    if not main.goals:
        print("No goals yet! ")
        return

    with open("finished.json", "r") as f:
        finished_goals = json.load(f)
    
    active_total = len(main.goals)
    completed_total = len(finished_goals)
    all_total_time = active_total + completed_total

    priority_list = [g.get('priority') for g in main.goals]
    priority_counts = Counter(priority_list)

    high_priority = priority_counts.get('!!!', 0)
    medium_priority = priority_counts.get('!!', 0)
    low_priority = priority_counts.get('!', 0)

    today = datetime.datetime.now().date()
    overdue_count = 0
    for goal in main.goals:
        if goal.get('due_date'):
            due_date = datetime.datetime.strptime(goal['due_date'], "%Y-%m-%d").date()
            if due_date < today:
                overdue_count +=1

    categories = {}
    for goal in main.goals:
        cat = goal.get('category', 'Uncategorized')
        categories[cat] = categories.get(cat, 0) + 1

    most_common_category = max(categories, key=categories.get) if categories else "None"

    repeating_count = len([g for g in main.goals if g.get('is_repeating')])

    completion_rate = 0
    if all_total_time> 0:
        completion_rate = (completed_total / all_total_time) * 100
    
    print("\n" + "=" * 40)
    print("YOUR GOAL STATISTICS")
    print("=" * 40)
    
    print(f"\nActive Goals: {active_total}")
    print(f"Completed Goals: {completed_total}")
    print(f"All-Time Total: {all_total_time}")
    
    if all_total_time > 0:
        print(f"Completion Rate: {completion_rate:.1f}%")
    
    print(f"\nOverdue Goals: {overdue_count}")
    print(f"Repeating Goals: {repeating_count}")
    
    print(f"\nHigh Priority (!!!): {high_priority}")
    print(f"Medium Priority (!!): {medium_priority}")
    print(f"Low Priority (!): {low_priority}")
    
    print(f"\nMost Common Category: {most_common_category}")
    
    if categories:
        print("\nGoals by Category:")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print(f"   {cat}: {count}")
    
    print("\n" + "=" * 40)
    
    time.sleep(0.5)
    input("\nPress enter to return to menu")