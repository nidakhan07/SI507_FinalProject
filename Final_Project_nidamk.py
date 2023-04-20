
# Name: Nida Khan
# uniqname: nidamk

import requests
import json
import pandas as pd
import re 
# from googlesearch import search



# try:
#     from googlesearch import search
# except ImportError:
#     print("No module named 'google' found")
# query = "Pizza Recipe"
# for j in search(query):
#     print(j)




# for i in search("Pizza Recipe",advanced=True, num_results=5):
#     print(i)


# import GoogleSearchResults
# query = GoogleSearchResults({"q": "coffee"})
# json_results = query.get_json()


api_key = '9abd24d47a9c4fcb8a030425d29a2ac9'
url1 = 'https://api.spoonacular.com/recipes/findByIngredients'
url2 = 'https://api.spoonacular.com/recipes/{id}/information'

url3 = "https://api.edamam.com/api/recipes/v2"


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
    '''
    If cache data exists, this function takes data from the cache_filename.

    Parameters
    ----------
    cache_filename

    '''
    try:
        cache_df = pd.read_csv(cache_filename)
        cache_df = cache_df.drop_duplicates(ignore_index=True)
    except:
        cache_df = pd.DataFrame()
    return cache_df



def write_to_cache(cache_df, results_df):
    '''
    This function concatenates the existing cache and new results and writes to cache to create an updated csv.

    Parameters
    ----------
    cache_df
    results_df
    '''
    cache_df = pd.concat([cache_df, results_df])
    cache_df.to_csv(cache_filename, index=False)

def call_api(ingredients):
    '''
    Function to call api (spoonacular) and fetch attributes for recipes matching the ingredient list.

    Parameters
    ----------
    ingredient list
    
    '''
    params = {'ingredients' : ingredients, 'number': 50, 'ignorePantry': True, 'cheap': True}
    ingred_output = requests.get(url1 + f'?apiKey={api_key}', params=params).json()
    id = [i['id'] for i in ingred_output]
    attribute_list = ['title', 'pricePerServing', 'glutenFree', 'vegetarian', 'vegan', 'dishTypes', 'readyInMinutes', 'sourceUrl']
    recipe_info = {i: [] for i in attribute_list}
    for i in id:
        url = f'https://api.spoonacular.com/recipes/{i}/information'
        api_result = requests.get(url + f'?apiKey={api_key}').json()
        for a in attribute_list:
            recipe_info[a].append(api_result[a])
    recipe_df  = pd.DataFrame(recipe_info)
    recipe_df["ingredients"]=[set(ingredients)]*len(recipe_df) #used set so order does not have to match, and takes unique values of the list.
    return recipe_df

def get_additionalrecipe(recipe_title):
    '''
    Additional api (Edamam) for more recipe options for the user. This function uses the recipe title to pull results rather than ingredients.

    Parameters
    ----------
    recipe_title: string
    '''
    params = {'type':'public','q': recipe_title, 'app_id': 'f43a1c59', 'app_key': 'e871a36d93f1795ee5c7f1d0422bdb04'}
    additional_output = requests.get(url3, params=params).json()
    url_list = []
    for i in additional_output['hits']:
        url_list.append(i['recipe']['url'])
    return url_list

def getrecipedata(ingredients, cache_df): 
    '''
    takes in a list of ingredients, and pulls information for attributes from attribute list for each recipe 
    corresponding to those ingredients.
    
    Parameters
    ----------
    ingredients: list
    cache_df: dataframe
    '''

    if len(cache_df) > 0:
        cache_df['ingredients'] = [set(re.sub("[\{\}' ]*","",i).split(',')) for i in cache_df['ingredients']]
        matched_rows = cache_df[cache_df['ingredients']==set(ingredients)]
        if len(matched_rows) > 0:
            return matched_rows
        else:
            results_df = call_api(ingredients)
    else:
        results_df = call_api(ingredients)
    return results_df


