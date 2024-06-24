from crewai_tools import BaseTool

class foodDatabase(BaseTool):
    name: str = "Food Database"
    description: str = (
        "To query and search for meals, recipe and dietary pereferneces based on user input"
    )

    def search_usda_recipes(diet, meal_type):
        """ Search for recipes in USDA FoodData Central based on diet and meal type"""
        api_key = ['4ipUHVZeHblzwKU08B9ywtAGTvjhxAV3rHemRRbr']
        url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={diet} {meal_type}&api_key={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            foods = response.json().get('foods', [])
            results = []
            for food in foods[:4]: # Limit to top 4 results
                results.append('\n'.join([
                    f"Description: {food.get('description', 'N/A')}",
                    f"Food Category: {food.get('foodCategory', 'N/A')}",
                    f"Brand Owner: {food.get('brandOwner', 'N/A')}",
                    f"Ingredients: {food.get('ingredients', 'N/A')}",
                    "\n-----------------------"
                ]))
            return '\n'.join(results)
        else:
            return f"Error: Unable to fetch recipes, status code {response.status_code}"
        
