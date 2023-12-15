from flask import Flask, render_template, request
from pulp import LpProblem, LpMinimize, LpVariable, LpStatus, lpSum

app = Flask(__name__)

# Define your food_data, MAX_QUANTITY, and MIN_QUANTITY here
# Add your food data, MAX_QUANTITY, and MIN_QUANTITY details
food_data = {

    "Full fat milk 100 ml": {"Calories": 89, "Protein": 3.3, "Fats": 6.2, "Carbs": 5, "Category": "Vegetarian", "MacroType": "Fat"},
    "Chicken breast 100 grams": {"Calories": 120, "Protein": 22.5, "Fats": 2.6, "Carbs": 0, "Category": "Non-Vegetarian", "MacroType": "Protein"},
    "Boiled white rice 100 grams": {"Calories": 97, "Protein": 2.1, "Fats": 0.3, "Carbs": 21.5, "Category": "Vegan", "MacroType": "Carb"},
    "Mutton raw": {"Calories": 194, "Protein": 18.5, "Fats": 13.3, "Carbs": 0, "Category": "Non-Vegetarian", "MacroType": "Protein"},
    "Tilapia fish raw": {"Calories": 111, "Protein": 23.3, "Fats": 2, "Carbs": 0, "Category": "Non-Vegetarian", "MacroType": "Protein"},
    "Tuna fish raw": {"Calories": 128, "Protein": 23.6, "Fats": 3, "Carbs": 0, "Category": "Non-Vegetarian", "MacroType": "Protein"},
    "Beef": {"Calories": 114, "Protein": 22.6, "Fats": 2.6, "Carbs": 0, "Category": "Non-Vegetarian", "MacroType": "Protein"},
    "Boiled egg white": {"Calories": 53, "Protein": 11.3, "Fats": 0.6, "Carbs": 0.6, "Category": "Vegetarian", "MacroType": "Protein"},
    "Boiled whole eggs": {"Calories": 155, "Protein": 12.6, "Fats": 10.6, "Carbs": 1.1, "Category": "Vegetarian", "MacroType": "Fat"},
    "Paneer": {"Calories": 265, "Protein": 18.3, "Fats": 20.8, "Carbs": 1.2, "Category": "Vegetarian", "MacroType": "Fat"},
    "Tofu": {"Calories": 144, "Protein": 17.3, "Fats": 8.7, "Carbs": 2.8, "Category": "Vegan", "MacroType": "Protein"},
    "Fat free Paneer": {"Calories": 115, "Protein": 23, "Fats": 1, "Carbs": 3, "Category": "Vegetarian", "MacroType": "Protein"},
    "Fried peanuts": {"Calories": 603, "Protein": 20.8, "Fats": 56, "Carbs": 14.3, "Category": "Vegan", "MacroType": "Fat"},
    "Brown bread": {"Calories": 265, "Protein": 8.8, "Fats": 3, "Carbs": 47.1, "Category": "Vegan", "MacroType": "Carb"},
    "Chapathi": {"Calories": 244, "Protein": 8.7, "Fats": 1.2, "Carbs": 50, "Category": "Vegan", "MacroType": "Carb"},
    "Idly": {"Calories": 146, "Protein": 4.5, "Fats": 0.7, "Carbs": 30.4, "Category": "Vegan", "MacroType": "Carb"},
    "Dosa": {"Calories": 184, "Protein": 4.5, "Fats": 6, "Carbs": 28.3, "Category": "Vegan", "MacroType": "Carb"},
    "Sweet Potato": {"Calories": 86, "Protein": 1.6, "Fats": 0.1, "Carbs": 20.1, "Category": "Vegan", "MacroType": "Carb"},
    "Fat free Milk 100 Ml": {"Calories": 38, "Protein": 3.3, "Fats": 0, "Carbs": 5.4, "Category": "Vegetarian", "MacroType": "Carb"},
    "Lentils": {"Calories": 353, "Protein": 25.8, "Fats": 1.1, "Carbs": 60.1, "Category": "Vegan", "MacroType": "Protein"},
    "Black chana": {"Calories": 360, "Protein": 17.1, "Fats": 5.3, "Carbs": 60.9, "Category": "Vegan", "MacroType": "Protein"},
    "Oats raw": {"Calories": 374, "Protein": 13.6, "Fats": 7.6, "Carbs": 62.8, "Category": "Vegan", "MacroType": "Carb"},
    "Upma": {"Calories": 85, "Protein": 2.4, "Fats": 1.4, "Carbs": 16, "Category": "Vegan", "MacroType": "Carb"},
    "Omellete": {"Calories": 227, "Protein": 11.9, "Fats": 19.9, "Carbs": 1.9, "Category": "Vegetarian", "MacroType": "Protein"},
    "Egg white Omellete": {"Calories": 100, "Protein": 9.7, "Fats": 6.1, "Carbs": 0.8, "Category": "Vegetarian", "MacroType": "Protein"},
    "Coconut oil 30 grams": {"Calories": 270, "Protein": 0, "Fats": 30, "Carbs": 0, "Category": "Vegan", "MacroType": "Fat"},
    "Butter 30 grams": {"Calories": 219, "Protein": 0, "Fats": 24.3, "Carbs": 0, "Category": "Vegetarian", "MacroType": "Fat"},
    "Ghee 30 grams": {"Calories": 270, "Protein": 0, "Fats": 30, "Carbs": 0, "Category": "Vegetarian", "MacroType": "Fat"},
    "Fruit options (Watermelon, Apple, Pineapple, Papaya)": {"Calories": 50, "Protein": 0.5, "Fats": 0.1, "Carbs": 13.1, "Category": "Vegan", "MacroType": "Carb"},
    "Vegetable salad": {"Calories": 36, "Protein": 1, "Fats": 1, "Carbs": 6.5, "Category": "Vegan", "MacroType": "Carb"},
    "Flax seeds 25 grams": {"Calories": 134, "Protein": 4.6, "Fats": 10.5, "Carbs": 7.2, "Category": "Vegan", "MacroType": "Fat"},
    "Almonds/Peanut 25 grams": {"Calories": 155, "Protein": 5.3, "Fats": 12.5, "Carbs": 5.4, "Category": "Vegan", "MacroType": "Fat"},
    "Soya chunk 50 grams": {"Calories": 173, "Protein": 26, "Fats": 0.3, "Carbs": 26.5, "Category": "Vegan", "MacroType": "Protein"},
    "Quinoa": {"Calories": 368, "Protein": 14.1, "Fats": 6.1, "Carbs": 64.2, "Category": "Vegan", "MacroType": "Carb"},
    "Kidney beans": {"Calories": 346, "Protein": 22.9, "Fats": 1.1, "Carbs": 60.6, "Category": "Vegan", "MacroType": "Protein"}
    # ... [your food_data] ...
}

MAX_QUANTITY = {
    "Chicken breast 100 grams": 200, # Example: max 200 grams per meal
    "Boiled white rice 100 grams": 300,
     "Full fat milk 100 ml": 200, # ml
    "Chicken breast 100 grams": 200, # grams
    "Boiled white rice 100 grams": 200, # grams
    "Mutton raw": 150, # grams
    "Tilapia fish raw": 150, # grams
    "Tuna fish raw": 150, # grams
    "Beef": 150, # grams
    "Boiled egg white": 6, # number of egg whites
    "Boiled whole eggs": 4, # number of eggs
    "Paneer": 100, # grams
    "Tofu": 150, # grams
    "Fat free Paneer": 150, # grams
    "Fried peanuts": 50, # grams
    "Brown bread": 100, # grams (about 2 slices)
    "Chapathi": 2, # number of chapathis
    "Idly": 4, # number of idlys
    "Dosa": 2, # number of dosas
    "Sweet Potato": 150, # grams
    "Fat free Milk 100 Ml": 200, # ml
    "Lentils": 100, # grams
    "Black chana": 100, # grams
    "Oats raw": 80, # grams
    "Upma": 150, # grams
    "Omellete": 2, # number of eggs used
    "Egg white Omellete": 4, # number of egg whites used
    "Coconut oil 30 grams": 30, # grams
    "Butter 30 grams": 30, # grams
    "Ghee 30 grams": 30, # grams
    "Fruit options (Watermelon, Apple, Pineapple, Papaya)": 200, # grams
    "Vegetable salad": 300, # grams
    "Flax seeds 25 grams": 25, # grams
    "Almonds/Peanut 25 grams": 50, # grams
    "Soya chunk 50 grams": 100, # grams
    "Quinoa": 100, # grams
    "Kidney beans": 100, # grams

    # ... [your MAX_QUANTITY data] ...
}

MIN_QUANTITY = {
    "Full fat milk 100 ml": 50,  # Assuming a practical minimum quantity in ml
    "Chicken breast 100 grams": 50,  # in grams
    "Boiled white rice 100 grams": 50,  # in grams
    "Mutton raw": 50,  # in grams
    "Tilapia fish raw": 50,  # in grams
    "Tuna fish raw": 50,  # in grams
    "Beef": 50,  # in grams
    "Boiled egg white": 1,  # number of egg whites
    "Boiled whole eggs": 1,  # number of eggs
    "Paneer": 50,  # in grams
    "Tofu": 50,  # in grams
    "Fat free Paneer": 50,  # in grams
    "Fried peanuts": 25,  # in grams
    "Brown bread": 50,  # in grams (about 1 slice)
    "Chapathi": 1,  # number of chapathis
    "Idly": 2,  # number of idlys
    "Dosa": 1,  # number of dosas
    "Sweet Potato": 50,  # in grams
    "Fat free Milk 100 Ml": 50,  # in ml
    "Lentils": 50,  # in grams
    "Black chana": 50,  # in grams
    "Oats raw": 50,  # in grams
    "Upma": 50,  # in grams
    "Omellete": 1,  # number of eggs used
    "Egg white Omellete": 2,  # number of egg whites used
    "Coconut oil 30 grams": 15,  # in grams
    "Butter 30 grams": 15,  # in grams
    "Ghee 30 grams": 15,  # in grams
    "Any fruit among the options": 50,  # in grams
    "Vegetable salad": 50,  # in grams
    "Flax seeds 25 grams": 10,  # in grams
    "Almonds/Peanut 25 grams": 10,  # in grams
    "Soya chunk 50 grams": 25,  # in grams
    "Quinoa": 50,  # in grams
    "Kidney beans": 50,  # in gram
    # ... [your MIN_QUANTITY data] ...
}

# Function to calculate maintenance calories
def calculate_maintenance_calories(weight, height, age, gender, activity_level):
    if gender == 'Male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    activity_factor = {
        'Sedentary': 1.2,
        'Light': 1.375,
        'Moderate': 1.55,
        'Active': 1.725,
        'Very Active': 1.9
    }
    return bmr * activity_factor[activity_level]

# Function to adjust calories for goal
def adjust_calories_for_goal(maintenance_calories, goal, goal_amount_per_week):
    kcal_per_gram = 7700 / 1000
    weekly_caloric_adjustment = goal_amount_per_week * kcal_per_gram
    if goal == 'Fat Loss':
        return maintenance_calories - weekly_caloric_adjustment / 7
    elif goal == 'Muscle Gain':
        return maintenance_calories + weekly_caloric_adjustment / 7
    else:
        return maintenance_calories

# Function to calculate macronutrients
def calculate_macros(calories, weight, macro_ratios):
    protein_calories = calories * macro_ratios['Protein']
    fats_calories = calories * macro_ratios['Fats']
    carbs_calories = calories * macro_ratios['Carbs']
    protein_grams = protein_calories / 4
    fats_grams = fats_calories / 9
    carbs_grams = carbs_calories / 4
    return {'Protein': protein_grams, 'Fats': fats_grams, 'Carbs': carbs_grams}

# Function to create diet optimization problem
def create_diet_optimization_problem(food_data, macros, user_inputs):
    problem = LpProblem("Diet_Optimization", LpMinimize)

    # Variables for food quantities
    food_vars = {food: LpVariable(f"Food_{food}", 0, cat='Continuous') for food in food_data}
    meal_food_vars = {(meal, food): LpVariable(f"Meal_{meal}_{food}", 0, cat='Continuous') 
                      for meal in range(user_inputs['number_of_meals']) 
                      for food in user_inputs['likes']}

    # Objective: Minimize total calories while meeting macro requirements
    problem += lpSum([food_vars[food] * food_data[food]['Calories'] for food in food_data])

    # Macro constraints
    problem += lpSum([food_vars[food] * food_data[food]['Protein'] for food in food_data]) >= macros['Protein']
    problem += lpSum([food_vars[food] * food_data[food]['Fats'] for food in food_data]) >= macros['Fats']
    problem += lpSum([food_vars[food] * food_data[food]['Carbs'] for food in food_data]) >= macros['Carbs']

    # Quantity constraints for each food item
    for food in food_data:
        if food in MAX_QUANTITY:
            problem += food_vars[food] <= MAX_QUANTITY[food]
        if food in MIN_QUANTITY:
            problem += food_vars[food] >= MIN_QUANTITY[food]

    # Meal distribution constraints
    for food in user_inputs['likes']:
        problem += lpSum(meal_food_vars[meal, food] for meal in range(user_inputs['number_of_meals'])) == food_vars[food]

    # Solve the problem
    problem.solve()

    # Extract the diet plan if a feasible solution was found
    if LpStatus[problem.status] == 'Optimal':
        diet_plan = {}
        for meal in range(user_inputs['number_of_meals']):
            meal_plan = {}
            for food in user_inputs['likes']:
                quantity = meal_food_vars[meal, food].varValue
                if quantity > 0:
                    meal_plan[food] = quantity
            diet_plan[f"Meal {meal+1}"] = meal_plan
        return diet_plan
    else:
        return "Optimization Failed"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_inputs = {
            
            'gender': request.form['gender'],
            'weight': float(request.form['weight']),
            'age': int(request.form['age']),
            'height': float(request.form['height']),
            'goal': request.form['goal'],
            'goal_amount_per_week': float(request.form['goal_amount_per_week']),
            'diet_preference': request.form['diet_preference'],
            'likes': request.form.getlist('likes'),
            'number_of_meals': int(request.form['number_of_meals']),
            'activity_level': request.form['activity_level']
        }

        maintenance_calories_args = {
            'weight': user_inputs['weight'],
            'height': user_inputs['height'],
            'age': user_inputs['age'],
            'gender': user_inputs['gender'],
            'activity_level': user_inputs['activity_level']
    # ... [your maintenance_calories_args data] ...
        }


       

        maintenance_calories = calculate_maintenance_calories(**maintenance_calories_args)
        adjusted_calories = adjust_calories_for_goal(maintenance_calories, user_inputs['goal'], user_inputs['goal_amount_per_week'])
        macros = calculate_macros(adjusted_calories, user_inputs['weight'], {'Protein': 0.3, 'Fats': 0.25, 'Carbs': 0.45})

        diet_plan = create_diet_optimization_problem(food_data, macros, user_inputs)
        return render_template('results.html', diet_plan=diet_plan, user_inputs=user_inputs)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
















# from pulp import LpProblem, LpMinimize, LpVariable, LpStatus, lpSum
# from flask import Flask, render_template, request
# from pulp import LpProblem, LpMinimize, LpVariable, LpStatus, lpSum


# app = Flask(__name__)

# # Function to calculate maintenance calories
# def calculate_maintenance_calories(weight, height, age, gender, activity_level):
#     if gender == 'Male':
#         bmr = 10 * weight + 6.25 * height - 5 * age + 5
#     else:
#         bmr = 10 * weight + 6.25 * height - 5 * age - 161
#     activity_factor = {
#         'Sedentary': 1.2,
#         'Light': 1.375,
#         'Moderate': 1.55,
#         'Active': 1.725,
#         'Very Active': 1.9
#     }
#     return bmr * activity_factor[activity_level]

# # Function to adjust calories for goal
# def adjust_calories_for_goal(maintenance_calories, goal, goal_amount_per_week):
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
#     protein_calories = calories * macro_ratios['Protein']
#     fats_calories = calories * macro_ratios['Fats']
#     carbs_calories = calories * macro_ratios['Carbs']
#     protein_grams = protein_calories / 4
#     fats_grams = fats_calories / 9
#     carbs_grams = carbs_calories / 4
#     return {'Protein': protein_grams, 'Fats': fats_grams, 'Carbs': carbs_grams}

# def create_diet_optimization_problem(food_data, macros, user_inputs, MAX_QUANTITY, MIN_QUANTITY):
#     problem = LpProblem("Diet_Optimization", LpMinimize)

#     # Variables for food quantities
#     food_vars = {food: LpVariable(f"Food_{food}", 0, cat='Continuous') for food in food_data}
#     meal_food_vars = {(meal, food): LpVariable(f"Meal_{meal}_{food}", 0, cat='Continuous') 
#                       for meal in range(user_inputs['number_of_meals']) 
#                       for food in user_inputs['likes']}

#     # Objective: Minimize total calories while meeting macro requirements
#     problem += lpSum([food_vars[food] * food_data[food]['Calories'] for food in food_data])

#     # Macro constraints
#     problem += lpSum([food_vars[food] * food_data[food]['Protein'] for food in food_data]) >= macros['Protein']
#     problem += lpSum([food_vars[food] * food_data[food]['Fats'] for food in food_data]) >= macros['Fats']
#     problem += lpSum([food_vars[food] * food_data[food]['Carbs'] for food in food_data]) >= macros['Carbs']

#     # Quantity constraints for each food item
#     for food in food_data:
#         if food in MAX_QUANTITY:
#             problem += food_vars[food] <= MAX_QUANTITY[food]
#         if food in MIN_QUANTITY:
#             problem += food_vars[food] >= MIN_QUANTITY[food]

#     # Meal distribution constraints
#     for food in user_inputs['likes']:
#         problem += lpSum(meal_food_vars[meal, food] for meal in range(user_inputs['number_of_meals'])) == food_vars[food]

#     # Solve the problem
#     problem.solve()

#     # Extract the diet plan if a feasible solution was found
#     if LpStatus[problem.status] == 'Optimal':
    
