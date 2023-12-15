# from gettext import npgettext
# from pulp import LpProblem, LpMinimize, LpVariable, LpStatus, lpSum
# import json
# from random import shuffle, random, randint,choice
# import numpy as np


# food_data = {

#     "Full fat milk 100 ml": {"Calories": 89, "Protein": 3.3, "Fats": 6.2, "Carbs": 5, "Category": "Vegetarian", "MacroType": "Fat"},
#     "Chicken breast 100 grams": {"Calories": 120, "Protein": 22.5, "Fats": 2.6, "Carbs": 0, "Category": "Non-Vegetarian", "MacroType": "Protein"},
#     "Boiled white rice 100 grams": {"Calories": 97, "Protein": 2.1, "Fats": 0.3, "Carbs": 21.5, "Category": "Vegan", "MacroType": "Carb"},
#     "Mutton raw": {"Calories": 194, "Protein": 18.5, "Fats": 13.3, "Carbs": 0, "Category": "Non-Vegetarian", "MacroType": "Protein"},
#     "Tilapia fish raw": {"Calories": 111, "Protein": 23.3, "Fats": 2, "Carbs": 0, "Category": "Non-Vegetarian", "MacroType": "Protein"},
#     "Tuna fish raw": {"Calories": 128, "Protein": 23.6, "Fats": 3, "Carbs": 0, "Category": "Non-Vegetarian", "MacroType": "Protein"},
#     "Beef": {"Calories": 114, "Protein": 22.6, "Fats": 2.6, "Carbs": 0, "Category": "Non-Vegetarian", "MacroType": "Protein"},
#     "Boiled egg white": {"Calories": 53, "Protein": 11.3, "Fats": 0.6, "Carbs": 0.6, "Category": "Vegetarian", "MacroType": "Protein"},
#     "Boiled whole eggs": {"Calories": 155, "Protein": 12.6, "Fats": 10.6, "Carbs": 1.1, "Category": "Vegetarian", "MacroType": "Fat"},
#     "Paneer": {"Calories": 265, "Protein": 18.3, "Fats": 20.8, "Carbs": 1.2, "Category": "Vegetarian", "MacroType": "Fat"},
#     "Tofu": {"Calories": 144, "Protein": 17.3, "Fats": 8.7, "Carbs": 2.8, "Category": "Vegan", "MacroType": "Protein"},
#     "Fat free Paneer": {"Calories": 115, "Protein": 23, "Fats": 1, "Carbs": 3, "Category": "Vegetarian", "MacroType": "Protein"},
#     "Fried peanuts": {"Calories": 603, "Protein": 20.8, "Fats": 56, "Carbs": 14.3, "Category": "Vegan", "MacroType": "Fat"},
#     "Brown bread": {"Calories": 265, "Protein": 8.8, "Fats": 3, "Carbs": 47.1, "Category": "Vegan", "MacroType": "Carb"},
#     "Chapathi": {"Calories": 244, "Protein": 8.7, "Fats": 1.2, "Carbs": 50, "Category": "Vegan", "MacroType": "Carb"},
#     "Idly": {"Calories": 146, "Protein": 4.5, "Fats": 0.7, "Carbs": 30.4, "Category": "Vegan", "MacroType": "Carb"},
#     "Dosa": {"Calories": 184, "Protein": 4.5, "Fats": 6, "Carbs": 28.3, "Category": "Vegan", "MacroType": "Carb"},
#     "Sweet Potato": {"Calories": 86, "Protein": 1.6, "Fats": 0.1, "Carbs": 20.1, "Category": "Vegan", "MacroType": "Carb"},
#     "Fat free Milk 100 Ml": {"Calories": 38, "Protein": 3.3, "Fats": 0, "Carbs": 5.4, "Category": "Vegetarian", "MacroType": "Carb"},
#     "Lentils": {"Calories": 353, "Protein": 25.8, "Fats": 1.1, "Carbs": 60.1, "Category": "Vegan", "MacroType": "Protein"},
#     "Black chana": {"Calories": 360, "Protein": 17.1, "Fats": 5.3, "Carbs": 60.9, "Category": "Vegan", "MacroType": "Protein"},
#     "Oats raw": {"Calories": 374, "Protein": 13.6, "Fats": 7.6, "Carbs": 62.8, "Category": "Vegan", "MacroType": "Carb"},
#     "Upma": {"Calories": 85, "Protein": 2.4, "Fats": 1.4, "Carbs": 16, "Category": "Vegan", "MacroType": "Carb"},
#     "Omellete": {"Calories": 227, "Protein": 11.9, "Fats": 19.9, "Carbs": 1.9, "Category": "Vegetarian", "MacroType": "Protein"},
#     "Egg white Omellete": {"Calories": 100, "Protein": 9.7, "Fats": 6.1, "Carbs": 0.8, "Category": "Vegetarian", "MacroType": "Protein"},
#     "Coconut oil 30 grams": {"Calories": 270, "Protein": 0, "Fats": 30, "Carbs": 0, "Category": "Vegan", "MacroType": "Fat"},
#     "Butter 30 grams": {"Calories": 219, "Protein": 0, "Fats": 24.3, "Carbs": 0, "Category": "Vegetarian", "MacroType": "Fat"},
#     "Ghee 30 grams": {"Calories": 270, "Protein": 0, "Fats": 30, "Carbs": 0, "Category": "Vegetarian", "MacroType": "Fat"},
#     "Fruit options (Watermelon, Apple, Pineapple, Papaya)": {"Calories": 50, "Protein": 0.5, "Fats": 0.1, "Carbs": 13.1, "Category": "Vegan", "MacroType": "Carb"},
#     "Vegetable salad": {"Calories": 36, "Protein": 1, "Fats": 1, "Carbs": 6.5, "Category": "Vegan", "MacroType": "Carb"},
#     "Flax seeds 25 grams": {"Calories": 134, "Protein": 4.6, "Fats": 10.5, "Carbs": 7.2, "Category": "Vegan", "MacroType": "Fat"},
#     "Almonds/Peanut 25 grams": {"Calories": 155, "Protein": 5.3, "Fats": 12.5, "Carbs": 5.4, "Category": "Vegan", "MacroType": "Fat"},
#     "Soya chunk 50 grams": {"Calories": 173, "Protein": 26, "Fats": 0.3, "Carbs": 26.5, "Category": "Vegan", "MacroType": "Protein"},
#     "Quinoa": {"Calories": 368, "Protein": 14.1, "Fats": 6.1, "Carbs": 64.2, "Category": "Vegan", "MacroType": "Carb"},
#     "Kidney beans": {"Calories": 346, "Protein": 22.9, "Fats": 1.1, "Carbs": 60.6, "Category": "Vegan", "MacroType": "Protein"}

