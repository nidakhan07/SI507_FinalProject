#
# Name: Nida Khan
# uniqname: nidamk

import requests
import json
import pandas as pd


api_key = '9abd24d47a9c4fcb8a030425d29a2ac9'
url1 = 'https://api.spoonacular.com/recipes/findByIngredients'
url2 = 'https://api.spoonacular.com/recipes/{id}/information'

cache_filename = "cache.csv"

# params = {'ingredients' : ['flour', 'eggs', 'milk', 'chocolate', 'baking powder'], 'number': 10, 'ignorePantry': True}

# ingred_output = requests.get(url1 + f'?apiKey={api_key}', params=params).json()
# id = [i['id'] for i in ingred_output]

# url2 = f'https://api.spoonacular.com/recipes/{id[0]}/information'

# api_result = requests.get(url2 + f'?apiKey={api_key}').json()
# recipe_df = pd.DataFrame()
# recipe_df['vegetarian'] = [api_result['vegetarian']]
# recipe_df['glutenFree'] = [api_result['glutenFree']]
# recipe_df['pricePerServing'] = [api_result['pricePerServing']]
# recipe_df['title'] = [api_result['title']]

# print(recipe_df)

def getcachedata(cache_filename):
    try:
        cache_df = pd.read_csv(cache_filename)
    except:
        cache_df = pd.DataFrame()
    return cache_df

def write_to_cache(cache_df, results_df):
    cache_df = pd.concat([cache_df, results_df]).drop_duplicates()
    cache_df.to_csv(cache_filename, index=False)

def call_api(ingredients):
    params = {'ingredients' : ingredients, 'number': 50, 'ignorePantry': True, 'cheap': True}
    ingred_output = requests.get(url1 + f'?apiKey={api_key}', params=params).json()
    id = [i['id'] for i in ingred_output]
    attribute_list = ['title', 'pricePerServing', 'glutenFree', 'vegetarian', 'dishTypes', 'readyInMinutes', 'sourceUrl']
    recipe_info = {i: [] for i in attribute_list}
    for i in id:
        url = f'https://api.spoonacular.com/recipes/{i}/information'
        api_result = requests.get(url + f'?apiKey={api_key}').json()
        for a in attribute_list:
            recipe_info[a].append(api_result[a])
    return pd.DataFrame(recipe_info)


def getrecipedata(ingredients, cache_df): #takes in a list of ingredients, and pulls information for attributes from attribute list for each recipe corresponding to those ingredients.
    if len(cache_df) > 0:
        matched_rows = cache_df[cache_df['ingredients']==ingredients]
        if len(matched_rows) > 0:
            return matched_rows
        else:
            results_df = call_api(ingredients)
    else:
        results_df = call_api(ingredients)
    return results_df


def ingred_input():
    testprompt = input("Enter a minimum of 5 ingredients that you want to use to create a dish, each separated by a comma: ").split(",")
    while True:
        if len(testprompt) >= 5:
            break
        else:
            testprompt = input("Please enter a minimum of 5 valid ingredients: ").split(",")
            continue
    return testprompt

prompt = ingred_input()
print(getrecipedata(prompt)['glutenFree'].value_counts())







# min_ingredients = input("Enter a few ingredients that you want to use to create a dish, each separated by a comma").split(",")
# print(min_ingredients)