#         diet_plan = {}
#         for meal in range(user_inputs['number_of_meals']):
#             meal_plan = {}
#             for food in user_inputs['likes']:
#                 quantity = meal_food_vars[meal, food].varValue
#                 if quantity > 0:
#                     meal_plan[food] = quantity
#             diet_plan[f"Meal {meal+1}"] = meal_plan
#         return diet_plan
#     else:
#         return "Optimization Failed"
# # Function to create diet optimization problem
# # def create_diet_optimization_problem(food_data, macros, user_inputs, MAX_QUANTITY, MIN_QUANTITY):
# #     problem = LpProblem("Diet_Optimization", LpMinimize)
# #     food_vars = {food: LpVariable(f"Food_{food}", 0, cat='Continuous') for food in food_data}
# #     problem += lpSum([food_vars[food] * food_data[food]['Calories'] for food in food_data])
# #     problem += lpSum([food_vars[food] * food_data[food]['Protein'] for food in food_data]) >= macros['Protein']
# #     problem += lpSum([food_vars[food] * food_data[food]['Fats'] for food in food_data]) >= macros['Fats']
# #     problem += lpSum([food_vars[food] * food_data[food]['Carbs'] for food in food_data]) >= macros['Carbs']
# #     for food in food_data:
# #         if food in MAX_QUANTITY:
# #             problem += food_vars[food] <= MAX_QUANTITY[food], f"Max_{food}"
# #         if food in MIN_QUANTITY:
# #             problem += food_vars[food] >= MIN_QUANTITY[food], f"Min_{food}"
# #     problem.solve()
# #     if LpStatus[problem.status] == 'Optimal':
# #     # if problem.status == LpStatus['Optimal']:
# #         # print("Optimized Diet Plan:", diet_plan)
# #         return {food: food_vars[food].varValue for food in food_data if food_vars[food].varValue > 0}
# #     else:
# #         print("Optimization Failed. Status:", LpStatus[problem.status])
# #         # return None
    

#     # if problem.status == LpStatus['Optimal']:
#     #     diet_plan = {food: food_vars[food].varValue for food in food_data if food_vars[food].varValue > 0}
#     #     return diet_plan
#     # else:
#     #     return "Optimization Failed"


# # Sample user inputs

# # @app.route('/', methods=['GET', 'POST'])
# # def index():
# #     if request.method == 'POST':
# #         user_inputs = {
# #             'gender': request.form.get('gender'),
# #             'weight': int(request.form.get('weight')),
# #             'age': int(request.form.get('age')),
# #             'height': int(request.form.get('height')),
# #             'goal': request.form.get('goal'),
# #             'goal_amount_per_week': int(request.form.get('goal_amount_per_week')),
# #             'diet_preference': request.form.get('diet_preference'),
# #             'likes': request.form.getlist('likes'),
# #             'number_of_meals': int(request.form.get('number_of_meals')),
# #             'activity_level': request.form.get('activity_level')
# #         }



# user_inputs = {
#     'gender': 'Male',
#     'weight': 71,  # in kg
#     'age':21,
#     'height': 170,  # in cm
#     'goal': 'Fat Loss',
#     'goal_amount_per_week': 100,  # in grams
#     'diet_preference': 'Non-Vegetarian',
#     'likes': ['Chicken breast 100 grams', 
#         'Boiled white rice 100 grams', 
#         'Boiled whole eggs', 
#         'Vegetable salad', 
#         'Butter 30 grams',
#         'Fat free Milk 100 Ml',
#         'Chapathi',
#         'Black chana', 
#         'Ghee 30 grams',
#         'Paneer',
#         'Tofu',
#         'Brown bread',
#         'Oats raw',
#         'Lentils',
#         'Almonds/Peanut 25 grams',
#         'Sweet Potato',
#         'Fruit options (Watermelon, Apple, Pineapple, Papaya)'],
#     'dislikes': ['Fish'],
#     'number_of_meals': 5,
#     'activity_level': 'Moderate',

#     # ... [your user_inputs data] ...
# }

# # Food data
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
#     # ... [your food_data] ...
# }

# # MAX_QUANTITY and MIN_QUANTITY
# MAX_QUANTITY = {
#     "Chicken breast 100 grams": 200, # Example: max 200 grams per meal
#     "Boiled white rice 100 grams": 300,
#      "Full fat milk 100 ml": 200, # ml
#     "Chicken breast 100 grams": 200, # grams
#     "Boiled white rice 100 grams": 200, # grams
#     "Mutton raw": 150, # grams
#     "Tilapia fish raw": 150, # grams
#     "Tuna fish raw": 150, # grams
#     "Beef": 150, # grams
#     "Boiled egg white": 6, # number of egg whites
#     "Boiled whole eggs": 4, # number of eggs
#     "Paneer": 100, # grams
#     "Tofu": 150, # grams
#     "Fat free Paneer": 150, # grams
#     "Fried peanuts": 50, # grams
#     "Brown bread": 100, # grams (about 2 slices)
#     "Chapathi": 2, # number of chapathis
#     "Idly": 4, # number of idlys
#     "Dosa": 2, # number of dosas
#     "Sweet Potato": 150, # grams
#     "Fat free Milk 100 Ml": 200, # ml
#     "Lentils": 100, # grams
#     "Black chana": 100, # grams
#     "Oats raw": 80, # grams
#     "Upma": 150, # grams
#     "Omellete": 2, # number of eggs used
#     "Egg white Omellete": 4, # number of egg whites used
#     "Coconut oil 30 grams": 30, # grams
#     "Butter 30 grams": 30, # grams
#     "Ghee 30 grams": 30, # grams
#     "Fruit options (Watermelon, Apple, Pineapple, Papaya)": 200, # grams
#     "Vegetable salad": 300, # grams
#     "Flax seeds 25 grams": 25, # grams
#     "Almonds/Peanut 25 grams": 50, # grams
#     "Soya chunk 50 grams": 100, # grams
#     "Quinoa": 100, # grams
#     "Kidney beans": 100, # grams

#     # ... [your MAX_QUANTITY data] ...
# }

# MIN_QUANTITY = {
#     "Full fat milk 100 ml": 50,  # Assuming a practical minimum quantity in ml
#     "Chicken breast 100 grams": 50,  # in grams
#     "Boiled white rice 100 grams": 50,  # in grams
#     "Mutton raw": 50,  # in grams
#     "Tilapia fish raw": 50,  # in grams
#     "Tuna fish raw": 50,  # in grams
#     "Beef": 50,  # in grams
#     "Boiled egg white": 1,  # number of egg whites
#     "Boiled whole eggs": 1,  # number of eggs
#     "Paneer": 50,  # in grams
#     "Tofu": 50,  # in grams
#     "Fat free Paneer": 50,  # in grams
#     "Fried peanuts": 25,  # in grams
#     "Brown bread": 50,  # in grams (about 1 slice)
#     "Chapathi": 1,  # number of chapathis
#     "Idly": 2,  # number of idlys
#     "Dosa": 1,  # number of dosas
#     "Sweet Potato": 50,  # in grams
#     "Fat free Milk 100 Ml": 50,  # in ml
#     "Lentils": 50,  # in grams
#     "Black chana": 50,  # in grams
#     "Oats raw": 50,  # in grams
#     "Upma": 50,  # in grams
#     "Omellete": 1,  # number of eggs used
#     "Egg white Omellete": 2,  # number of egg whites used
#     "Coconut oil 30 grams": 15,  # in grams
#     "Butter 30 grams": 15,  # in grams
#     "Ghee 30 grams": 15,  # in grams
#     "Any fruit among the options": 50,  # in grams
#     "Vegetable salad": 50,  # in grams
#     "Flax seeds 25 grams": 10,  # in grams
#     "Almonds/Peanut 25 grams": 10,  # in grams
#     "Soya chunk 50 grams": 25,  # in grams
#     "Quinoa": 50,  # in grams
#     "Kidney beans": 50,  # in grams
#     # ... [your MIN_QUANTITY data] ...
# }

# # Calculating maintenance calories
# maintenance_calories_args = {
#     'weight': user_inputs['weight'],
#     'height': user_inputs['height'],
#     'age': user_inputs['age'],
#     'gender': user_inputs['gender'],
#     'activity_level': user_inputs['activity_level']
#     # ... [your maintenance_calories_args data] ...
# }
# maintenance_calories = calculate_maintenance_calories(**maintenance_calories_args)

# # Adjusting calories for the goal
# adjusted_calories = adjust_calories_for_goal(maintenance_calories, user_inputs['goal'], user_inputs['goal_amount_per_week'])

# # Calculating macros
# macros = calculate_macros(adjusted_calories, user_inputs['weight'], {'Protein': 0.3, 'Fats': 0.25, 'Carbs': 0.45})

# # Generating diet plan
# diet_plan = create_diet_optimization_problem(food_data, macros, user_inputs, MAX_QUANTITY, MIN_QUANTITY)

# # Output the diet plan
# print(diet_plan)



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
#     'weight': 71,  # in kg
#     'age':21,
#     'height': 170,  # in cm
#     'goal': 'Fat Loss',
#     'goal_amount_per_week': 200,  # in grams
#     'diet_preference': 'Non-Vegetarian',
#     'likes': ['Chicken breast 100 grams', 'Boiled white rice 100 grams', 'Boiled whole eggs', 'Vegetable salad', 'Butter 30 grams','Fat free Milk 100 Ml','Chapathi','Black chana', 'Ghee 30 grams'],
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

# # def create_diet_optimization_problem(food_data, macros, user_inputs):
# #     problem = LpProblem("Diet_Optimization", LpMinimize)


# #     # Variables for the quantity of each food item in each meal
# #     food_vars = {meal: {food: LpVariable(f"Food_{meal}_{food}", lowBound=0, cat='Continuous')
# #                         for food in food_data}
# #                  for meal in range(user_inputs['number_of_meals'])}

# #     # Objective: Minimize deviation from macro targets
# #     for nutrient in ['Protein', 'Fats', 'Carbs']:
# #         problem += lpSum([food_vars[meal][food] * food_data[food][nutrient] for meal in food_vars for food in food_vars[meal]]
# #                          - macros[nutrient])**2
        
# #     MAX_QUANTITY = {
# #     "Full fat milk 100 ml": 200, # ml
# #     "Chicken breast 100 grams": 200, # grams
# #     "Boiled white rice 100 grams": 200, # grams
# #     "Mutton raw": 150, # grams
# #     "Tilapia fish raw": 150, # grams
# #     "Tuna fish raw": 150, # grams
# #     "Beef": 150, # grams
# #     "Boiled egg white": 6, # number of egg whites
# #     "Boiled whole eggs": 4, # number of eggs
# #     "Paneer": 100, # grams
# #     "Tofu": 150, # grams
# #     "Fat free Paneer": 150, # grams
# #     "Fried peanuts": 50, # grams
# #     "Brown bread": 100, # grams (about 2 slices)
# #     "Chapathi": 2, # number of chapathis
# #     "Idly": 4, # number of idlys
# #     "Dosa": 2, # number of dosas
# #     "Sweet Potato": 150, # grams
# #     "Fat free Milk 100 Ml": 200, # ml
# #     "Lentils": 100, # grams
# #     "Black chana": 100, # grams
# #     "Oats raw": 80, # grams
# #     "Upma": 150, # grams
# #     "Omellete": 2, # number of eggs used
# #     "Egg white Omellete": 4, # number of egg whites used
# #     "Coconut oil 30 grams": 30, # grams
# #     "Butter 30 grams": 30, # grams
# #     "Ghee 30 grams": 30, # grams
# #     "Fruit options (Watermelon, Apple, Pineapple, Papaya)": 200, # grams
# #     "Vegetable salad": 300, # grams
# #     "Flax seeds 25 grams": 25, # grams
# #     "Almonds/Peanut 25 grams": 50, # grams
# #     "Soya chunk 50 grams": 100, # grams
# #     "Quinoa": 100, # grams
# #     "Kidney beans": 100, # grams


# # }
# #     for nutrient in ['Protein', 'Fats', 'Carbs']:
# #      total_nutrient = lpSum([food_vars[meal][food] * food_data[food][nutrient]
# #                             for meal in food_vars for food in food_vars[meal]])
# #     problem += (total_nutrient - macros[nutrient])**2    

# #     # Portion size constraints
# #     for meal in food_vars:
# #         for food in food_vars[meal]:
# #             if food in MAX_QUANTITY:
# #                 problem += food_vars[meal][food] <= MAX_QUANTITY[food]

# #     # Ensure inclusion of all liked items at least once
# #     for food in user_inputs['likes']:
# #         problem += lpSum([food_vars[meal][food] for meal in food_vars]) >= 1

# #     # Variety in meals
# #     for meal in food_vars:
# #         problem += lpSum([food_vars[meal][food] for food in food_vars[meal]]) <= 3  # At most 3 different items per meal

# #     # Solve the problem
# #     problem.solve()

# #     if LpStatus[problem.status] == 'Optimal':
# #         food_quantities = {food: food_vars[food].varValue for food in user_inputs['likes'] if food_vars[food].varValue > 0}

# #         # Distribute the food into the number of meals
# #         diet_plan = {f"Meal {meal+1}": {} for meal in range(user_inputs['number_of_meals'])}
# #         meal_counter = 0
# #         for food, quantity in food_quantities.items():
# #             meal_name = f"Meal {meal_counter % user_inputs['number_of_meals'] + 1}"
# #             diet_plan[meal_name][food] = quantity
# #             meal_counter += 1

# #         return diet_plan
# #     else:
# #         return "Optimization Failed"


# MIN_QUANTITY = {
#     "Full fat milk 100 ml": 50,  # Assuming a practical minimum quantity in ml
#     "Chicken breast 100 grams": 50,  # in grams
#     "Boiled white rice 100 grams": 50,  # in grams
#     "Mutton raw": 50,  # in grams
#     "Tilapia fish raw": 50,  # in grams
#     "Tuna fish raw": 50,  # in grams
#     "Beef": 50,  # in grams
#     "Boiled egg white": 1,  # number of egg whites
#     "Boiled whole eggs": 1,  # number of eggs
#     "Paneer": 50,  # in grams
#     "Tofu": 50,  # in grams
#     "Fat free Paneer": 50,  # in grams
#     "Fried peanuts": 25,  # in grams
#     "Brown bread": 50,  # in grams (about 1 slice)
#     "Chapathi": 1,  # number of chapathis
#     "Idly": 2,  # number of idlys
#     "Dosa": 1,  # number of dosas
#     "Sweet Potato": 50,  # in grams
#     "Fat free Milk 100 Ml": 50,  # in ml
#     "Lentils": 50,  # in grams
#     "Black chana": 50,  # in grams
#     "Oats raw": 50,  # in grams
#     "Upma": 50,  # in grams
#     "Omellete": 1,  # number of eggs used
#     "Egg white Omellete": 2,  # number of egg whites used
#     "Coconut oil 30 grams": 15,  # in grams
#     "Butter 30 grams": 15,  # in grams
#     "Ghee 30 grams": 15,  # in grams
#     "Any fruit among the options": 50,  # in grams
#     "Vegetable salad": 50,  # in grams
#     "Flax seeds 25 grams": 10,  # in grams
#     "Almonds/Peanut 25 grams": 10,  # in grams
#     "Soya chunk 50 grams": 25,  # in grams
#     "Quinoa": 50,  # in grams
#     "Kidney beans": 50,  # in grams
#     # Add other foods as needed
# }



# MAX_QUANTITY = {
#     "Chicken breast 100 grams": 200, # Example: max 200 grams per meal
#     "Boiled white rice 100 grams": 300,
#      "Full fat milk 100 ml": 200, # ml
#     "Chicken breast 100 grams": 200, # grams
#     "Boiled white rice 100 grams": 200, # grams
#     "Mutton raw": 150, # grams
#     "Tilapia fish raw": 150, # grams
#     "Tuna fish raw": 150, # grams
#     "Beef": 150, # grams
#     "Boiled egg white": 6, # number of egg whites
#     "Boiled whole eggs": 4, # number of eggs
#     "Paneer": 100, # grams
#     "Tofu": 150, # grams
#     "Fat free Paneer": 150, # grams
#     "Fried peanuts": 50, # grams
#     "Brown bread": 100, # grams (about 2 slices)
#     "Chapathi": 2, # number of chapathis
#     "Idly": 4, # number of idlys
#     "Dosa": 2, # number of dosas
#     "Sweet Potato": 150, # grams
#     "Fat free Milk 100 Ml": 200, # ml
#     "Lentils": 100, # grams
#     "Black chana": 100, # grams
#     "Oats raw": 80, # grams
#     "Upma": 150, # grams
#     "Omellete": 2, # number of eggs used
#     "Egg white Omellete": 4, # number of egg whites used
#     "Coconut oil 30 grams": 30, # grams
#     "Butter 30 grams": 30, # grams
#     "Ghee 30 grams": 30, # grams
#     "Fruit options (Watermelon, Apple, Pineapple, Papaya)": 200, # grams
#     "Vegetable salad": 300, # grams
#     "Flax seeds 25 grams": 25, # grams
#     "Almonds/Peanut 25 grams": 50, # grams
#     "Soya chunk 50 grams": 100, # grams
#     "Quinoa": 100, # grams
#     "Kidney beans": 100, # grams

#     # ... other foods ...
# }




    

# # def create_diet_optimization_problem(food_data, macros, user_inputs, MAX_QUANTITY, MIN_QUANTITY):
# #     problem = LpProblem("Diet_Optimization", LpMinimize)

# #     # Variables for food quantities
# #     food_vars = {food: LpVariable(f"Food_{food}", lowBound=0) for food in food_data}
# #     meal_vars = {(meal, food): LpVariable(f"Meal_{meal}_{food}", cat='Binary') 
# #                  for meal in range(user_inputs['number_of_meals']) 
# #                  for food in user_inputs['likes']}

# #     # Objective: Minimize total calories while meeting macro requirements
# #     problem += lpSum([food_vars[food] * food_data[food]['Calories'] for food in food_data])