# }


# # Sample user inputs, to be replaced with actual inputs from the questionnaire
# user_inputs = {
#     'gender': 'Male',
#     'weight': 70,  # in kg
#     'height': 175,  # in cm
#     'goal': 'Fat Loss',
#     'goal_amount_per_week': 250,  # in grams
#     'diet_preference': 'Non-Vegetarian',
#     'likes': ['Chicken', 'Rice', 'Eggs'],
#     'dislikes': ['Fish'],
#     'number_of_meals': 5,
#     'activity_level': 'Moderate',
#     # ... more inputs as required
# }



# # Function to calculate maintenance calories
# def calculate_maintenance_calories(weight, height, age, gender, activity_level):
#     # Basic Metabolic Rate (BMR) Calculation using Mifflin-St Jeor Equation
#     if gender == 'Male':
#         bmr = 10 * weight + 6.25 * height - 5 * age + 5
#     else:
#         bmr = 10 * weight + 6.25 * height - 5 * age - 161

#     # Adjust BMR based on activity level
#     activity_factor = {
#         'Sedentary': 1.2,
#         'Light': 1.375,
#         'Moderate': 1.55,
#         'Active': 1.725,
#         'Very Active': 1.9
#     }
#     maintenance_calories = bmr * activity_factor[activity_level]
#     return maintenance_calories

# # Function to adjust calories for goal
# def adjust_calories_for_goal(maintenance_calories, goal, goal_amount_per_week):
#     # 7700 kcals is approx equal to 1 kg of body weight
#     kcal_per_gram = 7700 / 1000
#     weekly_caloric_adjustment = goal_amount_per_week * kcal_per_gram
    
