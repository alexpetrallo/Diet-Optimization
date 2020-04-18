import pandas as pd
import pulp as p
import numpy as np

excel_file = 'usda_2016_food_facts.xls'
# excel_file = 'nutrition2.xls'

df = pd.read_excel(excel_file)
df = df.fillna(0)



foodies = (df['Food Name'])
types = df['Food Group']
# foodies = (df.iloc[:,2])


food_items = []
typeList = []
for t in types:
    typeList.append(t)
for food in foodies:
    food_items.append(food)


food_items = list(set(food_items))

meatList = ['Lamb, Veal, and Game Products', 'Finfish and Shellfish Products', 'Beef Products', 'Pork Products', 'Sausages and Luncheon Meats', 'Poultry Products']
snackSweetList = ['Sweets','Snacks']

#make dict for each of the nutrient facts
calories = dict(zip(food_items, df['Calories']))
fat = dict(zip(food_items, df['Fat (g)']))
carbs = dict(zip(food_items, df['Carbohydrates (g)']))
proteins = dict(zip(food_items, df['Protein (g)']))
ca = dict(zip(food_items, df['Calcium (mg)']))
fe = dict(zip(food_items, df['Iron (mg)']))
# weights = dict(zip(food_items, df['Weight [g]']))

foodType = dict(zip(food_items, df['Food Group']))
# local = dict(zip(food_items, df['LOCAL']))
# prepTime = dict(zip(food_items, df['PREP TIME']))

#create list of params for quanitites of each food
food_vars = p.LpVariable.dicts("Food", food_items,lowBound=0,upBound=2,cat='Continuous')


calList = list(calories.values())
foodList = list(food_vars.values())


#create the problem (depending on what you want to optim)
# prob = p.LpProblem("Nutrient-Optimization", p.LpMaximize)
prob = p.LpProblem("Nutrient-Optimization", p.LpMinimize)

#pick one of these for differnt things to optimize
#min calories
# prob += p.lpSum([calList[i]*foodList[i] for i in range(len(food_items))])

#maximize veggies
# prob += p.lpSum([(1 if foodType[f] == 'VEGETABLES AND LEGUMES' else 0) * food_vars[f] for f in food_items])


#for maximize local
# prob += p.lpSum([(1 if local[f] == 'yes' else 0) * food_vars[f] for f in food_items])

#for min prep
# prob += p.lpSum([prepTime[i]*food_vars[i] for i in food_items])

#for min fat
prob += p.lpSum([fat[f] * food_vars[f] for f in food_items])




###for at least 2000 cals
prob += p.lpSum([calories[i]*food_vars[i] for i in food_items]) >= 2000
prob += p.lpSum([calories[i]*food_vars[i] for i in food_items]) <= 2500

#####

#daily nutrition requirements
prob += p.lpSum([fat[f] * food_vars[f] for f in food_items]) >= 70.0
prob += p.lpSum([fat[f] * food_vars[f] for f in food_items]) <= 80.0

prob += p.lpSum([carbs[f] * food_vars[f] for f in food_items]) >= 305.0
prob += p.lpSum([carbs[f] * food_vars[f] for f in food_items]) <= 315.0

prob += p.lpSum([proteins[f] * food_vars[f] for f in food_items]) >= 45.0
prob += p.lpSum([proteins[f] * food_vars[f] for f in food_items]) <= 60.0

prob += p.lpSum([ca[f] * food_vars[f] for f in food_items]) >= 1000.0
prob += p.lpSum([ca[f] * food_vars[f] for f in food_items]) >= 110.0

prob += p.lpSum([fe[f] * food_vars[f] for f in food_items]) >= 18.0
prob += p.lpSum([fe[f] * food_vars[f] for f in food_items]) <= 20.0




prob += p.lpSum([(1 if foodType[f] == 'Vegetables and Vegetable Products' else 0) * food_vars[f] for f in food_items]) >=3
prob += p.lpSum([(1 if foodType[f] == 'Fruits and Fruit Juices' else 0) * food_vars[f] for f in food_items]) >=2
prob += p.lpSum([(1 if foodType[f] in meatList else 0) * food_vars[f] for f in food_items]) >=2
prob += p.lpSum([(1 if foodType[f] in snackSweetList else 0) * food_vars[f] for f in food_items]) >=1
prob += p.lpSum([(1 if foodType[f] in snackSweetList else 0) * food_vars[f] for f in food_items]) <=2

# prob += p.lpSum(sum(value == 'VEGETABLES AND LEGUMES' for value in foodType.values())) >= 10



# prob += p.lpSum([weights[f] * food_vars[f] for f in food_items]) >= 1500
# prob += p.lpSum([weights[f] * food_vars[f] for f in food_items]) <= 2500
# p.LpSolverDefault.msg = 1
prob.solve()

print("Status:", p.LpStatus[prob.status])

calCount = []
for v in prob.variables():
    try:
        if v.varValue>0:
            print(v.name, "=", v.varValue)
            # print(v)
            calCount = np.append(calCount, v.varValue * calList(v))
    except:
        pass
print('the total amount of calories is', prob.objective.value())



ret = sum(calCount)
print(calCount)

typeList = list(dict.fromkeys(typeList))
print(typeList)