# #     # Macro constraints
# #     problem += lpSum([food_vars[food] * food_data[food]['Protein'] for food in food_data]) >= macros['Protein']
# #     problem += lpSum([food_vars[food] * food_data[food]['Fats'] for food in food_data]) >= macros['Fats']
# #     problem += lpSum([food_vars[food] * food_data[food]['Carbs'] for food in food_data]) >= macros['Carbs']

# #     # Meal diversity and distribution constraints
# #     for meal in range(user_inputs['number_of_meals']):
# #         problem += lpSum(meal_vars[meal, food] for food in user_inputs['likes']) <= 3
# #         for food in user_inputs['likes']:
# #             problem += food_vars[food] <= meal_vars[meal, food] * MAX_QUANTITY[food]
# #             problem += food_vars[food] >= meal_vars[meal, food] * MIN_QUANTITY[food]

# #     # Practical quantity constraints
# #     for food in food_data:
# #         if food in MAX_QUANTITY:
# #             problem += food_vars[food] <= MAX_QUANTITY[food]
# #         if food in MIN_QUANTITY:
# #             problem += food_vars[food] >= MIN_QUANTITY[food]

# #     # Solve the problem
# #     problem.solve()

# #     # Extract the diet plan if a feasible solution was found
# #     if LpStatus[problem.status] == 'Optimal':
# #         diet_plan = {f"Meal {meal+1}": {} for meal in range(user_inputs['number_of_meals'])}
# #         for meal in range(user_inputs['number_of_meals']):
# #             for food in user_inputs['likes']:
# #                 if meal_vars[meal, food].varValue > 0:
# #                     diet_plan[f"Meal {meal+1}"][food] = food_vars[food].varValue
# #         return diet_plan
# #     else:
# #         return "Optimization Failed"

# def create_diet_optimization_problem(food_data, macros, user_inputs):
#     problem = LpProblem("Diet_Optimization", LpMinimize)

#     # Define variables for the quantity of each food item
#     food_vars = LpVariable.dicts("Food", food_data.keys(), lowBound=0, cat='Continuous')
#     meal_food_vars = {meal: {food: LpVariable(f"Meal_{meal}_{food}", cat='Binary') for food in user_inputs['likes']} for meal in range(user_inputs['number_of_meals'])}

#     # Objective function: Minimize total calories while meeting macro requirements
#     problem += lpSum([food_vars[food] * food_data[food]['Calories'] for food in user_inputs['likes']])

#     # Macro constraints
#     problem += lpSum([food_vars[food] * food_data[food]['Protein'] for food in user_inputs['likes']]) >= macros['Protein']
#     problem += lpSum([food_vars[food] * food_data[food]['Fats'] for food in user_inputs['likes']]) >= macros['Fats']
#     problem += lpSum([food_vars[food] * food_data[food]['Carbs'] for food in user_inputs['likes']]) >= macros['Carbs']

#     # Meal diversity constraints: Ensure each meal contains a mix of items
#     for meal in range(user_inputs['number_of_meals']):
#         for food in user_inputs['likes']:
#             problem += meal_food_vars[meal][food] * MAX_QUANTITY[food] >= food_vars[food]
#             problem += food_vars[food] >= meal_food_vars[meal][food]

#         problem += lpSum(meal_food_vars[meal].values()) >= min(len(user_inputs['likes']), 2) # Adjust '2' based on minimum variety desired in each meal

#     # Ensure all liked foods are included in the diet plan
#     for food in user_inputs['likes']:
#         problem += lpSum([meal_food_vars[meal][food] for meal in range(user_inputs['number_of_meals'])]) >= 1

#     # Solve the problem
#     problem.solve()

#     # Check if a feasible diet plan was found
#     if LpStatus[problem.status] == 'Optimal':
#         food_quantities = {food: food_vars[food].varValue for food in user_inputs['likes'] if food_vars[food].varValue > 0}

#         # Distribute the food into the number of meals
#         diet_plan = {f"Meal {meal+1}": {} for meal in range(user_inputs['number_of_meals'])}
#         for meal in range(user_inputs['number_of_meals']):
#             for food in user_inputs['likes']:
#                 if meal_food_vars[meal][food].varValue > 0:
#                     diet_plan[f"Meal {meal+1}"][food] = food_vars[food].varValue

#         return diet_plan
#     else:
#         return "Optimization Failed"

# # Define MAX_QUANTITY for each food item
# # MIN_QUANTITY = {
# #     "Full fat milk 100 ml": 50,  # Assuming a practical minimum quantity in ml
# #     "Chicken breast 100 grams": 50,  # in grams
# #     "Boiled white rice 100 grams": 50,  # in grams
# #     "Mutton raw": 50,  # in grams
# #     "Tilapia fish raw": 50,  # in grams
# #     "Tuna fish raw": 50,  # in grams
# #     "Beef": 50,  # in grams
# #     "Boiled egg white": 1,  # number of egg whites
# #     "Boiled whole eggs": 1,  # number of eggs
# #     "Paneer": 50,  # in grams
# #     "Tofu": 50,  # in grams
# #     "Fat free Paneer": 50,  # in grams
# #     "Fried peanuts": 25,  # in grams
# #     "Brown bread": 50,  # in grams (about 1 slice)
# #     "Chapathi": 1,  # number of chapathis
# #     "Idly": 2,  # number of idlys
# #     "Dosa": 1,  # number of dosas
# #     "Sweet Potato": 50,  # in grams
# #     "Fat free Milk 100 Ml": 50,  # in ml
# #     "Lentils": 50,  # in grams
# #     "Black chana": 50,  # in grams
# #     "Oats raw": 50,  # in grams
# #     "Upma": 50,  # in grams
# #     "Omellete": 1,  # number of eggs used
# #     "Egg white Omellete": 2,  # number of egg whites used
# #     "Coconut oil 30 grams": 15,  # in grams
# #     "Butter 30 grams": 15,  # in grams
# #     "Ghee 30 grams": 15,  # in grams
# #     "Any fruit among the options": 50,  # in grams
# #     "Vegetable salad": 50,  # in grams
# #     "Flax seeds 25 grams": 10,  # in grams
# #     "Almonds/Peanut 25 grams": 10,  # in grams
# #     "Soya chunk 50 grams": 25,  # in grams
# #     "Quinoa": 50,  # in grams
# #     "Kidney beans": 50,  # in grams
# #     # Add other foods as needed
# # }



# # MAX_QUANTITY = {
# #     "Chicken breast 100 grams": 200, # Example: max 200 grams per meal
# #     "Boiled white rice 100 grams": 300,
# #      "Full fat milk 100 ml": 200, # ml
# #     "Chicken breast 100 grams": 200, # grams
# #     "Boiled white rice 100 grams": 200, # grams
# #     "Mutton raw": 150, # grams
# #     "Tilapia fish raw": 150, # grams
# #     "Tuna fish raw": 150, # grams
# #     "Beef": 150, # grams
# #     "Boiled egg white": 6, # number of egg whites
# #     "Boiled whole eggs": 4, # number of eggs
# #     "Paneer": 100, # grams
# #     "Tofu": 150, # grams
# #     "Fat free Paneer": 150, # grams
# #     "Fried peanuts": 50, # grams
# #     "Brown bread": 100, # grams (about 2 slices)
# #     "Chapathi": 2, # number of chapathis
# #     "Idly": 4, # number of idlys
# #     "Dosa": 2, # number of dosas
# #     "Sweet Potato": 150, # grams
# #     "Fat free Milk 100 Ml": 200, # ml
# #     "Lentils": 100, # grams
# #     "Black chana": 100, # grams
# #     "Oats raw": 80, # grams
# #     "Upma": 150, # grams
# #     "Omellete": 2, # number of eggs used
# #     "Egg white Omellete": 4, # number of egg whites used
# #     "Coconut oil 30 grams": 30, # grams
# #     "Butter 30 grams": 30, # grams
# #     "Ghee 30 grams": 30, # grams
# #     "Fruit options (Watermelon, Apple, Pineapple, Papaya)": 200, # grams
# #     "Vegetable salad": 300, # grams
# #     "Flax seeds 25 grams": 25, # grams
# #     "Almonds/Peanut 25 grams": 50, # grams
# #     "Soya chunk 50 grams": 100, # grams
# #     "Quinoa": 100, # grams
# #     "Kidney beans": 100, # grams

# #     # ... other foods ...
# # }


# # def create_diet_optimization_problem(food_data, macros, user_inputs):
# #     # Initialize the optimization problem
# #     problem = LpProblem("Diet_Optimization", LpMinimize)

# #     # Create variables for each food item in each meal
# #     meal_food_vars = {}
# #     for meal in range(user_inputs['number_of_meals']):
# #         for food in food_data:
# #             meal_food_vars[(meal, food)] = LpVariable(f"Meal_{meal}_{food}", lowBound=0, cat='Continuous')

# #     # Objective function: Minimize total calories while meeting macro requirements
# #     problem += lpSum([meal_food_vars[(meal, food)] * food_data[food]['Calories'] for meal in range(user_inputs['number_of_meals']) for food in food_data])

# #     # Macro constraints
# #     for macro in ['Protein', 'Fats', 'Carbs']:
# #         problem += lpSum([meal_food_vars[(meal, food)] * food_data[food][macro] for meal in range(user_inputs['number_of_meals']) for food in food_data]) >= macros[macro]

# #     MAX_QUANTITY = {
# #     "Full fat milk 100 ml": 200, # ml
# #     "Chicken breast 100 grams": 200, # grams
# #     "Boiled white rice 100 grams": 200, # grams
# #     "Mutton raw": 150, # grams
# #     "Tilapia fish raw": 150, # grams
# #     "Tuna fish raw": 150, # grams
# #     "Beef": 150, # grams
# #     "Boiled egg white": 6, # number of egg whites
# #     "Boiled whole eggs": 4, # number of eggs
# #     "Paneer": 100, # grams
# #     "Tofu": 150, # grams
# #     "Fat free Paneer": 150, # grams
# #     "Fried peanuts": 50, # grams
# #     "Brown bread": 100, # grams (about 2 slices)
# #     "Chapathi": 2, # number of chapathis
# #     "Idly": 4, # number of idlys
# #     "Dosa": 2, # number of dosas
# #     "Sweet Potato": 150, # grams
# #     "Fat free Milk 100 Ml": 200, # ml
# #     "Lentils": 100, # grams
# #     "Black chana": 100, # grams
# #     "Oats raw": 80, # grams
# #     "Upma": 150, # grams
# #     "Omellete": 2, # number of eggs used
# #     "Egg white Omellete": 4, # number of egg whites used
# #     "Coconut oil 30 grams": 30, # grams
# #     "Butter 30 grams": 30, # grams
# #     "Ghee 30 grams": 30, # grams
# #     "Fruit options (Watermelon, Apple, Pineapple, Papaya)": 200, # grams
# #     "Vegetable salad": 300, # grams
# #     "Flax seeds 25 grams": 25, # grams
# #     "Almonds/Peanut 25 grams": 50, # grams
# #     "Soya chunk 50 grams": 100, # grams
# #     "Quinoa": 100, # grams
# #     "Kidney beans": 100, # grams


# # }    

# #     # Maximum quantity constraints for each food item
# #     for meal in range(user_inputs['number_of_meals']):
# #         for food in food_data:
# #             problem += meal_food_vars[(meal, food)] <= MAX_QUANTITY.get(food, float('inf'))

# #     # Ensure each meal contains at least one food item from 'likes'
# #     for meal in range(user_inputs['number_of_meals']):
# #         problem += lpSum([meal_food_vars[(meal, food)] for food in user_inputs['likes']]) >= 1, f"Meal_{meal}_food_presence"

# #     # Solve the problem
# #     problem.solve()

# #     # Check if a feasible diet plan was found
# #     if LpStatus[problem.status] == 'Optimal':
# #         # Extract the quantities of each food item for each meal from the solution
# #         diet_plan = {}
# #         for meal in range(user_inputs['number_of_meals']):
# #             meal_name = f"Meal {meal+1}"
# #             diet_plan[meal_name] = {}
# #             for food in food_data:
# #                 quantity = meal_food_vars[(meal, food)].varValue
# #                 if quantity > 0:
# #                     diet_plan[meal_name][food] = quantity

# #         return diet_plan
# #     else:
# #         return "Optimization Failed"

# # You will continue with the rest of your code here...



# # def create_diet_optimization_problem(food_data, macros, user_inputs):
# #     problem = LpProblem("Diet_Optimization", LpMinimize)

# #     # Define variables for the quantity of each food item
# #     food_vars = LpVariable.dicts("Food", food_data.keys(), lowBound=0, cat='Continuous')



# #     # Create variables for each food item in each meal
   
# # # ... [rest of the code to solve and process the problem] ...







# #     # Objective function: Minimize total calories while meeting macro requirements
# #     problem += lpSum([food_vars[food] * food_data[food]['Calories'] for food in user_inputs['likes']])

# #     # Macro constraints
# #     problem += lpSum([food_vars[food] * food_data[food]['Protein'] for food in user_inputs['likes']]) >= macros['Protein']
# #     problem += lpSum([food_vars[food] * food_data[food]['Fats'] for food in user_inputs['likes']]) >= macros['Fats']
# #     problem += lpSum([food_vars[food] * food_data[food]['Carbs'] for food in user_inputs['likes']]) >= macros['Carbs']

# #     MAX_QUANTITY = {
# #     "Full fat milk 100 ml": 200, # ml
# #     "Chicken breast 100 grams": 200, # grams
# #     "Boiled white rice 100 grams": 200, # grams
# #     "Mutton raw": 150, # grams
# #     "Tilapia fish raw": 150, # grams
# #     "Tuna fish raw": 150, # grams
# #     "Beef": 150, # grams
# #     "Boiled egg white": 6, # number of egg whites
# #     "Boiled whole eggs": 4, # number of eggs
# #     "Paneer": 100, # grams
# #     "Tofu": 150, # grams
# #     "Fat free Paneer": 150, # grams
# #     "Fried peanuts": 50, # grams
# #     "Brown bread": 100, # grams (about 2 slices)
# #     "Chapathi": 2, # number of chapathis
# #     "Idly": 4, # number of idlys
# #     "Dosa": 2, # number of dosas
# #     "Sweet Potato": 150, # grams
# #     "Fat free Milk 100 Ml": 200, # ml
# #     "Lentils": 100, # grams
# #     "Black chana": 100, # grams
# #     "Oats raw": 80, # grams
# #     "Upma": 150, # grams
# #     "Omellete": 2, # number of eggs used
# #     "Egg white Omellete": 4, # number of egg whites used
# #     "Coconut oil 30 grams": 30, # grams
# #     "Butter 30 grams": 30, # grams
# #     "Ghee 30 grams": 30, # grams
# #     "Fruit options (Watermelon, Apple, Pineapple, Papaya)": 200, # grams
# #     "Vegetable salad": 300, # grams
# #     "Flax seeds 25 grams": 25, # grams
# #     "Almonds/Peanut 25 grams": 50, # grams
# #     "Soya chunk 50 grams": 100, # grams
# #     "Quinoa": 100, # grams
# #     "Kidney beans": 100, # grams


# # }


# #     for food in food_data:

# #      for meal in range(user_inputs['number_of_meals']):
# #          meal_name = f"Meal_{meal}"
# #          problem += food_vars[meal_name][food] <= MAX_QUANTITY.get(food, float('inf'))

# #     # Ensure each meal contains at least one food item from 'likes'
# #     for meal in range(user_inputs['number_of_meals']):
# #         problem += lpSum([food_vars[food] for food in user_inputs['likes']]) >= 1, f"Meal_{meal}_food_presence"

# #     # Solve the problem
# #     problem.solve()

# #     # Check if a feasible diet plan was found
# #     if LpStatus[problem.status] == 'Optimal':
# #         food_quantities = {food: food_vars[food].varValue for food in user_inputs['likes'] if food_vars[food].varValue > 0}

# #         # Distribute the food into the number of meals
# #         diet_plan = {f"Meal {meal+1}": {} for meal in range(user_inputs['number_of_meals'])}
# #         meal_counter = 0
# #         for food, quantity in food_quantities.items():
# #             meal_name = f"Meal {meal_counter % user_inputs['number_of_meals'] + 1}"
# #             diet_plan[meal_name][food] = quantity
# #             meal_counter += 1

# #         return diet_plan
# #     else:
# #         return "Optimization Failed"

# # # Function to create the diet optimization problem
# # def create_diet_optimization_problem(food_data, macros, user_inputs):
# #     problem = LpProblem("Diet_Optimization", LpMinimize)

# #     # Define variables for the quantity of each food item
# #     food_vars = LpVariable.dicts("Food", food_data.keys(), lowBound=0, cat='Continuous')

# #     # Objective function: Minimize total calories while meeting macro requirements
# #     problem += lpSum([food_vars[food] * food_data[food]['Calories'] for food in food_data])

# #     # Macro constraints
# #     problem += lpSum([food_vars[food] * food_data[food]['Protein'] for food in food_data]) >= macros['Protein']
# #     problem += lpSum([food_vars[food] * food_data[food]['Fats'] for food in food_data]) >= macros['Fats']
# #     problem += lpSum([food_vars[food] * food_data[food]['Carbs'] for food in food_data]) >= macros['Carbs']

# #     # Ensure each meal contains at least one food item
# #     for meal in range(user_inputs['number_of_meals']):
# #         problem += lpSum([food_vars[food] for food in user_inputs['likes']]) >= 1, f"Meal_{meal}_food_presence"

# #     # Solve the problem
# #     problem.solve()

# #     # Check if a feasible diet plan was found
# #     if LpStatus[problem.status] == 'Optimal':
# #         food_quantities = {food: food_vars[food].varValue for food in food_data if food_vars[food].varValue > 0}

# #         # Distribute the food into the number of meals
# #         diet_plan = {f"Meal {meal+1}": {} for meal in range(user_inputs['number_of_meals'])}
# #         meal_counter = 0
# #         for food, quantity in food_quantities.items():
# #             meal_name = f"Meal {meal_counter % user_inputs['number_of_meals'] + 1}"
# #             diet_plan[meal_name][food] = quantity
# #             meal_counter += 1

