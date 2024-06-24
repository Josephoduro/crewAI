#!/usr/bin/env python
import sys
from menu_planner.crew import MenuPlannerCrew
from dotenv import load_dotenv
import agentops

load_dotenv()
agentops.init()


def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    diet = input(" Enter your dietary perence: ")
    meal_type = input("What specific meal are you looking for? ")
    ingredients = input(" Do you have specific ingredients you would like to include? ")
    
    cuisine = input("Please specify the cuisine: ")
    nutrition = input("What specific nutritional contents do you require? ")
    recipe = input ("What recipe would you want to have in the menu? ")
    goals = input("What nutritional goals do you want to achieve with this menu? ")


    inputs = {
        "diet": diet,
        "meal_type": meal_type,
        "cuisine": cuisine,
        "ingredient": ingredients,
        "nutrition": nutrition,
        "recipe": recipe,
        "goals": goals,
        }
    result = MenuPlannerCrew().crew().kickoff(inputs=inputs)
    crew = MenuPlannerCrew()
    print("Analysis Result:")
    print(result)

if __name__ == "__main__":
    run()