#     if goal == 'Fat Loss':
#         return maintenance_calories - weekly_caloric_adjustment / 7
#     elif goal == 'Muscle Gain':
#         return maintenance_calories + weekly_caloric_adjustment / 7
#     else:
#         return maintenance_calories

# # Function to calculate macronutrients
# def calculate_macros(calories, weight, macro_ratios):
#     # Example macro ratios {'Protein': 0.3, 'Fats': 0.25, 'Carbs': 0.45}
#     protein_calories = calories * macro_ratios['Protein']
#     fats_calories = calories * macro_ratios['Fats']
#     carbs_calories = calories * macro_ratios['Carbs']

#     protein_grams = protein_calories / 4
#     fats_grams = fats_calories / 9
#     carbs_grams = carbs_calories / 4

#     return {'Protein': protein_grams, 'Fats': fats_grams, 'Carbs': carbs_grams}

# # Function to create the diet optimization problem
# def create_diet_optimization_problem(food_data, macros, user_inputs):
#     # Create the LP object, set up as a minimization problem
#     problem = LpProblem("Diet_Optimization", LpMinimize)

#     food_vars = LpVariable.dicts("Food", food_data.keys(), lowBound=0, cat='Continuous')
#     meal_vars = {meal: LpVariable(f"Meal_{meal}", cat='Binary') for meal in range(user_inputs['number_of_meals'])}

#     # Objective function: Minimize the deviation from the macro targets
#     problem += lpSum([food_vars[food] * (food_data[food]['Protein'] - macros['Protein'] / user_inputs['number_of_meals'])**2 for food in food_data]) + \
#                lpSum([food_vars[food] * (food_data[food]['Fats'] - macros['Fats'] / user_inputs['number_of_meals'])**2 for food in food_data]) + \
#                lpSum([food_vars[food] * (food_data[food]['Carbs'] - macros['Carbs'] / user_inputs['number_of_meals'])**2 for food in food_data])

#     # Constraints
#     # The sum of protein, fats, and carbs from the foods must meet the user's requirements
#     problem += lpSum([food_vars[food] * food_data[food]['Protein'] for food in food_data]) >= macros['Protein']
#     problem += lpSum([food_vars[food] * food_data[food]['Fats'] for food in food_data]) >= macros['Fats']
#     problem += lpSum([food_vars[food] * food_data[food]['Carbs'] for food in food_data]) >= macros['Carbs']

#     # Ensure that each meal is used (binary meal variables will be 1 if the meal is selected)
#     for meal in meal_vars:
#         problem += lpSum([meal_vars[meal] * food_vars[food] for food in food_data]) >= 1

#     # Additional constraints for meal sizes and preferences can be added here

#     # Solve the problem
#     problem.solve()
    
#     # Check if a feasible diet plan was found
#     if LpStatus[problem.status] == 'Optimal':
#         # Extract the quantities of each food item from the solution
#         food_quantities = {food: food_vars[food].varValue for food in food_data if food_vars[food].varValue > 0}

#         # Structure the diet plan by meals
#         diet_plan = {f"Meal {meal}": {} for meal in range(user_inputs['number_of_meals'])}
#         for food, quantity in food_quantities.items():
#             # Randomly assign food items to meals for simplicity, can be improved with more specific logic
#             assigned_meal = np.random.choice(list(diet_plan.keys()))
#             diet_plan[assigned_meal][food] = quantity
        
#         return diet_plan
#     else:
#         return "Optimization Failed"

# # Assuming food_data is a dictionary containing food items with their macros and user preferences
# # Example: {'Chicken Breast': {'Protein': 31, 'Fats': 3.6, 'Carbs': 0}, ... }

# maintenance_calories = calculate_maintenance_calories(**user_inputs)
# adjusted_calories = adjust_calories_for_goal(maintenance_calories, user_inputs['goal'], user_inputs['goal_amount_per_week'])
# macros = calculate_macros(adjusted_calories, user_inputs['weight'], {'Protein': 0.3, 'Fats': 0.25, 'Carbs': 0.45})

# # Assuming we have a valid food_data dictionary
# diet_plan = create_diet_optimization_problem(food_data, macros, user_inputs)

# print(diet_plan)