# #         return diet_plan
# #     else:
# #         return "Optimization Failed"

    

# # Assuming food_data is a dictionary containing food items with their macros and user preferences
# # Example: {'Chicken Breast': {'Protein': 31, 'Fats': 3.6, 'Carbs': 0}, ... }
# # user_inputs = {
# #     'gender': 'Male',
# #     'weight': 71,  # in kg
# #     'age':21,
# #     'height': 170,  # in cm
# #     'goal': 'Fat Loss',
# #     'goal_amount_per_week': 250,  # in grams
# #     'diet_preference': 'Non-Vegetarian',
# #     'likes': ['Chicken breast 100 grams', 'Boiled white rice 100 grams', 'Boiled whole eggs', 'Vegetable salad', 'Butter 30 grams','Fat free Milk 100 Ml'],
# #     'dislikes': ['Fish'],
# #     'number_of_meals': 5,
# #     'activity_level': 'Moderate',
# #     # ... more inputs as required
# # }


# # maintenance_calories = calculate_maintenance_calories(**user_inputs)
# # adjusted_calories = adjust_calories_for_goal(maintenance_calories, user_inputs['goal'], user_inputs['goal_amount_per_week'])
# # macros = calculate_macros(adjusted_calories, user_inputs['weight'], {'Protein': 0.3, 'Fats': 0.25, 'Carbs': 0.45})

# # ... [previous parts of your code] ...

# # Prepare arguments for calculate_maintenance_calories function
# maintenance_calories_args = {
#     'weight': user_inputs['weight'],
#     'height': user_inputs['height'],
#     'age': user_inputs['age'],
#     'gender': user_inputs['gender'],
#     'activity_level': user_inputs['activity_level']
# }

# # Calculate maintenance calories
# maintenance_calories = calculate_maintenance_calories(**maintenance_calories_args)

# # Adjust calories for the goal
# adjusted_calories = adjust_calories_for_goal(maintenance_calories, user_inputs['goal'], user_inputs['goal_amount_per_week'])

# # Calculate macros
# macros = calculate_macros(adjusted_calories, user_inputs['weight'], {'Protein': 0.3, 'Fats': 0.25, 'Carbs': 0.45})

# # ... [rest of your code for diet plan optimization] ...



# # maintenance_calories = calculate_maintenance_calories(**maintenance_calories_args)

# # Assuming we have a valid food_data dictionary
# diet_plan = create_diet_optimization_problem(food_data, macros, user_inputs
#                                             )

# print(diet_plan)







# from pulp import LpProblem, LpMinimize, LpVariable, LpStatus, lpSum
# from math import ceil
# from flask import Flask, render_template, request
# import pulp
# from random import shuffle, random, randint


# app = Flask(__name__)

# # Food data dictionary
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
#     # ... [Insert your complete food data here] ...
# }

# def calculate_maintenance_calories(weight, gender):
#     if gender == 'Male':
#         return weight * 28.5
#     else:
#         return weight * 24.5

# def adjust_calories_for_goal(calories, goal, goal_amount):
#     if goal == 'Fat Loss':
#         return max(calories - (goal_amount * 7700 / 7), 1300)
#     elif goal == 'Muscle Gain':
#         return calories + (goal_amount * 7700 / 7)
#     return calories

# def calculate_macros(calories, weight):
#     protein = weight * 2  # grams of protein
#     fats = weight * 0.5   # grams of fat
#     carbs = (calories - (protein * 4 + fats * 9)) / 4  # grams of carbs
#     return {'Protein': protein, 'Fats': fats, 'Carbs': carbs}

# def filter_food_by_preferences(food_data, diet_preference, protein_sources, fat_sources, carb_sources):
#     filtered_food = {}
#     for food, data in food_data.items():
#         if data['Category'].lower() == diet_preference.lower():
#             if (data['MacroType'] == 'Protein' and food in protein_sources) or \
#                (data['MacroType'] == 'Fat' and food in fat_sources) or \
#                (data['MacroType'] == 'Carb' and food in carb_sources):
#                 filtered_food[food] = data
#     return filtered_food

# from pulp import LpProblem, LpMinimize, LpVariable, LpStatus, lpSum

# def round_to_nearest(value, base=5):
#     return base * round(value / base)


# # def generate_diet_plan(gender, weight, diet_preference, protein_sources, fat_sources, carb_sources, goal, goal_amount, num_meals):
# #     # Calculate maintenance and adjusted calories
# #     maintenance_calories = calculate_maintenance_calories(weight, gender)
# #     adjusted_calories = adjust_calories_for_goal(maintenance_calories, goal, goal_amount)
    
# #     # Calculate macros based on the adjusted calories and user's weight
# #     macros = calculate_macros(adjusted_calories, weight)

# #     # Filter and shuffle the food items
# #     eligible_foods = filter_food_by_preferences(food_data, diet_preference, protein_sources, fat_sources, carb_sources)
# #     shuffled_food_items = list(eligible_foods.keys())
# #     random.shuffle(shuffled_food_items)

# #     # Define the optimization problem
# #     problem = LpProblem("Diet Optimization", LpMinimize)
# #     food_vars = LpVariable.dicts("Food", shuffled_food_items, lowBound=0)

# #     # Objective function and constraints
# #     problem += lpSum([food_vars[food] * eligible_foods[food]['Calories'] for food in shuffled_food_items])
# #     problem += lpSum([food_vars[food] * eligible_foods[food]['Protein'] for food in shuffled_food_items]) >= macros['Protein']
# #     problem += lpSum([food_vars[food] * eligible_foods[food]['Fats'] for food in shuffled_food_items]) >= macros['Fats']
# #     problem += lpSum([food_vars[food] * eligible_foods[food]['Carbs'] for food in shuffled_food_items]) >= macros['Carbs']
# #     problem.solve()

# #     if LpStatus[problem.status] == 'Optimal':
# #         # Initialize meal plan with a balanced distribution of macro types
# #         meal_plan = {f"Meal {i+1}": {'Protein': [], 'Fat': [], 'Carb': []} for i in range(num_meals)}
        
# #         # Distribute the food items into the meal plan ensuring a balance of macros
# #         for food in shuffled_food_items:
# #             if food_vars[food].varValue > 0:
# #                 quantity = max(round_to_nearest(food_vars[food].varValue), 10)
# #                 if food in protein_sources:
# #                     macro_type = 'Protein'
# #                 elif food in fat_sources:
# #                     macro_type = 'Fat'
# #                 else:
# #                     macro_type = 'Carb'
# #                 # Assign food items to meals in a round-robin fashion
# #                 for meal_name in meal_plan:
# #                     if not meal_plan[meal_name][macro_type]:
# #                         meal_plan[meal_name][macro_type].append((food, quantity))
# #                         break

# #         # Convert meal plan to desired format
# #         formatted_meal_plan = []
# #         for meal_name, macros in meal_plan.items():
# #             meal = {'name': meal_name, 'foods': []}
# #             for macro_type, items in macros.items():
# #                 for food, quantity in items:
# #                     meal['foods'].append({'item': food, 'quantity': quantity})
# #             formatted_meal_plan.append(meal)

# #         return formatted_meal_plan
# #     else:
# #         return "Optimization Failed."



# # def generate_diet_plan(gender, weight, diet_preference, protein_sources, fat_sources, carb_sources, goal, goal_amount, num_meals):
# #     # Calculate maintenance and adjusted calories
# #     maintenance_calories = calculate_maintenance_calories(weight, gender)
# #     adjusted_calories = adjust_calories_for_goal(maintenance_calories, goal, goal_amount)
# #     print("Protein sources:", protein_sources)
# #     print("Fat sources:", fat_sources)
# #     print("Carb sources:", carb_sources)

    
# #     # Calculate macros based on the adjusted calories and user's weight
# #     macros = calculate_macros(adjusted_calories, weight)

# #     # Filter and shuffle the food items
# #     eligible_foods = filter_food_by_preferences(food_data, diet_preference, protein_sources, fat_sources, carb_sources)
# #     shuffled_food_items = list(eligible_foods.keys())
# #     shuffle(shuffled_food_items)
# #     all_selected_foods = protein_sources + fat_sources + carb_sources
# #     shuffle(all_selected_foods)
# #     print("All selected foods:", all_selected_foods)
# #     print("Eligible foods:", eligible_foods)



# #     # Define the optimization problem
# #     problem = LpProblem("Diet Optimization", LpMinimize)
# #     food_vars = LpVariable.dicts("Food", shuffled_food_items, lowBound=0)
# #     print("Food variables:", food_vars)

# #     # Objective function and constraints
# #     problem += lpSum([food_vars[food] * eligible_foods[food]['Calories'] for food in shuffled_food_items])
# #     problem += lpSum([food_vars[food] * eligible_foods[food]['Protein'] for food in shuffled_food_items]) >= macros['Protein']
# #     problem += lpSum([food_vars[food] * eligible_foods[food]['Fats'] for food in shuffled_food_items]) >= macros['Fats']
# #     problem += lpSum([food_vars[food] * eligible_foods[food]['Carbs'] for food in shuffled_food_items]) >= macros['Carbs']
# #     problem.solve()

# # def generate_diet_plan(gender, weight, diet_preference, protein_sources, fat_sources, carb_sources, goal, goal_amount, num_meals):
# #     all_selected_foods = []

# #     # Calculate maintenance and adjusted calories
# #     maintenance_calories = calculate_maintenance_calories(weight, gender)
# #     adjusted_calories = adjust_calories_for_goal(maintenance_calories, goal, goal_amount)
    
# #     # Calculate macros based on the adjusted calories and user's weight
# #     macros = calculate_macros(adjusted_calories, weight)
# #     print("Protein sources:", protein_sources)
# #     print("Fat sources:", fat_sources)
# #     print("Carb sources:", carb_sources)


# #     # Filter and shuffle the food items
# #     eligible_foods = filter_food_by_preferences(food_data, diet_preference, protein_sources, fat_sources, carb_sources)
# #     shuffled_food_items = list(all_selected_foods)
# #     shuffle(shuffled_food_items)
# #     # eligible_foods = filter_food_by_preferences(food_data, diet_preference, protein_sources, fat_sources, carb_sources)
# #     # shuffled_food_items = list(eligible_foods.keys())
# #     # shuffle(shuffled_food_items)
# #     all_selected_foods = protein_sources + fat_sources + carb_sources

# #     print("All selected foods:", all_selected_foods)
# #     print("Eligible foods:", eligible_foods)

# #     # Define the optimization problem
    
# #     problem = LpProblem("Diet Optimization", LpMinimize)
# #     food_vars = {food: LpVariable("Food_" + food.replace(" ", "_"), lowBound=0) for food in shuffled_food_items}
# #     print("Food variables:", food_vars)

# #     # Objective function and constraints
# #     problem += lpSum([food_vars[food] * eligible_foods[food]['Calories'] for food in shuffled_food_items])
# #     problem += lpSum([food_vars[food] * eligible_foods[food]['Protein'] for food in shuffled_food_items]) >= macros['Protein']
# #     problem += lpSum([food_vars[food] * eligible_foods[food]['Fats'] for food in shuffled_food_items]) >= macros['Fats']
# #     problem += lpSum([food_vars[food] * eligible_foods[food]['Carbs'] for food in shuffled_food_items]) >= macros['Carbs']
    
# #     # Solve the problem
# #     problem.solve()

#     # if LpStatus[problem.status] == 'Optimal':
#     #     # Initialize meal plan with empty meals
#     #     diet_plan = {f"Meal {i+1}": {} for i in range(num_meals)}
        
#     #     # Distribute food into meals based on the linear programming solution
#     #     for food in shuffled_food_items:
#     #         var_value = food_vars[food].varValue
#     #         if var_value > 0:
#     #             quantity = max(round_to_nearest(var_value), 10)
#     #             meal_index = randint(1, num_meals)
#     #             meal_name = f"Meal {meal_index}"
#     #             diet_plan[meal_name].setdefault(food, 0)
#     #             diet_plan[meal_name][food] += quantity

#     #     # Convert the meal plan to a format that can be easily used in the template
#     #     formatted_meal_plan = [
#     #         {"name": meal_name, "foods": [{"item": item, "quantity": qty} for item, qty in foods.items()]}
#     #         for meal_name, foods in diet_plan.items()
#     #     ]

#     #     return formatted_meal_plan
#     # else:
#     #     return "Optimization Failed."

# #     if LpStatus[problem.status] == 'Optimal':
# #     # Split the selected food items into meals
# #      diet_plan = {f"Meal {i+1}": {} for i in range(num_meals)}
    
# #     # Extract the results and assign them to meal plans
# #     for food in shuffled_food_items:
# #         var_value = food_vars[food].varValue
# #         if var_value > 0:
# #             # Find the meal with the least amount of the macro type of the current food
# #             macro_type = eligible_foods[food]['MacroType']
# #             min_meal = min(diet_plan, key=lambda x: sum(eligible_foods[item]['Calories'] for item in diet_plan[x] if eligible_foods[item]['MacroType'] == macro_type))
            
# #             # Round the quantity to the nearest practical amount (like 5 or 10 grams)
# #             quantity = max(round_to_nearest(var_value), 10)
# #             diet_plan[min_meal].setdefault(food, 0)
# #             diet_plan[min_meal][food] += quantity

# #     return diet_plan
# # else:
# #     return "Optimization Failed."

#     # if LpStatus[problem.status] == 'Optimal':
#     #     # Split the selected food items into meals
#     #     diet_plan = {f"Meal {i+1}": {} for i in range(num_meals)}
        
#     #     # Extract the results and assign them to meal plans
#     #     for food in shuffled_food_items:
#     #         var_value = food_vars[food].varValue
#     #         if var_value > 0:
#     #             # Find the meal with the least amount of the macro type of the current food
#     #             macro_type = eligible_foods[food]['MacroType']
#     #             min_meal = min(diet_plan, key=lambda x: sum(diet_plan[x].get(f['MacroType'], 0) for f in diet_plan[x] if f['MacroType'] == macro_type))
                
#     #             # Round the quantity to the nearest practical amount (like 5 or 10 grams)
#     #             quantity = max(round_to_nearest(var_value), 10)
#     #             diet_plan[min_meal][food] = quantity

#     #     return diet_plan
#     # else:
#     #     return "Optimization Failed."

# def generate_diet_plan(gender, weight, diet_preference, protein_sources, fat_sources, carb_sources, goal, goal_amount, num_meals):
#     # Calculate maintenance and adjusted calories
#     maintenance_calories = calculate_maintenance_calories(weight, gender)
#     adjusted_calories = adjust_calories_for_goal(maintenance_calories, goal, goal_amount)
    
#     # Calculate macros based on the adjusted calories and user's weight
#     macros = calculate_macros(adjusted_calories, weight)

#     print("Protein sources:", protein_sources)
#     print("Fat sources:", fat_sources)
#     print("Carb sources:", carb_sources)


#     # Filter and shuffle the food items
#     eligible_foods = filter_food_by_preferences(food_data, diet_preference, protein_sources, fat_sources, carb_sources)
#     shuffled_food_items = list(eligible_foods.keys())
#     shuffle(shuffled_food_items)

#     print("All selected foods:", filter_food_by_preferences)
#     print("Eligible foods:", eligible_foods)


#     # Define the optimization problem
#     problem = LpProblem("Diet Optimization", LpMinimize)
#     food_vars = LpVariable.dicts("Food", shuffled_food_items, lowBound=0)
#     print("Food variables:", food_vars)


#     # Objective function and constraints
#     problem += lpSum([food_vars[food] * eligible_foods[food]['Calories'] for food in shuffled_food_items])
#     problem += lpSum([food_vars[food] * eligible_foods[food]['Protein'] for food in shuffled_food_items]) >= macros['Protein']
#     problem += lpSum([food_vars[food] * eligible_foods[food]['Fats'] for food in shuffled_food_items]) >= macros['Fats']
#     problem += lpSum([food_vars[food] * eligible_foods[food]['Carbs'] for food in shuffled_food_items]) >= macros['Carbs']
#     problem.solve()

#     if LpStatus[problem.status] == 'Optimal':
#         # Split the selected food items into meals
#         diet_plan = {f"Meal {i+1}": {} for i in range(num_meals)}
#         meal_number = 0
        
#         for food in shuffled_food_items:
#             if food_vars[food].varValue > 0:
#                 # Round the quantity to the nearest practical amount (like 5 or 10 grams)
#                 quantity = max(round_to_nearest(food_vars[food].varValue), 10)
#                 meal_name = f"Meal {(meal_number % num_meals) + 1}"
#                 diet_plan[meal_name][food] = quantity
#                 meal_number += 1

#         return diet_plan
#     else:
#         return "Optimization Failed."

   

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         gender = request.form.get('gender')
#         weight = float(request.form.get('weight'))
#         diet_preference = request.form.get('diet')
#         protein_source = request.form.getlist('protein_source[]')
#         fat_source = request.form.getlist('fat_source[]')
#         carb_source = request.form.getlist('carb_source[]')
#         goal = request.form.get('goal')
#         goal_amount = float(request.form.get('goal_amount'))
#         num_meals = int(request.form.get('num_meals'))

#         diet_plan = generate_diet_plan(gender, weight, diet_preference, protein_source, fat_source, carb_source, goal, goal_amount, num_meals)

#         if not isinstance(diet_plan, dict):
#             diet_plan = {}  # Ensure diet_plan is always a dictionary

#         return render_template('diet_plan.html', diet_plan=diet_plan)
#     else:
#         protein_sources = [food for food, details in food_data.items() if details["MacroType"] == "Protein"]
#         fat_sources = [food for food, details in food_data.items() if details["MacroType"] == "Fat"]
#         carb_sources = [food for food, details in food_data.items() if details["MacroType"] == "Carb"]
#         return render_template('index.html', protein_sources=protein_sources, fat_sources=fat_sources, carb_sources=carb_sources)
 
# if __name__ == '__main__':
#     app.run(debug=True)










# from flask import Flask, render_template, request
# import pulp
# from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus , value
# from math import ceil

# app = Flask(__name__)

