import requests
from langchain_core.tools import tool


@tool
def search_recipe(dish: str) -> str:
    """
    Search for a recipe by dish name. Returns ingredients, measurements,
    and step-by-step cooking instructions. Uses TheMealDB — free, no API key.
    """
    dish_query = dish.strip() if dish else ""
    if not dish_query:
        return "Please provide a dish name to search for."

    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={dish_query}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        return f"Error connecting to recipe database: {e}"

    meals = data.get("meals")
    if not meals:
        return f"No recipe found for '{dish_query}'. Please check the dish name and try again."

    meal = meals[0]
    name = meal.get("strMeal") or "Unknown"
    cuisine = meal.get("strArea") or "Unknown"
    category = meal.get("strCategory") or "Unknown"
    raw_instructions = meal.get("strInstructions") or ""
    instructions = raw_instructions.strip()[:1000]

    ingredients = []
    for i in range(1, 21):
        ingredient = meal.get(f"strIngredient{i}")
        measure = meal.get(f"strMeasure{i}")

        if ingredient and ingredient.strip():
            ing_clean = ingredient.strip()
            meas_clean = measure.strip() if measure else ""
            if meas_clean:
                ingredients.append(f"  • {meas_clean} {ing_clean}")
            else:
                ingredients.append(f"  • {ing_clean}")

    ingredients_list = "\n".join(ingredients) if ingredients else "  • No ingredients listed"

    return (
        f"Recipe: {name}\n"
        f"Cuisine: {cuisine} | Category: {category}\n\n"
        f"Ingredients:\n"
        f"{ingredients_list}\n\n"
        f"Instructions:\n"
        f"{instructions}"
    )
