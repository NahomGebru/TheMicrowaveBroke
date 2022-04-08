import os
import requests
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


def recipe_search(ingredients, cuisine, diet, intolerances):
    API_KEY = os.getenv("SPOON_API_KEY")

    # Assuming that the information comes as an array, Turns it into string for API params
    param_Ingredients = ",".join(ingredients)
    param_cuisine = ",".join(cuisine)
    param_diet = ",".join(diet)
    param_intolerances = ",".join(intolerances)

    id_params = {
        "apiKey": API_KEY,
        "ingredients": param_Ingredients,
        "sort": "min-missing-ingrediants",
    }

    # Add params as we need them
    if param_cuisine:
        id_params["cuisine"] = param_cuisine

    if param_diet:
        id_params["diet"] = param_diet

    if param_intolerances:
        id_params["intolerances"] = param_intolerances

    id_response = requests.get(
        "https://api.spoonacular.com/recipes/complexSearch",
        params=id_params,
    )

    id_response_json = id_response.json()

    int_idlist = []
    for i in range(len(id_response_json["results"])):
        int_idlist.append(id_response_json["results"][i]["id"])

    string_idlist = map(str, int_idlist)
    param_id_list = ",".join(string_idlist)
    recipe_titles = []
    recipe_pictures = []
    recipe_links = []

    # We have to do a second round as the complex search does not give link urls
    recipe_params = {
        "apiKey": API_KEY,
        "ids": param_id_list,
    }

    recipe_response = requests.get(
        "https://api.spoonacular.com/recipes/informationBulk",
        params=recipe_params,
    )

    recipe_response_json = recipe_response.json()

    for i in range(len(recipe_response_json)):
        recipe_titles.append(recipe_response_json[i]["title"])
        recipe_pictures.append(recipe_response_json[i]["image"])
        recipe_links.append(recipe_response_json[i]["sourceUrl"])

    return (recipe_titles, recipe_pictures, recipe_links)