# # Define your food_data dictionary here with actual data from the images provided
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

# # Function to calculate maintenance calories
# def calculate_maintenance_calories(weight, gender):
#     return weight * 28.5 if gender == 'Male' else weight * 24.5

# # Function to adjust calories for the goal
# def adjust_calories_for_goal(calories, goal, goal_amount):
#     calorie_change_per_week = goal_amount * 7700 / 7
#     return calories + calorie_change_per_week if goal == 'Muscle Gain' else max(calories - calorie_change_per_week, 1300)

# # Function to calculate macros
# def calculate_macros(calories, weight):
#     protein = weight * 2
#     fats = weight * 0.5
#     carbs = (calories - (protein * 4 + fats * 9)) / 4
#     return {'Protein': protein, 'Fats': fats, 'Carbs': carbs}

# # Function to round quantities to nearest practical amount
# def round_to_nearest_practical_amount(quantity):
#     return ceil(quantity / 10) * 10

# # Function to generate the diet plan
# def generate_diet_plan(gender, weight, diet_preference, protein_sources, fat_sources, carb_sources, goal, goal_amount, num_meals):
#     # Validate input types
#     if not all(isinstance(v, (int, float)) for v in [weight, goal_amount, num_meals]):
#         return None, "Weight, goal amount, and number of meals must be numbers."

#     maintenance_calories = calculate_maintenance_calories(weight, gender)
#     adjusted_calories = adjust_calories_for_goal(maintenance_calories, goal, goal_amount)
#     macros = calculate_macros(adjusted_calories, weight)

#     # Create the LP problem
#     problem = LpProblem("Diet Plan", LpMinimize)

#     # Variables for the amount of each food item to include in the diet
#     food_vars = LpVariable.dicts("Food", food_data.keys(), lowBound=0)

#     # Additional variables to handle the absolute values in the objective function for macros
#     protein_diff = LpVariable("Protein_diff", lowBound=0)
#     fats_diff = LpVariable("Fats_diff", lowBound=0)
#     carbs_diff = LpVariable("Carbs_diff", lowBound=0)

#     # Objective function: Minimize the sum of the absolute differences of macros
#     problem += protein_diff + fats_diff + carbs_diff

#     # Constraints to calculate the absolute difference for protein
#     problem += lpSum([food_vars[food] * food_data[food]['Protein'] for food in protein_sources]) - macros['Protein'] <= protein_diff
#     problem += -lpSum([food_vars[food] * food_data[food]['Protein'] for food in protein_sources]) + macros['Protein'] <= protein_diff

#     # Constraints to calculate the absolute difference for fats
#     problem += lpSum([food_vars[food] * food_data[food]['Fats'] for food in fat_sources]) - macros['Fats'] <= fats_diff
#     problem += -lpSum([food_vars[food] * food_data[food]['Fats'] for food in fat_sources]) + macros['Fats'] <= fats_diff

#     # Constraints to calculate the absolute difference for carbs
#     problem += lpSum([food_vars[food] * food_data[food]['Carbs'] for food in carb_sources]) - macros['Carbs'] <= carbs_diff
#     problem += -lpSum([food_vars[food] * food_data[food]['Carbs'] for food in carb_sources]) + macros['Carbs'] <= carbs_diff

#     # Dietary preference constraints (e.g., vegetarian, non-vegetarian, vegan)
#     for food in food_data.keys():
#         if food_data[food]['Category'].lower() != diet_preference.lower() and food_data[food]['Category'] != "All":
#             problem += food_vars[food] == 0

#     # Solve the problem
#     status = problem.solve()

#     # Check if the optimization was successful and create the diet plan
#     if LpStatus[status] == 'Optimal':
#         diet_plan = {f"Meal {meal + 1}": {} for meal in range(num_meals)}
#         for food in food_data.keys():
#             quantity = value(food_vars[food])
#             if quantity and quantity > 0:
#                 for meal in range(num_meals):
#                     meal_name = f"Meal {meal + 1}"
#                     diet_plan[meal_name][food] = round_to_nearest_practical_amount(quantity / num_meals)
#         return diet_plan, None
#     else:
#         return None, "Optimization Failed. Please adjust your inputs and try again."



# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         gender = request.form.get('gender')
#         weight = float(request.form.get('weight'))
#         diet_preference = request.form.get('diet')
#         protein_sources = request.form.getlist('protein_source[]')
#         fat_sources = request.form.getlist('fat_source[]')
#         carb_sources = request.form.getlist('carb_source[]')
#         goal = request.form.get('goal')
#         goal_amount = float(request.form.get('goal_amount'))
#         num_meals = int(request.form.get('num_meals'))
          


#         diet_plan = generate_diet_plan(gender, weight, diet_preference, protein_sources, fat_sources, carb_sources, goal, goal_amount, num_meals)

#         if diet_plan:
#             return render_template('diet_plan.html', diet_plan=diet_plan)
#         # else:
#         #     return render_template('error.html', message="Unable to generate diet plan.")
#     else:
#      protein_sources = [food for food, details in food_data.items() if details["MacroType"] == "Protein"]
#      fat_sources = [food for food, details in food_data.items() if details["MacroType"] == "Fat"]
#      carb_sources = [food for food, details in food_data.items() if details["MacroType"] == "Carb"]
#      return render_template('index.html', protein_sources=protein_sources, fat_sources=fat_sources, carb_sources=carb_sources)

# if __name__ == '__main__':
#     app.run(debug=True)





# from flask import Flask, render_template, request
# import pulp
# from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus
# from math import ceil



# app = Flask(__name__)

# # Food data dictionary
# food_data = {
#      "Full fat milk 100 ml": {"Calories": 89, "Protein": 3.3, "Fats": 6.2, "Carbs": 5, "Category": "Vegetarian", "MacroType": "Fat"},
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
#     # ... [Insert your complete food data here] ...
# }

# def calculate_maintenance_calories(weight, gender):
#     if gender == 'Male':
#         return weight * 28.5
#     else:
#         return weight * 24.5

# def adjust_calories_for_goal(calories, goal, goal_amount):
#     if goal == 'Fat Loss':
#         return max(calories - (goal_amount * 7700 / 7), 1300)
#     elif goal == 'Muscle Gain':
#         return calories + (goal_amount * 7700 / 7)
#     return calories

# def calculate_macros(calories, weight):
#     protein = weight * 2  # grams of protein
#     fats = weight * 0.5   # grams of fat
#     carbs = (calories - (protein * 4 + fats * 9)) / 4  # grams of carbs
#     return {'Protein': protein, 'Fats': fats, 'Carbs': carbs}


# MIN_QUANTITY = 10

# def calculate_maintenance_calories(weight, gender):
#     if gender == 'Male':
#         return weight * 28.5
#     else:
#         return weight * 24.5

# def adjust_calories_for_goal(calories, goal, goal_amount):
#     if goal == 'Fat Loss':
#         return max(calories - (goal_amount * 7700 / 7), 1300)
#     elif goal == 'Muscle Gain':
#         return calories + (goal_amount * 7700 / 7)
#     return calories

# def calculate_macros(calories, weight):
#     protein = weight * 2  # grams of protein
#     fats = weight * 0.5   # grams of fat
#     carbs = (calories - (protein * 4 + fats * 9)) / 4  # grams of carbs
#     return {'Protein': protein, 'Fats': fats, 'Carbs': carbs}


# MIN_FOOD_QUANTITY = 10  # The minimum amount of food (in grams) to be included in a meal


# def round_to_nearest_practical_amount(quantity, food_item, food_data):
#     # Define standard serving sizes for each category of food
#     standard_serving_sizes = {
#         'P': 100,  # Proteins (grams per serving)
#         'F': 30,   # Fats
#         'C': 50,   # Carbs
#     }
    
#     # Identify the macro type of the food item
#     macro_type = food_data[food_item]['MacroType']
    
#     # Get the standard serving size for the macro type
#     standard_serving_size = standard_serving_sizes.get(macro_type, 10)
    
#     # If the quantity is less than the standard serving size, round up to the standard serving size
#     if quantity < standard_serving_size:
#         return standard_serving_size
    
#     # Otherwise, round to the nearest multiple of the standard serving size
#     return ceil(quantity / standard_serving_size) * standard_serving_size


# def generate_diet_plan(gender, weight, diet_preference, protein_sources, fat_sources, carb_sources, goal, goal_amount, num_meals, food_data):

#     maintenance_calories = calculate_maintenance_calories(weight, gender)
#     adjusted_calories = adjust_calories_for_goal(maintenance_calories, goal, goal_amount)
    
#     # Calculate macros based on the adjusted calories and user's weight
#     macros = calculate_macros(adjusted_calories, weight)
#     # ... [previous code to calculate macros] ...

#     # Initialize the problem
#     problem = LpProblem("Diet_Optimization", LpMinimize)
    
#     # Create variables for each food item
#     food_vars = {food: LpVariable(f"var_{food}", lowBound=0) for food in food_data}
    
#     # Objective function: Minimize total calories
#     problem += lpSum([food_vars[food] * food_data[food]['Calories'] for food in food_data])
    
#     # Macro constraints
#     problem += lpSum([food_vars[food] * food_data[food]['Protein'] for food in food_data]) >= macros['Protein']
#     problem += lpSum([food_vars[food] * food_data[food]['Fats'] for food in food_data]) >= macros['Fats']
#     problem += lpSum([food_vars[food] * food_data[food]['Carbs'] for food in food_data]) >= macros['Carbs']
    
#     # Ensure that the minimum quantity for each selected food item is included
#     for food in protein_sources + fat_sources + carb_sources:
#         if food in food_data:
#             problem += food_vars[food] >= MIN_FOOD_QUANTITY

#     # Solve the problem
#     problem.solve()
    
#     # Generate diet plan if the solution is optimal
#     if LpStatus[problem.status] == 'Optimal':
#         diet_plan = {f"Meal {meal + 1}": {} for meal in range(num_meals)}
#         for food in food_data:
#             quantity = food_vars[food].varValue
#             if quantity and quantity > 0:
#                 # Round the total quantity to the nearest practical amount
#                 practical_quantity = round_to_nearest_practical_amount(quantity, food, food_data)
#                 # Divide the total practical quantity evenly among the number of meals
#                 quantity_per_meal = practical_quantity / num_meals
#                 for meal in range(num_meals):
#                     meal_name = f"Meal {meal + 1}"
#                     # Round the quantity per meal to the nearest practical amount
#                     diet_plan[meal_name][food] = round_to_nearest_practical_amount(quantity_per_meal, food, food_data)
#         return diet_plan
#     else:
#         return None, "Optimization Failed. Please adjust your inputs and try again."




# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':

#         print(request.form)  # Add this line for debugging

#         gender = request.form.get('gender')
#         weight = float(request.form.get('weight'))
#         diet_preference = request.form.get('diet')
#         protein_source = request.form.getlist('protein_source[]')
#         fat_source = request.form.getlist('fat_source[]')
#         carb_source = request.form.getlist('carb_source[]')
#         goal = request.form.get('goal')
#         goal_amount = float(request.form.get('goal_amount'))
#         num_meals = int(request.form.get('num_meals'))

#         diet_plan = generate_diet_plan(gender, weight, diet_preference, protein_source, fat_source, carb_source, goal, goal_amount, num_meals, food_data)

#         if not isinstance(diet_plan, dict):
#             diet_plan = {}  # Ensure diet_plan is always a dictionary
   

#         return render_template('diet_plan.html', diet_plan=diet_plan)
#     else:
#         protein_sources = [food for food, details in food_data.items() if details["MacroType"] == "Protein"]
#         fat_sources = [food for food, details in food_data.items() if details["MacroType"] == "Fat"]
#         carb_sources = [food for food, details in food_data.items() if details["MacroType"] == "Carb"]
#         return render_template('index.html', protein_sources=protein_sources, fat_sources=fat_sources, carb_sources=carb_sources)

# if __name__ == '__main__':
#     app.run(debug=True)








# def round_to_nearest_practical_amount(quantity):
#     if quantity < MIN_FOOD_QUANTITY:
#         return ceil(quantity)
#     else:
#         return ceil(quantity / MIN_FOOD_QUANTITY) * MIN_FOOD_QUANTITY

# def generate_diet_plan(gender, weight, diet_preference, protein_sources, fat_sources, carb_sources, goal, goal_amount, num_meals, food_data):
#     maintenance_calories = calculate_maintenance_calories(weight, gender)
#     adjusted_calories = adjust_calories_for_goal(maintenance_calories, goal, goal_amount)
#     macros = calculate_macros(adjusted_calories, weight)
    
#     # Filter the food_data to include only the items that match the diet preference and macro type
#     eligible_foods_dict = {food: details for food, details in food_data.items() 
#                            if (details['Category'] == diet_preference and 
#                                ((details['MacroType'] == 'Protein' and food in protein_sources) or
#                                 (details['MacroType'] == 'Fat' and food in fat_sources) or
#                                 (details['MacroType'] == 'Carb' and food in carb_sources)))}
    
#     # Define the problem
#     problem = LpProblem("Diet_Optimization", LpMinimize)
    
#     # Create variables for each food item
#     food_vars = {food: LpVariable(f"var_{food}", lowBound=MIN_FOOD_QUANTITY/num_meals) for food in eligible_foods_dict}
    
#     # Objective function to minimize total calories
#     problem += lpSum([food_vars[food] * eligible_foods_dict[food]['Calories'] for food in eligible_foods_dict])
    
#     # Macro constraints
#     problem += lpSum([food_vars[food] * eligible_foods_dict[food]['Protein'] for food in eligible_foods_dict]) >= macros['Protein']
#     problem += lpSum([food_vars[food] * eligible_foods_dict[food]['Fats'] for food in eligible_foods_dict]) >= macros['Fats']
#     problem += lpSum([food_vars[food] * eligible_foods_dict[food]['Carbs'] for food in eligible_foods_dict]) >= macros['Carbs']
    
#     # Solve the problem
#     problem.solve()
    
#     # Check if the solution is optimal
#     if LpStatus[problem.status] == 'Optimal':
#         diet_plan = {f"Meal {meal + 1}": {} for meal in range(num_meals)}
#         for food in eligible_foods_dict:
#             quantity = food_vars[food].varValue
#             if quantity and quantity > 0:
#                 practical_quantity = round_to_nearest_practical_amount(quantity)
#                 quantity_per_meal = practical_quantity / num_meals
#                 for meal in range(num_meals):
#                     meal_name = f"Meal {meal + 1}"
#                     diet_plan[meal_name][food] = round_to_nearest_practical_amount(quantity_per_meal)
#         return diet_plan
#     else:
#         return None, "Optimization Failed. Please adjust your inputs and try again."


# def round_to_nearest_practical_amount(quantity):
#     if quantity < 10:
#         return ceil(quantity)
#     else:
#         return ceil(quantity / 10) * 10





# def generate_diet_plan(gender, weight, diet_preference, protein_sources, fat_sources, carb_sources, goal, goal_amount, num_meals):
#     maintenance_calories = calculate_maintenance_calories(weight, gender)
#     adjusted_calories = adjust_calories_for_goal(maintenance_calories, goal, goal_amount)
#     macros = calculate_macros(adjusted_calories, weight)
#     print("Protein preferences:", protein_sources)
#     print("Fat preferences:", fat_sources)
#     print("Carb preferences:", carb_sources)

#     eligible_foods_dict = {food: details for food, details in food_data.items() 
#                       if (details['Category'] == diet_preference and 
#                           (details['MacroType'] == 'Protein' and any(protein in food for protein in protein_sources) or
#                            details['MacroType'] == 'Fat' and any(fat in food for fat in fat_sources) or
#                            details['MacroType'] == 'Carb' and any(carb in food for carb in carb_sources)))}
#     # ... [Your existing code for calculating calories and macros] ...

#     # Assuming MIN_FOOD_QUANTITY is the minimum amount of each food you want in the diet
#     MIN_FOOD_QUANTITY = 10  # For example, 10 grams

#     # Combine all food sources
#     all_selected_sources = set(protein_sources + fat_sources + carb_sources)

#     # Initialize the problem
#     problem = LpProblem("Diet_Optimization", LpMinimize)

#     # Define variables for food quantities and whether they are included
#     food_vars = LpVariable.dicts("Food_Quantity", eligible_foods_dict.keys(), lowBound=0)
#     food_included_vars = LpVariable.dicts("Food_Included", eligible_foods_dict.keys(), cat='Binary')

#     # Objective function: Minimize total calories while considering the inclusion of selected foods
#     problem += lpSum([food_vars[food] * details['Calories'] for food, details in eligible_foods_dict.items()])

#     # Constraints to meet macro requirements
#     problem += lpSum([food_vars[food] * details['Protein'] for food, details in eligible_foods_dict.items()]) >= macros['Protein']
#     problem += lpSum([food_vars[food] * details['Fats'] for food, details in eligible_foods_dict.items()]) >= macros['Fats']
#     problem += lpSum([food_vars[food] * details['Carbs'] for food, details in eligible_foods_dict.items()]) >= macros['Carbs']

#     # Constraints to ensure all selected foods are included
#     for food in all_selected_sources:
#         if food in eligible_foods_dict:
#             # Food must be included if selected, linking quantity to binary inclusion variable
#             problem += food_vars[food] >= MIN_FOOD_QUANTITY * food_included_vars[food]
#             # Ensure that food_included_vars is set to 1 (true) if the food is selected
#             problem += food_included_vars[food] >= 1

    
            


#     # Solve the problem
#     problem.solve()

#     # Generate diet plan if the solution is optimal
#     if LpStatus[problem.status] == 'Optimal':
#         diet_plan = {f"Meal {meal + 1}": {} for meal in range(num_meals)}
#         for food in eligible_foods_dict.keys():
#             if food in all_selected_sources:
#                 total_quantity = food_vars[food].varValue
#                 quantity_per_meal = total_quantity / num_meals
#                 for meal in range(num_meals):
#                     diet_plan[f"Meal {meal + 1}"].setdefault(food, 0)
#                     diet_plan[f"Meal {meal + 1}"][food] += quantity_per_meal
        
            
#         return diet_plan
#     else:
#         return None, "Optimization Failed. Please adjust your inputs and try again."