def ingred_input():
    '''
    Function to prompt user to enter 5 minimum ingredients and create a list of those ingredients.
    '''
    testprompt = input("Enter a minimum of 5 ingredients that you want to use to create a dish, each separated by a comma: ").split(",")
    testprompt = [i.strip() for i in testprompt]
    while True:
        if len(testprompt) >= 5:
            break
        else:
            testprompt = input("Please enter a minimum of 5 valid ingredients: ").split(",")
            testprompt = [i.strip() for i in testprompt]
            continue
    return testprompt



# print(get_additionalrecipe('no oven peanut butter square'))

# google_apikey = 

# def call_google_api(ingredients):
#     q = ingredients

#     url = f"https://www.googleapis.com/customsearch/v1?{parameters}"


# min_ingredients = input("Enter a few ingredients that you want to use to create a dish, each separated by a comma").split(",")
# print(min_ingredients)

# testcache = getcachedata(cache_filename)
# testcache['ingredients'] = [set(re.sub("[\{\}' ]*","",i).split(',')) for i in testcache['ingredients']]
# print(testcache)
# ingredients = ['ginger', 'garlic', 'potato', 'onion', 'tomato']
# matched_rows = testcache[testcache['ingredients']==set(ingredients)]
# print(matched_rows)
# print(set(ingredients))
# print(testcache['ingredients'][0])
# print(type(testcache['ingredients'][0]))
# set(re.sub("[\{\}']*","",testcache['ingredients'][0]).split(','))

def main():
    prompt = ingred_input()
    recipe_cache = getcachedata(cache_filename)
    results_df = getrecipedata(prompt, cache_df=recipe_cache)
    write_to_cache(recipe_cache, results_df)

    # results_df["ingredients"] = [set(i) for i in results_df["ingredients"]]
    # print(results_df)
    # cache_df = pd.concat([recipe_cache, results_df])
    # print(cache_df)

    dish_type = input('Do you want something sweet or savory ').strip()

    if dish_type == "sweet":
        sweet_results = results_df[results_df['dishTypes'].str.contains('desserts', regex=False)]
        gluten = input('Does the dish need to be Gluten Free?')
        if gluten == "Yes" or gluten == "yes":
            sweet_results = sweet_results[sweet_results['glutenFree']==True]
        final_results = sweet_results

    elif dish_type == 'savory':
        savory_results = results_df[~results_df['dishTypes'].str.contains('desserts', regex=False)]
        vegetarian = input('Does the dish need to be Vegetarian? ')
        if vegetarian == "Yes" or vegetarian == "yes":
            savory_results = savory_results[savory_results['vegetarian']==True]
            vegan = input("Does it need to be Vegan? ")
            if vegan == "Yes" or vegan == "yes":
                savory_results = savory_results[savory_results['vegan']==True]
        final_results = savory_results

    cheapornot = input("Do you want something cheap? ")
    if cheapornot == "Yes" or cheapornot == "yes":
        final_results = final_results.sort_values(by='pricePerServing').head(10).reset_index(drop=True)
    else:
        final_results = final_results

    
    while True:
        print(final_results[['title', 'pricePerServing']])
        index_recipe = input("Select a dish number for which you want recipe options? ")
        while True:
            if index_recipe.isnumeric():
                index_recipe = int(index_recipe)
                break
            else:
                index_recipe = input("Please enter a valid index number ")
                continue

        additional_url = get_additionalrecipe(final_results['title'][index_recipe])
        print(f"{final_results['title'][index_recipe]} Recipe URL:")
        print(final_results['sourceUrl'][index_recipe])
        if len(additional_url) == 0:
            print("No other options found")
        elif len(additional_url) == 1 and additional_url[0] == final_results['sourceUrl'][index_recipe]:
            print("No other options found")
        else:
            print("Similar Recipe Options:")
            for i in additional_url:
                if i != final_results['sourceUrl'][index_recipe]:
                    print(i)
        
        diff_index = input("Would you like to select a different dish? ")
        if diff_index == "Yes" or diff_index == "yes":
            continue
        else:
            break



if __name__ == "__main__":
    main()








