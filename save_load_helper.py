"""
save and load goals
"""
import json
# ------------------------- Save Goals -------------------------
def save_goals():
    import main
    with open("goals.json", "w") as f:
        json.dump(main.goals, f, indent = 4)

# ------------------------- Load Goals -------------------------
def load_goals():
    import main
    try:
        with open("goals.json", "r") as f:
            main.goals = json.load(f)
    except FileNotFoundError:
        print("file not found error.")
        main.goals = []
    except json.JSONDecodeError:
        print("json.JSONDecode Error")
        main.goals = []