# def generate_diet_plan(gender, weight, diet_preference, protein_sources, fat_sources, carb_sources, goal, goal_amount, num_meals):
#     # Calculate maintenance and adjusted calories
#     maintenance_calories = calculate_maintenance_calories(weight, gender)
#     adjusted_calories = adjust_calories_for_goal(maintenance_calories, goal, goal_amount)
#     macros = calculate_macros(adjusted_calories, weight)
#     print("Protein preferences:", protein_sources)
#     print("Fat preferences:", fat_sources)
#     print("Carb preferences:", carb_sources)
    
#     # Filter eligible foods based on user preferences
#     eligible_foods = {food: details for food, details in food_data.items() 
#                       if (details['Category'] == diet_preference and 
#                           (details['MacroType'] == 'Protein' and any(protein in food for protein in protein_sources) or
#                            details['MacroType'] == 'Fat' and any(fat in food for fat in fat_sources) or
#                            details['MacroType'] == 'Carb' and any(carb in food for carb in carb_sources)))}
    
#     # Setting up the optimization problem
#     problem = LpProblem("Diet_Optimization", LpMinimize)
#     food_vars = LpVariable.dicts("Food", eligible_foods.keys(), lowBound=0)
    
#     # Objective function: Minimize total calories
#     problem += lpSum([food_vars[food] * details['Calories'] for food, details in eligible_foods.items()])
    
#     # Constraints to ensure macro requirements are met
#     problem += lpSum([food_vars[food] * details['Protein'] for food, details in eligible_foods.items()]) >= macros['Protein']
#     problem += lpSum([food_vars[food] * details['Fats'] for food, details in eligible_foods.items()]) >= macros['Fats']
#     problem += lpSum([food_vars[food] * details['Carbs'] for food, details in eligible_foods.items()]) >= macros['Carbs']
    
#     # Solve the problem
#     problem.solve()
    
#     # Check if the solution is optimal and generate diet plan
#     if LpStatus[problem.status] == 'Optimal':
#         diet_plan = {f"Meal {meal + 1}": {} for meal in range(num_meals)}
#         for food in eligible_foods.keys():
#             quantity = food_vars[food].varValue
#             if quantity > 0:
#                 split_quantity = quantity / num_meals
#                 for meal in range(num_meals):
#                     diet_plan[f"Meal {meal + 1}"][food] = split_quantity
#         return diet_plan
#     else:
#         return None, "Optimization Failed. Please adjust your inputs and try again."

# # ... [The rest of your Flask app code] ...







# def generate_diet_plan(gender, weight, diet_preference, protein_prefs, fat_prefs, carb_prefs, goal, goal_amount, num_meals):
#     # Calculate maintenance and adjusted calories
#     maintenance_calories = calculate_maintenance_calories(weight, gender)
#     adjusted_calories = adjust_calories_for_goal(maintenance_calories, goal, goal_amount)
#     macros = calculate_macros(adjusted_calories, weight)

#     # Start with all foods matching the diet preference
#     all_foods = {food: details for food, details in food_data.items() if details['Category'] == diet_preference}
#     eligible_foods = set()

#     # Apply filters based on the user's macro preferences
#     if 'All' not in protein_prefs:
#         for pref in protein_prefs:
#             eligible_foods.update({food for food, details in all_foods.items() if details['MacroType'] == 'Protein' and pref.lower() in food.lower()})

#     if 'All' not in fat_prefs:
#         for pref in fat_prefs:
#             eligible_foods.update({food for food, details in all_foods.items() if details['MacroType'] == 'Fat' and pref.lower() in food.lower()})

#     if 'All' not in carb_prefs:
#         for pref in carb_prefs:
#             eligible_foods.update({food for food, details in all_foods.items() if details['MacroType'] == 'Carb' and pref.lower() in food.lower()})

#     # Check if there are any eligible foods left after filtering
#     if not eligible_foods:
#         return None, "No eligible foods found based on the selected preferences."

#     # Convert the set to a dictionary for pulp
#     eligible_foods_dict = {food: all_foods[food] for food in eligible_foods}

#     # Setting up the linear programming problem
#     problem = pulp.LpProblem("Diet Optimization", pulp.LpMinimize)
#     food_vars = pulp.LpVariable.dicts("Food", eligible_foods_dict.keys(), lowBound=0)

#     # Objective function - minimize total calorie intake
#     problem += pulp.lpSum([food_vars[food] * details['Calories'] for food, details in eligible_foods_dict.items()])

#     # Constraints to meet the macro requirements
#     problem += pulp.lpSum([food_vars[food] * details['Protein'] for food, details in eligible_foods_dict.items()]) >= macros['Protein'], "ProteinRequirement"
#     problem += pulp.lpSum([food_vars[food] * details['Fats'] for food, details in eligible_foods_dict.items()]) >= macros['Fats'], "FatRequirement"
#     problem += pulp.lpSum([food_vars[food] * details['Carbs'] for food, details in eligible_foods_dict.items()]) >= macros['Carbs'], "CarbRequirement"

#     # Solve the problem
#     problem.solve()

#     # Check if the solution is optimal
#     if pulp.LpStatus[problem.status] == 'Optimal':
#         # Create a diet plan with evenly distributed meals
#         diet_plan = {f"Meal {meal + 1}": {} for meal in range(num_meals)}
#         for food in eligible_foods_dict:
#             total_quantity = food_vars[food].varValue
#             if total_quantity > 0:
#                 # Round the total quantity to a practical amount before dividing by the number of meals
#                 practical_total_quantity = round_to_nearest_practical_amount(total_quantity)
#                 for meal in range(num_meals):
#                     # Distribute the total quantity across the number of meals
#                     # Ensure that the quantity per meal is practical
#                     quantity_per_meal = practical_total_quantity / num_meals
#                     diet_plan[f"Meal {meal + 1}"][food] = round(quantity_per_meal, 2)  # Round to two decimal places for practicality
#         return diet_plan
#     else:
#         return None, "Optimization Failed. Please adjust your inputs and try again."


# def generate_diet_plan(gender, weight, diet_preference, protein_prefs, fat_prefs, carb_prefs, goal, goal_amount, num_meals):
#     # Calculate maintenance and adjusted calories
#     maintenance_calories = calculate_maintenance_calories(weight, gender)
#     adjusted_calories = adjust_calories_for_goal(maintenance_calories, goal, goal_amount)
#     macros = calculate_macros(adjusted_calories, weight)

#     # Start with all foods matching the diet preference
#     all_foods = {food: details for food, details in food_data.items() if details['Category'] == diet_preference}

#     # Apply filters based on the user's macro preferences
#     eligible_foods = {}
#     for macro_type, prefs in zip(['Protein', 'Fat', 'Carb'], [protein_prefs, fat_prefs, carb_prefs]):
#         if 'All' not in prefs:
#             for pref in prefs:
#                 eligible_foods.update({food: details for food, details in all_foods.items()
#                                        if details['MacroType'] == macro_type and pref.lower() in food.lower()})

#     # Check if there are any eligible foods left after filtering
#     if not eligible_foods:
#         return None, "No eligible foods found based on the selected preferences."

#     # Setting up the linear programming problem
#     problem = LpProblem("Diet Optimization", LpMinimize)
#     food_vars = LpVariable.dicts("Food", eligible_foods.keys(), lowBound=0)

#     # Objective function - minimize total calorie intake
#     problem += lpSum([food_vars[food] * details['Calories'] for food, details in eligible_foods.items()])

#     # Constraints to meet the macro requirements
#     problem += lpSum([food_vars[food] * details['Protein'] for food, details in eligible_foods.items()]) == macros['Protein'], "ProteinRequirement"
#     problem += lpSum([food_vars[food] * details['Fats'] for food, details in eligible_foods.items()]) == macros['Fats'], "FatRequirement"
#     problem += lpSum([food_vars[food] * details['Carbs'] for food, details in eligible_foods.items()]) == macros['Carbs'], "CarbRequirement"

#     # Solve the problem
#     problem.solve()

#     # Check if the solution is optimal
#     if LpStatus[problem.status] == 'Optimal':
#         # Create a diet plan with evenly distributed meals
#         diet_plan = {f"Meal {meal + 1}": {} for meal in range(num_meals)}
#         for food in eligible_foods:
#             total_quantity = food_vars[food].varValue
#             if total_quantity > 0:
#                 # Distribute the total quantity across the number of meals
#                 quantity_per_meal = round(total_quantity / num_meals, 2)  # round to two decimal places for practicality
#                 for meal in range(num_meals):
#                     diet_plan[f"Meal {meal + 1}"][food] = quantity_per_meal
#         return diet_plan
#     else:
#         return None, "Optimization Failed. Please adjust your inputs and try again."


# print("Protein preferences:", protein_pref)
# print("Fat preferences:", fat_pref)
# print("Carb preferences:", carb_pref)

 


# def generate_diet_plan(gender, weight, diet_preference, protein_pref, fat_pref, carb_pref, goal, goal_amount, num_meals):

#     # Calculate maintenance and adjusted calories
#     maintenance_calories = calculate_maintenance_calories(weight, gender)
#     adjusted_calories = adjust_calories_for_goal(maintenance_calories, goal, goal_amount)
#     macros = calculate_macros(adjusted_calories, weight)

#     print("Protein preferences:", protein_pref)
#     print("Fat preferences:", fat_pref)
#     print("Carb preferences:", carb_pref)





#     # Start with all foods matching the diet preference
#     all_foods = {food: details for food, details in food_data.items() if details['Category'] == diet_preference}
#     eligible_foods = set()

#     # Assuming 'protein_source', 'fat_source', and 'carb_source' are lists of user's preferences for each macronutrient

# # Filter eligible foods based on protein preferences



#     # Apply protein filter if not 'All'
#     # if 'All' not in protein_pref:
#     #     for pref in protein_pref:
#     #         eligible_foods.update({food for food, details in all_foods.items() if details['MacroType'] == 'Protein' and pref.lower() in food.lower()})

#     # # Apply fat filter if not 'All'
#     # if 'All' not in fat_pref:
#     #     for pref in fat_pref:
#     #         eligible_foods.update({food for food, details in all_foods.items() if details['MacroType'] == 'Fat' and pref.lower() in food.lower()})

#     # # Apply carb filter if not 'All'
#     # if 'All' not in carb_pref:
#     #     for pref in carb_pref:
#     #         eligible_foods.update({food for food, details in all_foods.items() if details['MacroType'] == 'Carb' and pref.lower() in food.lower()})
#     #         print("Eligible foods after filtering:", eligible_foods)


#      # Apply protein filter if not 'All'
#     if 'All' not in protein_pref:
#         for pref in protein_pref:
#             eligible_foods.update({food for food, details in all_foods.items() if details['MacroType'] == 'Protein' and pref.lower() in food.lower()})

#     # Apply fat filter if not 'All'
#     if 'All' not in fat_pref:
#         for pref in fat_pref:
#             eligible_foods.update({food for food, details in all_foods.items() if details['MacroType'] == 'Fat' and pref.lower() in food.lower()})

#     # Apply carb filter if not 'All'
#     if 'All' not in carb_pref:
#         for pref in carb_pref:
#             eligible_foods.update({food for food, details in all_foods.items() if details['MacroType'] == 'Carb' and pref.lower() in food.lower()})
    
#     # Convert the set back to a dictionary to use the 'items' method
#     eligible_foods_dict = {food: all_foods[food] for food in eligible_foods}



#     # Check if there are any eligible foods left after filtering
#     if not eligible_foods:
#         print("No eligible foods found based on the selected preferences.")
#         return None, "No eligible foods found based on the selected preferences."

#     # Filter eligible foods with their details
#     eligible_foods_dict = {food: all_foods[food] for food in eligible_foods}

#     # Setting up the linear programming problem
#     problem = pulp.LpProblem("Diet Optimization", pulp.LpMinimize)
#     food_vars = pulp.LpVariable.dicts("Food", eligible_foods_dict.keys(), lowBound=0.01)

#     # Objective function
#     problem += pulp.lpSum([food_vars[food] * details['Calories'] for food, details in eligible_foods_dict.items()])

#     # Constraints
#     problem += pulp.lpSum([food_vars[food] * details['Protein'] for food, details in eligible_foods_dict.items()]) >= max(macros['Protein'], 0)
#     problem += pulp.lpSum([food_vars[food] * details['Fats'] for food, details in eligible_foods_dict.items()]) >= max(macros['Fats'], 0)
#     problem += pulp.lpSum([food_vars[food] * details['Carbs'] for food, details in eligible_foods_dict.items()]) >= max(macros['Carbs'], 0)

#     # Solving the problem
#     problem.solve()

#     # Check if the solution is optimal
#     if pulp.LpStatus[problem.status] == 'Optimal':
#         diet_plan = {f"Meal {meal + 1}": {} for meal in range(num_meals)}
#         for food in eligible_foods_dict:
#             total_quantity = food_vars[food].varValue
#             if total_quantity > 0:
#                 for meal in range(num_meals):
#                     diet_plan[f"Meal {meal + 1}"][food] = total_quantity / num_meals
#         return diet_plan
#     else:
#         return None, "Optimization Failed. Please adjust your inputs and try again."










# def generate_diet_plan(gender, weight, diet_preference, protein_pref, fat_pref, carb_pref, goal, goal_amount, num_meals):
#     maintenance_calories = calculate_maintenance_calories(weight, gender)
#     adjusted_calories = adjust_calories_for_goal(maintenance_calories, goal, goal_amount)
#     macros = calculate_macros(adjusted_calories, weight)

#     eligible_foods = {food: details for food, details in food_data.items() if details['Category'] == diet_preference}

#     print("Eligible foods before protein filter:", eligible_foods)
#     if 'All' not in protein_pref:
#         eligible_foods = {food: details for food, details in eligible_foods.items()
#                           if details['MacroType'] == 'Protein' and any(pref.lower() in food.lower() for pref in protein_pref)}
#         print("Eligible foods after protein filter:", eligible_foods)
        

#     if 'All' not in fat_pref:
#         eligible_foods = {food: details for food, details in eligible_foods.items()
#                           if details['MacroType'] == 'Fat' and any(pref.lower() in food.lower() for pref in fat_pref)}
#         print("Eligible foods after fat filter:", eligible_foods)

#     if 'All' not in carb_pref:
#         eligible_foods = {food: details for food, details in eligible_foods.items()
#                           if details['MacroType'] == 'Carb' and any(pref.lower() in food.lower() for pref in carb_pref)}
#         print("Eligible foods after carb filter:", eligible_foods)

   

   

    

    



#     # if protein_pref != 'All':
#     #     eligible_foods = {food: details for food, details in eligible_foods.items()
#     #                       if details['MacroType'] == 'Protein' and protein_pref.lower() in food.lower()}
        
#     #     print("Eligible foods after protein filter:", eligible_foods)
      
#     # #Filter based on user's fat preferenc

#     # if fat_pref != 'All':
#     #     eligible_foods = {food: details for food, details in eligible_foods.items()
#     #                       if details['MacroType'] == 'Fat' and fat_pref.lower() in food.lower()}
#     #     print("Eligible foods after fat filter:", eligible_foods)


#     # # Filter based on user's carb preference
#     # if carb_pref != 'All':
#     #     eligible_foods = {food: details for food, details in eligible_foods.items()
#     #                       if details['MacroType'] == 'Carb' and carb_pref.lower() in food.lower()}
#     #     print("Eligible foods after protein filter:", eligible_foods)


#     # print("After filtering based on user preferences:", eligible_foods)



#     # Ensure there are eligible foods before continuing
#     if not eligible_foods:
#         print("No eligible foods found based on the selected preferences.")
#         return None, "No eligible foods found based on the selected preferences."
#     eligible_foods = {food: details for food, details in food_data.items() if details['Category'] == diet_preference}

#     # if protein_pref != 'All':
#     #     eligible_foods = {food: details for food, details in eligible_foods.items()
#     #                       if details['MacroType'] == 'Protein' and protein_pref.lower() in food.lower()}

#     # # Filter based on user's fat preference
#     # if fat_pref != 'All':
#     #     eligible_foods = {food: details for food, details in eligible_foods.items()
#     #                       if details['MacroType'] == 'Fat' and fat_pref.lower() in food.lower()}

#     # # Filter based on user's carb preference
#     # if carb_pref != 'All':
#     #     eligible_foods = {food: details for food, details in eligible_foods.items()
#     #                       if details['MacroType'] == 'Carb' and carb_pref.lower() in food.lower()}

#     # # Check if there are any eligible foods left after filtering
#     # if not eligible_foods:
#     #     return None, "No eligible foods found based on the selected preferences."

#     # Further filter based on macro preferences if not 'All'
#     # if protein_pref != 'All':
#     #     filtered_protein = {food: details for food, details in eligible_foods.items() if details['MacroType'] == 'Protein'}
#     #     print("After protein preference filter:", filtered_protein)
#     #     eligible_foods = filtered_protein if filtered_protein else eligible_foods

#     # if fat_pref != 'All':
#     #     filtered_fat = {food: details for food, details in eligible_foods.items() if details['MacroType'] == 'Fat'}
#     #     print("After fat preference filter:", filtered_fat)
#     #     eligible_foods = filtered_fat if filtered_fat else eligible_foods

#     # if carb_pref != 'All':
#     #     filtered_carb = {food: details for food, details in eligible_foods.items() if details['MacroType'] == 'Carb'}
#     #     print("After carb preference filter:", filtered_carb)
#     #     eligible_foods = filtered_carb if filtered_carb else eligible_foods

#     # print("Final eligible foods:", eligible_foods)

#     # # Ensure there are eligible foods before continuing
#     # if not eligible_foods:
#     #     return "No eligible foods found based on the selected preferences."


