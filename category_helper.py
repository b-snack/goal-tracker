"""
categorization --> e.g. personal, school, health, etc..; tags; urgency/importance (kinda similar to the reminders app --> !, !!, !!!, etc. (maybe more efficent way?) )
"""
import json

# def create_category():
#     category_name = ""
#     create_category = input("Do you want to create a new category? (y/n): ").strip().lower()
#     while create_category not in ['y', 'n']:
#         create_category = input("Please enter a valid input: ").strip().lower()

#     if create_category == 'y':
#         category = input("What is the name of your category?")
#         category_name = category
    
#     elif create_category == 'n':
#         category_name = False
    
#     return category_name

def load_categories():
    try:
        with open("goals.json", "r") as f:
            goals = json.load(f)
            categories = set()
            for goal in goals:
                if goal.get('category'):
                    categories.add(goal['category'])
            return list(categories)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def create_category():
    existing = load_categories()

    if existing:
        print(f"Existing categories: {', '.join(existing)}")
    
    create_new = input("Do you want to create a new category? (y/n): ").strip().lower()
    while create_new not in ['y', 'n']:
        create_new = input("Please enter a valid input: ").strip().lower()
    
    if create_new == 'y':
        if existing:
            use_existing = input("Use existing category? (y/n): ").strip().lower()
            if use_existing == 'y':
                print("\nAvailable categories:")
                for i, cat in enumerate(existing, 1):
                    print (f"{i}. {cat}")
                choice = input("Select number or type new name: ").strip()

                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(existing):
                        return existing[idx]
                except ValueError:
                    pass
                
                return choice if choice else None
        category = input("What is the name of your category? ").strip()
        return category if category else None
    
    return None