#     # if protein_pref != 'All':
#     #     eligible_foods.update({food: details for food, details in food_data.items() if details['MacroType'] == 'Protein' and (protein_pref in food or protein_pref) == 'All'})
#     # if fat_pref != 'All':
#     #     eligible_foods.update({food: details for food, details in food_data.items() if details['MacroType'] == 'Fat'and (fat_pref in food or fat_pref == 'All')})
#     # if carb_pref != 'All':
#     #     eligible_foods.update({food: details for food, details in food_data.items() if details['MacroType'] == 'Carb' and (carb_pref in food or carb_pref == 'All')})

#     problem = pulp.LpProblem("Diet Optimization", pulp.LpMinimize)
#     food_vars = pulp.LpVariable.dicts("Food", eligible_foods.keys(), lowBound=0.01)

#     problem += pulp.lpSum([food_vars[food] * details['Calories'] for food, details in eligible_foods.items()])

#     # Adjusting constraints to be more realistic
#     problem += pulp.lpSum([food_vars[food] * details['Protein'] for food, details in eligible_foods.items()]) >= max(macros['Protein'], 0)
#     problem += pulp.lpSum([food_vars[food] * details['Fats'] for food, details in eligible_foods.items()]) >= max(macros['Fats'], 0)
#     problem += pulp.lpSum([food_vars[food] * details['Carbs'] for food, details in eligible_foods.items()]) >= max(macros['Carbs'], 0)

#     problem.solve()

#     if pulp.LpStatus[problem.status] == 'Optimal':
#         diet_plan = {f"Meal {meal + 1}": {} for meal in range(num_meals)}
#         for food in eligible_foods:
#             total_quantity = food_vars[food].varValue
#             if total_quantity > 0:
#                 for meal in range(num_meals):
#                     diet_plan[f"Meal {meal + 1}"][food] = total_quantity / num_meals
#         return diet_plan
#     else:
#         return "Optimization Failed. Please adjust your inputs and try again."









# from flask import Flask, render_template, request
# import pulp

# app = Flask(__name__)

# # Food data dictionary
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
#     # ... [Insert your complete food data here] ...
# }

# def calculate_maintenance_calories(weight, gender):
#     if gender == 'Male':
#         return weight * 28.5
#     else:
#         return weight * 24.5

# def adjust_calories_for_goal(calories, goal, goal_amount):
#     if goal == 'Fat Loss':
#         return max(calories - (goal_amount * 7700 / 7), 1300)
#     elif goal == 'Muscle Gain':
#         return calories + (goal_amount * 7700 / 7)
#     return calories

# def calculate_macros(calories, weight):
#     protein = weight * 2  # grams of protein
#     fats = weight * 0.5   # grams of fat
#     carbs = (calories - (protein * 4 + fats * 9)) / 4  # grams of carbs
#     return {'Protein': protein, 'Fats': fats, 'Carbs': carbs}

# def generate_diet_plan(gender, weight, diet_preference, protein_pref, fat_pref, carb_pref, goal, goal_amount, num_meals):
#     maintenance_calories = calculate_maintenance_calories(weight, gender)
#     adjusted_calories = adjust_calories_for_goal(maintenance_calories, goal, goal_amount)
#     macros = calculate_macros(adjusted_calories, weight)

#     eligible_foods = {food: details for food, details in food_data.items() if details['Category'] == diet_preference}

#     if protein_pref != 'All':
#         eligible_foods = {food: details for food, details in eligible_foods.items() if details['MacroType'] == 'Protein' and protein_pref in food}
#     if fat_pref != 'All':
#         eligible_foods = {food: details for food, details in eligible_foods.items() if details['MacroType'] == 'Fat' and fat_pref in food}
#     if carb_pref != 'All':
#         eligible_foods = {food: details for food, details in eligible_foods.items() if details['MacroType'] == 'Carb' and carb_pref in food}

#     problem = pulp.LpProblem("Diet Optimization", pulp.LpMinimize)
#     food_vars = pulp.LpVariable.dicts("Food", eligible_foods.keys(), lowBound=0.01)

#     problem += pulp.lpSum([food_vars[food] * details['Calories'] for food, details in eligible_foods.items()])

#     problem += pulp.lpSum([food_vars[food] * details['Protein'] for food, details in eligible_foods.items()]) >= macros['Protein']
#     problem += pulp.lpSum([food_vars[food] * details['Fats'] for food, details in eligible_foods.items()]) >= macros['Fats']
#     problem += pulp.lpSum([food_vars[food] * details['Carbs'] for food, details in eligible_foods.items()]) >= macros['Carbs']

#     problem.solve()

#     if pulp.LpStatus[problem.status] == 'Optimal':
#         diet_plan = {f"Meal {meal + 1}": {} for meal in range(num_meals)}
#         for food in eligible_foods:
#             total_quantity = food_vars[food].varValue
#             if total_quantity > 0:
#                 for meal in range(num_meals):
#                     diet_plan[f"Meal {meal + 1}"][food] = total_quantity / num_meals
#         return diet_plan
#     else:
#         return "Optimization Failed. Please adjust your inputs and try again."

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         gender = request.form.get('gender')
#         weight = float(request.form.get('weight'))
#         diet_preference = request.form.get('diet')
#         protein_source = request.form.get('protein_source')
#         fat_source = request.form.get('fat_source')
#         carb_source = request.form.get('carb_source')
#         goal = request.form.get('goal')
#         goal_amount = float(request.form.get('goal_amount'))
#         num_meals = int(request.form.get('num_meals'))

#         diet_plan = generate_diet_plan(gender, weight, diet_preference, protein_source, fat_source, carb_source, goal, goal_amount, num_meals)
        
#         if not isinstance(diet_plan, dict):
#             diet_plan = {}  # Ensure diet_plan is always a dictionary

#         return render_template('diet_plan.html', diet_plan=diet_plan)
#     else:
#         protein_sources = [food for food, details in food_data.items() if details["MacroType"] == "Protein"]
#         fat_sources = [food for food, details in food_data.items() if details["MacroType"] == "Fat"]
#         carb_sources = [food for food, details in food_data.items() if details["MacroType"] == "Carb"]
#         return render_template('index.html', protein_sources=protein_sources, fat_sources=fat_sources, carb_sources=carb_sources)

# if __name__ == '__main__':
#     app.run(debug=True)















# from flask import Flask, render_template, request
# import pulp

# app = Flask(__name__)

# # Food data dictionary
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
#     # ... [Insert your complete food data here] ...
# }

# def calculate_maintenance_calories(weight, gender):
#     if gender == 'Male':
#         return weight * 28.5
#     else:
#         return weight * 24.5

# def adjust_calories_for_goal(calories, goal, goal_amount):
#     if goal == 'Fat Loss':
#         return max(calories - (goal_amount * 7700 / 7), 1300)
#     elif goal == 'Muscle Gain':
#         return calories + (goal_amount * 7700 / 7)
#     return calories

# def calculate_macros(calories, weight):
#     protein = weight * 2  # grams of protein
#     fats = weight * 0.5   # grams of fat
#     carbs = (calories - (protein * 4 + fats * 9)) / 4  # grams of carbs
#     return {'Protein': protein, 'Fats': fats, 'Carbs': carbs}

# def generate_diet_plan(gender, weight, diet_preference, protein_pref, fat_pref, carb_pref, goal, goal_amount, num_meals):
#     maintenance_calories = calculate_maintenance_calories(weight, gender)
#     adjusted_calories = adjust_calories_for_goal(maintenance_calories, goal, goal_amount)
#     macros = calculate_macros(adjusted_calories, weight)

#     eligible_foods = {food: details for food, details in food_data.items() if details['Category'] == diet_preference}

#     if protein_pref != 'All':
#         eligible_foods = {food: details for food, details in eligible_foods.items() if details['MacroType'] == 'Protein' and protein_pref in food}
#     if fat_pref != 'All':
#         eligible_foods = {food: details for food, details in eligible_foods.items() if details['MacroType'] == 'Fat' and fat_pref in food}
#     if carb_pref != 'All':
#         eligible_foods = {food: details for food, details in eligible_foods.items() if details['MacroType'] == 'Carb' and carb_pref in food}

#     problem = pulp.LpProblem("Diet Optimization", pulp.LpMinimize)
#     food_vars = pulp.LpVariable.dicts("Food", eligible_foods.keys(), lowBound=0.01)

#     problem += pulp.lpSum([food_vars[food] * details['Calories'] for food, details in eligible_foods.items()])

#     problem += pulp.lpSum([food_vars[food] * details['Protein'] for food, details in eligible_foods.items()]) >= macros['Protein']
#     problem += pulp.lpSum([food_vars[food] * details['Fats'] for food, details in eligible_foods.items()]) >= macros['Fats']
#     problem += pulp.lpSum([food_vars[food] * details['Carbs'] for food, details in eligible_foods.items()]) >= macros['Carbs']

#     problem.solve()

#     if pulp.LpStatus[problem.status] == 'Optimal':
#         diet_plan = {f"Meal {meal + 1}": {} for meal in range(num_meals)}
#         for food in eligible_foods:
#             total_quantity = food_vars[food].varValue
#             if total_quantity > 0:
#                 for meal in range(num_meals):
#                     diet_plan[f"Meal {meal + 1}"][food] = total_quantity / num_meals
#         return diet_plan
#     else: 
#         return "Optimization Failed. Please adjust your inputs and try again."

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         gender = request.form.get('gender')
#         weight = float(request.form.get('weight'))
#         diet_preference = request.form.get('diet')
#         protein_source = request.form.get('protein_source')
#         fat_source = request.form.get('fat_source')
#         carb_source = request.form.get('carb_source')
#         goal = request.form.get('goal')
#         goal_amount = float(request.form.get('goal_amount'))
#         num_meals = int(request.form.get('num_meals'))

#         diet_plan = generate_diet_plan(gender, weight, diet_preference, protein_source, fat_source, carb_source, goal, goal_amount, num_meals)
        
#         if isinstance(diet_plan, str):  # Check for an error message
#             return render_template('diet_plan.html', diet_plan=None, error=diet_plan)

#         return render_template('diet_plan.html', diet_plan=diet_plan)
#     else:
#         protein_sources = [food for food, details in food_data.items() if details["MacroType"] == "Protein"]
#         fat_sources = [food for food, details in food_data.items() if details["MacroType"] == "Fat"]
#         carb_sources = [food for food, details in food_data.items() if details["MacroType"] == "Carb"]
#         return render_template('index.html', protein_sources=protein_sources, fat_sources=fat_sources, carb_sources=carb_sources)

# if __name__ == '__main__':
#     app.run(debug=True)







# from flask import Flask, render_template, request
# import pulp

# app = Flask(__name__)

# # Food data dictionary
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
#     # ... [Insert your complete food data here] ...
# }

# # Function to calculate maintenance calories
# def calculate_maintenance_calories(weight, gender):
#     if gender == 'Male':
#         return weight * 28.5
#     else:
#         return weight * 24.5

# # Function to adjust calories for specific goals
# def adjust_calories_for_goal(calories, goal, goal_amount):
#     if goal == 'Fat Loss':
#         return max(calories - (goal_amount * 7700 / 7), 1300)  # Ensuring minimum 1300 calories
#     elif goal == 'Muscle Gain':
#         return calories + (goal_amount * 7700 / 7)
#     return calories

# # Function to calculate macros
# def calculate_macros(calories, weight):
#     protein = weight * 2  # Protein in grams
#     fats = weight * 0.5   # Fats in grams
#     carbs = (calories - (protein * 4 + fats * 9)) / 4  # Carbs in grams
#     return {'Protein': protein, 'Fats': fats, 'Carbs': carbs}

# # Function to generate a diet plan
# def generate_diet_plan(gender, weight, diet_preference, protein_pref, fat_pref, carb_pref, goal, goal_amount, num_meals):
#     maintenance_calories = calculate_maintenance_calories(weight, gender)
#     adjusted_calories = adjust_calories_for_goal(maintenance_calories, goal, goal_amount)
#     macros = calculate_macros(adjusted_calories, weight)

#     # Filter eligible foods based on user preferences and diet type
#     # eligible_foods = {food: details for food, details in food_data.items() if details['Category'] == diet_preference}
# #     if protein_pref != 'All':
# #         eligible_foods = {food: details for food, details in eligible_foods.items() if protein_pref in food}
# #     if fat_pref != 'All':
# #         eligible_foods = {food: details for food, details in eligible_foods.items() if fat_pref in food}
# #     if carb_pref != 'All':
# #         eligible_foods = {food: details for food, details in eligible_foods.items() if carb_pref in food}

# #     # Check if there are eligible foods
# #     if not eligible_foods:
# #         print("No eligible foods found. Please check the filters and food data.")
# #         return {}

#     eligible_foods = {food: details for food, details in food_data.items() if details['Category'] == diet_preference}
#     # ... additional logic to further filter based on protein, fat, and carb preferences ...

#     problem = pulp.LpProblem("Diet Optimization", pulp.LpMinimize)
#     food_vars = pulp.LpVariable.dicts("Food", eligible_foods.keys(), lowBound=0.01)

#     # Objective function: Minimize total calorie deviation
#     problem += pulp.lpSum([food_vars[food] * details['Calories'] for food, details in eligible_foods.items()])

#     # Macro constraints
#     problem += pulp.lpSum([food_vars[food] * details['Protein'] for food, details in eligible_foods.items()]) >= macros['Protein']
#     problem += pulp.lpSum([food_vars[food] * details['Fats'] for food, details in eligible_foods.items()]) >= macros['Fats']
#     problem += pulp.lpSum([food_vars[food] * details['Carbs'] for food, details in eligible_foods.items()]) >= macros['Carbs']

#     # Solve the problem
#     problem.solve()

#     # Check if the problem has a feasible solution
#     if pulp.LpStatus[problem.status] == 'Optimal':
#         # Generate the diet plan
#         diet_plan = {f"Meal {meal + 1}": {} for meal in range(num_meals)}
#         for food in eligible_foods:
#             total_quantity = food_vars[food].varValue
#             if total_quantity > 0:
#                 for meal in range(num_meals):
#                     diet_plan[f"Meal {meal + 1}"][food] = total_quantity / num_meals
#         return diet_plan
#     else:
#         return "Optimization Failed. Please adjust your inputs and try again."

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         gender = request.form.get('gender')
#         weight = float(request.form.get('weight'))
#         diet_preference = request.form.get('diet')
#         protein_source = request.form.get('protein_source')
#         fat_source = request.form.get('fat_source')
#         carb_source = request.form.get('carb_source')
#         goal = request.form.get('goal')
#         goal_amount = float(request.form.get('goal_amount'))
#         num_meals = int(request.form.get('num_meals'))

#         diet_plan = generate_diet_plan(gender, weight, diet_preference, protein_source, fat_source, carb_source, goal, goal_amount, num_meals)
        
#         if isinstance(diet_plan, str):  # If an error message is returned
#             return render_template('diet_plan.html', diet_plan=None, error=diet_plan)

#         return render_template('diet_plan.html', diet_plan=diet_plan)
#     else:
#         return render_template('index.html')

# if __name__ == '__main__':
#     app.run(debug=True)














# from flask import Flask, render_template, request
# import pulp

# app = Flask(__name__)

# # Structured food data with categories, macro types, and macro content
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
#     # ... (Insert your structured food data here)
# }

# # @app.route('/', methods=['GET', 'POST'])
# # def index():
# #     if request.method == 'POST':
# #         gender = request.form.get('gender')
# #         weight = float(request.form.get('weight'))
# #         diet_preference = request.form.get('diet')
# #         protein_source = request.form.get('protein_source')
# #         fat_source = request.form.get('fat_source')
# #         carb_source = request.form.get('carb_source')
# #         goal = request.form.get('goal')
# #         goal_amount = float(request.form.get('goal_amount'))
# #         num_meals = int(request.form.get('num_meals'))

# #         diet_plan = generate_diet_plan(gender, weight, diet_preference, protein_source, fat_source, carb_source, goal, goal_amount, num_meals)

# #         if not diet_plan or isinstance(diet_plan, str):
# #             # If there is an error or diet_plan is empty, pass an error message to the template
# #             return render_template('diet_plan.html', diet_plan=None, error="An error occurred or no diet plan could be generated.")
        
# #         # Render the diet plan
# #         return render_template('diet_plan.html', diet_plan=diet_plan)
# #     else:
# #         protein_sources = [food for food, details in food_data.items() if details["MacroType"] == "Protein"]
# #         fat_sources = [food for food, details in food_data.items() if details["MacroType"] == "Fat"]
# #         carb_sources = [food for food, details in food_data.items() if details["MacroType"] == "Carb"]
# #         # Render the index page with the form
# #         return render_template('index.html', protein_sources=protein_sources, fat_sources=fat_sources, carb_sources=carb_sources)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         gender = request.form.get('gender')
#         weight = float(request.form.get('weight'))
#         diet_preference = request.form.get('diet')
#         protein_source = request.form.get('protein_source')
#         fat_source = request.form.get('fat_source')
#         carb_source = request.form.get('carb_source')
#         goal = request.form.get('goal')
#         goal_amount = float(request.form.get('goal_amount'))
#         num_meals = int(request.form.get('num_meals'))

#         diet_plan = generate_diet_plan(gender, weight, diet_preference, protein_source, fat_source, carb_source, goal, goal_amount, num_meals)
#         return render_template('diet_plan.html', diet_plan=diet_plan)
#     else:
#         protein_sources = [food for food, details in food_data.items() if details["MacroType"] == "Protein"]
#         fat_sources = [food for food, details in food_data.items() if details["MacroType"] == "Fat"]
#         carb_sources = [food for food, details in food_data.items() if details["MacroType"] == "Carb"]
#         return render_template('index.html', protein_sources=protein_sources, fat_sources=fat_sources, carb_sources=carb_sources)

# def calculate_maintenance_calories(weight, gender):
#     if gender == 'Male':
#         return weight * 24
#     else:
#         return weight * 22

# def adjust_calories_for_goal(calories, goal, goal_amount):
#     if goal == 'Fat Loss':
#         return calories - (goal_amount * 1000 / 7)
#     elif goal == 'Muscle Gain':
#         return calories + (goal_amount * 500 / 7)
#     return calories

# def calculate_macros(calories):
#     return {
#         'Protein': calories * 0.30 / 4,
#         'Fats': calories * 0.25 / 9,
#         'Carbs': calories * 0.45 / 4
#     }

# def generate_diet_plan(gender, weight, diet_preference, protein_pref, fat_pref, carb_pref, goal, goal_amount, num_meals):
#     maintenance_calories = calculate_maintenance_calories(weight, gender)
#     adjusted_calories = adjust_calories_for_goal(maintenance_calories, goal, goal_amount)
#     daily_macros = calculate_macros(adjusted_calories)

#     # Print the total daily macros needed
#     print("Total daily macros needed:", daily_macros)

#     eligible_foods = {food: details for food, details in food_data.items() if details['Category'] == diet_preference}
#     if protein_pref != 'All':
#         eligible_foods = {food: details for food, details in eligible_foods.items() if protein_pref in food}
#     if fat_pref != 'All':
#         eligible_foods = {food: details for food, details in eligible_foods.items() if fat_pref in food}
#     if carb_pref != 'All':
#         eligible_foods = {food: details for food, details in eligible_foods.items() if carb_pref in food}

#     # Check if there are eligible foods
#     if not eligible_foods:
#         print("No eligible foods found. Please check the filters and food data.")
#         return {}

#     problem = pulp.LpProblem("Diet Optimization", pulp.LpMinimize)

#     # Create variables for the food items with a small positive lower bound
#     food_vars = pulp.LpVariable.dicts("Food", eligible_foods.keys(), lowBound=0.01)

#     # Objective function: Minimize the deviation from the target calories
#     problem += pulp.lpSum([food_vars[food] * details['Calories'] for food, details in eligible_foods.items()])

#     # Constraints for total macros needed for the entire day
#     for macro in ['Protein', 'Fats', 'Carbs']:
#         problem += pulp.lpSum([food_vars[food] * details[macro] for food, details in eligible_foods.items()]) == daily_macros[macro], f"Total{macro}"

#     # Solve the problem
#     problem.solve()

#     print("Problem Status:", pulp.LpStatus[problem.status])

#     # If the problem has an optimal solution
#     if pulp.LpStatus[problem.status] == 'Optimal':
#         # Create a dictionary to hold the diet plan
#         diet_plan = {f"Meal {meal+1}": {} for meal in range(num_meals)}
#         for food in eligible_foods:
#             total_quantity = food_vars[food].varValue
#             if total_quantity and total_quantity > 0:
#                 # Distribute the total quantity across the number of meals
#                 for meal in range(num_meals):
#                     diet_plan[f"Meal {meal+1}"][food] = total_quantity / num_meals
        
#         # Print the diet plan
#         print("Generated Diet Plan:", diet_plan)
#         return diet_plan
#     else:
#         print("Optimization Failed. Please adjust your inputs and try again.")
#         return {}


# # def generate_diet_plan(gender, weight, diet_preference, protein_pref, fat_pref, carb_pref, goal, goal_amount, num_meals):
# #     maintenance_calories = calculate_maintenance_calories(weight, gender)
# #     adjusted_calories = adjust_calories_for_goal(maintenance_calories, goal, goal_amount)
# #     macros = calculate_macros(adjusted_calories)
    
# #     print("Macros needed per meal:", macros)

# #     eligible_foods = {food: details for food, details in food_data.items() if details['Category'] == diet_preference}
# #     if protein_pref != 'All':
# #         eligible_foods = {food: details for food, details in eligible_foods.items() if protein_pref in food}
# #     if fat_pref != 'All':
# #         eligible_foods = {food: details for food, details in eligible_foods.items() if fat_pref in food}
# #     if carb_pref != 'All':
# #         eligible_foods = {food: details for food, details in eligible_foods.items() if carb_pref in food}

# #     print("Eligible foods after filtering:", eligible_foods)

# #     problem = pulp.LpProblem("Diet Optimization", pulp.LpMinimize)

# #     food_vars = pulp.LpVariable.dicts("Food", eligible_foods.keys(), lowBound=0.01)

# #     problem += pulp.lpSum([food_vars[food] * details['Calories'] for food, details in eligible_foods.items()])

# #     for macro in ['Protein', 'Fats', 'Carbs']:
# #         problem += pulp.lpSum([food_vars[food] * details[macro] for food, details in eligible_foods.items()]) >= macros[macro] / num_meals, f"Total{macro}"

# #     problem.solve()

# #     print("Problem Status:", pulp.LpStatus[problem.status])

# #     if pulp.LpStatus[problem.status] == 'Optimal':
# #         diet_plan = {f"Meal {meal+1}": {} for meal in range(num_meals)}
# #         for food in eligible_foods:
# #             total_quantity = food_vars[food].varValue
# #             if total_quantity and total_quantity > 0:
# #                 for meal in range(num_meals):
# #                     diet_plan[f"Meal {meal+1}"][food] = total_quantity / num_meals
        
# #         # Debugging prints for total macros
# #         print("Total macros from food_vars:")
# #         total_protein = sum(food_vars[food].varValue * details['Protein'] for food, details in eligible_foods.items())
# #         total_fats = sum(food_vars[food].varValue * details['Fats'] for food, details in eligible_foods.items())
# #         total_carbs = sum(food_vars[food].varValue * details['Carbs'] for food, details in eligible_foods.items())
# #         print(f"Protein: {total_protein}, Fats: {total_fats}, Carbs: {total_carbs}")

# #         print("Generated Diet Plan:", diet_plan)
# #         return diet_plan
# #     else:
# #         print("Optimization Failed. Please adjust your inputs and try again.")
# #         return {}


# # def generate_diet_plan(gender, weight, diet_preference, protein_pref, fat_pref, carb_pref, goal, goal_amount, num_meals):
# #     # Calculate maintenance calories based on gender and weight
# #     maintenance_calories = calculate_maintenance_calories(weight, gender)

# #     # Adjust calories based on the user's fitness goal
# #     adjusted_calories = adjust_calories_for_goal(maintenance_calories, goal, goal_amount)

# #     # Calculate macros
# #     macros = calculate_macros(adjusted_calories)

# #     # Filter eligible foods based on user preferences and diet type
# #     eligible_foods = {food: details for food, details in food_data.items() if details['Category'] == diet_preference}
# #     if protein_pref != 'All':
# #         eligible_foods = {food: details for food, details in eligible_foods.items() if details['MacroType'] == 'Protein' and protein_pref in food}
# #     if fat_pref != 'All':
# #         eligible_foods = {food: details for food, details in eligible_foods.items() if details['MacroType'] == 'Fat' and fat_pref in food}
# #     if carb_pref != 'All':
# #         eligible_foods = {food: details for food, details in eligible_foods.items() if details['MacroType'] == 'Carb' and carb_pref in food}

# #     # Set up the linear programming problem
# #     problem = pulp.LpProblem("Diet Optimization", pulp.LpMinimize)

# #     # Create a variable for each food item
# #     food_vars = pulp.LpVariable.dicts("Food", eligible_foods.keys(), lowBound=0)

# #     # Objective function: Minimize total calorie deviation
# #     problem += pulp.lpSum([food_vars[food] * details['Calories'] for food, details in eligible_foods.items()])

# #     # Macro constraints for each meal
# #     for macro in ['Protein', 'Fats', 'Carbs']:
# #         problem += pulp.lpSum([food_vars[food] * details[macro] for food, details in eligible_foods.items()]) >= macros[macro] * num_meals, f"Total{macro}"

# #     # Solve the problem
# #     problem.solve()

# #     # Debugging prints
# #     print("Problem Status:", pulp.LpStatus[problem.status])
# #     for food in eligible_foods:
# #         print(food, food_vars[food].varValue)

# #     # Check if the problem has a feasible solution
# #     if pulp.LpStatus[problem.status] == 'Optimal':
# #         # Generate the diet plan
# #         diet_plan = {f"Meal {meal+1}": {} for meal in range(num_meals)}
# #         for food in eligible_foods:
# #             total_quantity = food_vars[food].varValue
# #             if total_quantity and total_quantity > 0:
# #                 for meal in range(num_meals):
# #                     diet_plan[f"Meal {meal+1}"][food] = total_quantity / num_meals
# #         print("Generated Diet Plan:", diet_plan)  # Debugging print
# #         return diet_plan
# #     else:
# #         print("Optimization Failed. Please adjust your inputs and try again.")
# #         return {}


# # def generate_diet_plan(gender, weight, diet_preference, protein_pref, fat_pref, carb_pref, goal, goal_amount, num_meals):
# #     # Calculate maintenance calories based on gender and weight
# #     maintenance_calories = calculate_maintenance_calories(weight, gender)

# #     # Adjust calories based on the user's fitness goal
# #     adjusted_calories = adjust_calories_for_goal(maintenance_calories, goal, goal_amount)

# #     # Calculate macros
# #     macros = calculate_macros(adjusted_calories)

# #     # Filter eligible foods based on user preferences and diet type
# #     eligible_foods = {food: details for food, details in food_data.items() if details['Category'] == diet_preference}
# #     if protein_pref != 'All':
# #         eligible_foods = {food: details for food, details in eligible_foods.items() if details['MacroType'] == 'Protein' and protein_pref in food}
# #     if fat_pref != 'All':
# #         eligible_foods = {food: details for food, details in eligible_foods.items() if details['MacroType'] == 'Fat' and fat_pref in food}
# #     if carb_pref != 'All':
# #         eligible_foods = {food: details for food, details in eligible_foods.items() if details['MacroType'] == 'Carb' and carb_pref in food}

# #     # Set up the linear programming problem
# #     problem = pulp.LpProblem("Diet Optimization", pulp.LpMinimize)

# #     # Create a variable for each food item
# #     food_vars = pulp.LpVariable.dicts("Food", eligible_foods.keys(), lowBound=0)

# #     # Objective function: Minimize total calorie deviation
# #     problem += pulp.lpSum([food_vars[food] * details['Calories'] for food, details in eligible_foods.items()])

# #     # Macro constraints for each meal
# #     for macro in ['Protein', 'Fats', 'Carbs']:
# #         problem += pulp.lpSum([food_vars[food] * details[macro] for food, details in eligible_foods.items()]) >= macros[macro] * num_meals, f"Total{macro}"

# #     # Solve the problem
# #     problem.solve()

# #     # Check if the problem has a feasible solution
# #     if pulp.LpStatus[problem.status] == 'Optimal':
# #         # Generate the diet plan
# #         diet_plan = {f"Meal {meal+1}": {} for meal in range(num_meals)}
# #         for food in eligible_foods:
# #             total_quantity = food_vars[food].varValue
# #             if total_quantity and total_quantity > 0:
# #                 for meal in range(num_meals):
# #                     diet_plan[f"Meal {meal+1}"][food] = total_quantity / num_meals
# #         return diet_plan
# #     else:
# #         return "Optimization Failed. Please adjust your inputs and try again."

# if __name__ == '__main__':
#     app.run(debug=True)



















# from flask import Flask, render_template, request
# import pulp
# from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus


# app = Flask(__name__)

# # Structured food data
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
#     # ... (Insert your complete structured food data here)
# }

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         gender = request.form.get('gender', 'Female')
#         weight = float(request.form.get('weight', 0))
#         diet_preference = request.form.get('diet', 'Vegetarian')
#         protein_source = request.form.get('protein_source', 'All')
#         fat_source = request.form.get('fat_source', 'All')
#         carb_source = request.form.get('carb_source', 'All')
#         goal = request.form.get('goal')
#         goal_amount = float(request.form.get('goal_amount', 0))
#         num_meals = int(request.form.get('num_meals', 3))

#         maintenance_calories = calculate_maintenance_calories(weight, gender)
#         adjusted_calories = adjust_calories_for_goal(maintenance_calories, goal, goal_amount)
#         macros = calculate_macros(adjusted_calories)

#         diet_plan = optimize_diet_plan(macros, diet_preference, protein_source, fat_source, carb_source, num_meals)
#         return render_template('diet_plan.html', diet_plan=diet_plan, goal=goal, goal_amount=goal_amount)

#     protein_sources = [food for food, details in food_data.items() if details["MacroType"] == "Protein"]
#     fat_sources = [food for food, details in food_data.items() if details["MacroType"] == "Fat"]
#     carb_sources = [food for food, details in food_data.items() if details["MacroType"] == "Carb"]

#     return render_template('index.html', protein_sources=protein_sources, fat_sources=fat_sources, carb_sources=carb_sources)

# def calculate_maintenance_calories(weight, gender):
#     # Calculation based on gender and weight
#     # Example: weight * 28.5 for male and weight * 24.5 for female
#     return weight * 28.5 if gender == 'Male' else weight * 24.5

# def adjust_calories_for_goal(calories, goal, amount):
#     # Adjust calories based on goal (Fat Loss or Muscle Gain)
#     if goal == "Fat Loss":
#         deficit = 7700 * amount / 1000 / 7  # Calorie deficit for fat loss
#         return max(calories - deficit, 1200)  # Ensure not going below a minimum threshold
#     elif goal == "Muscle Gain":
#         surplus = 110 * amount / 1000 / 7  # Calorie surplus for muscle gain
#         return calories + surplus
#     return calories

# def calculate_macros(calories):
#     # Example macro ratios: 40% carbs, 30% protein, 30% fats
#     protein_calories = calories * 0.3
#     fat_calories = calories * 0.3
#     carb_calories = calories * 0.4
#     return {"Protein": protein_calories / 4, "Fats": fat_calories / 9, "Carbohydrates": carb_calories / 4}


# def optimize_diet_plan(macros, diet_preference, protein_source, fat_source, carb_source, num_meals):
#     # Filter foods based on diet preference
#     filtered_foods = {food: details for food, details in food_data.items() if details['Category'] == diet_preference}
    
#     # Create a new problem with pulp
#     prob = LpProblem("DietPlanOptimization", LpMinimize)

#     # Create a dictionary of pulp variables with lower bound of zero
#     food_vars = LpVariable.dicts("Food", filtered_foods, lowBound=0)

#     # Set the objective: Minimize the total deviation from macro goals
#     prob += lpSum([food_vars[food] * (details['Protein'] * 4 + details['Fats'] * 9 + details['Carbs'] * 4)
#                    for food, details in filtered_foods.items()])

#     # Add constraints for each macro nutrient based on user preferences
#     if protein_source != 'All':
#         prob += lpSum([food_vars[food] * details['Protein'] for food, details in filtered_foods.items() if details['MacroType'] == 'Protein']) >= macros['Protein']
    
#     if fat_source != 'All':
#         prob += lpSum([food_vars[food] * details['Fats'] for food, details in filtered_foods.items() if details['MacroType'] == 'Fat']) >= macros['Fats']
    
#     if carb_source != 'All':
#         prob += lpSum([food_vars[food] * details['Carbs'] for food, details in filtered_foods.items() if details['MacroType'] == 'Carb']) >= macros['Carbohydrates']

#     # Solve the problem
#     prob.solve()
    
#     # Check if the optimization was successful
#     if LpStatus[prob.status] == 'Optimal':
#         # Create the diet plan based on the optimized variables
#         diet_plan = {f"Meal {meal}": {} for meal in range(1, num_meals + 1)}
#         for food, details in filtered_foods.items():
#             # Divide the quantity of each food by the number of meals
#             quantity = food_vars[food].varValue / num_meals if food_vars[food].varValue else 0
#             for meal in range(1, num_meals + 1):
#                 if quantity > 0:
#                     diet_plan[f"Meal {meal}"][food] = quantity
#         return diet_plan
#     else:
#         return "Optimization Failed"



# # import pulp

# # def optimize_diet_plan(macros, diet_preference, protein_source, fat_source, carb_source, num_meals):
# #     # Filter food items based on user preferences
# #     filtered_food_data = {food: details for food, details in food_data.items()
# #                           if details["Category"] == diet_preference and
# #                           (protein_source in food or protein_source == "All") and
# #                           (fat_source in food or fat_source == "All") and
# #                           (carb_source in food or carb_source == "All")}

# #     # Convert total daily macros to per meal macros
# #     macros_per_meal = {key: value / num_meals for key, value in macros.items()}

# #     # Create a linear programming problem
# #     problem = pulp.LpProblem("Diet Optimization", pulp.LpMinimize)

# #     # Create a variable for each food item in each meal
# #     food_vars = {(food, meal): pulp.LpVariable(f"{food}_Meal{meal}", lowBound=0) 
# #                  for food in filtered_food_data for meal in range(1, num_meals + 1)}

# #     # Objective function: Minimize total calories deviation across all meals
# #     problem += pulp.lpSum([filtered_food_data[food]["Calories"] * food_vars[food, meal] 
# #                            for food in filtered_food_data for meal in range(1, num_meals + 1)])

# #     # Constraints for meeting macro targets for each meal
# #     for meal in range(1, num_meals + 1):
# #         problem += pulp.lpSum([filtered_food_data[food]["Protein"] * food_vars[food, meal] 
# #                                for food in filtered_food_data]) >= macros_per_meal["Protein"]
# #         problem += pulp.lpSum([filtered_food_data[food]["Fats"] * food_vars[food, meal] 
# #                                for food in filtered_food_data]) >= macros_per_meal["Fats"]
# #         problem += pulp.lpSum([filtered_food_data[food]["Carbs"] * food_vars[food, meal] 
# #                                for food in filtered_food_data]) >= macros_per_meal["Carbohydrates"]

# #     # Solve the problem
# #     problem.solve()

# #     # Generate the diet plan based on the solution
# #     # Generate the diet plan based on the solution
# #     diet_plan = {f"Meal {meal}": {} for meal in range(1, num_meals + 1)}
# #     for food, meal in food_vars:
# #         if pulp.value(food_vars[(food, meal)]) > 0:
# #             diet_plan[f"Meal {meal}"][food] = pulp.value(food_vars[(food, meal)])

# #     # diet_plan = {meal: {} for meal in range(1, num_meals + 1)}
# #     # for food, meal in food_vars:
# #     #     if pulp.value(food_vars[(food, meal)]) > 0:
# #     #         diet_plan[meal][food] = pulp.value(food_vars[(food, meal)])

# #     return diet_plan

# if __name__ == '__main__':
#     app.run(debug=True)




