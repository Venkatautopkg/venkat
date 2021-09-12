#!/usr/bin/env python
"""
run all AutoPkg recipes in repo
"""
import os
import random
import subprocess
import sys
import time

import yaml


def get_all_files(extension=".bigfix.recipe.yaml"):
    # https://stackoverflow.com/a/3964691/861745
    print("get_all_files()")
    file_paths = []
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(extension):
                if "Example" not in file:
                    file_paths.append(os.path.join(root, file))
    return file_paths


def get_recipe_identifier(recipe_path):
    # print("get_recipe_identifier(recipe_path)")
    with open(recipe_path, "rb") as stream:
        try:
            yaml_data = yaml.safe_load(stream)
        except yaml.YAMLError as err:
            print(err)
    # https://stackoverflow.com/a/50432697/861745
    return yaml_data["Identifier"]


def get_all_identifiers(recipe_path_array):
    print("get_all_identifiers(recipe_path_array)")
    recipe_identifiers = []
    for path in recipe_path_array:
        recipe_identifiers.append(get_recipe_identifier(path))
    return recipe_identifiers


def run_recipe(recipe_id):
    print("run_recipe(recipe_id)")
    # print(recipe_id)
    run_cmd = ["python", "../autopkg/Code/autopkg", "run", "-v", recipe_id]
    print(f"Starting: {recipe_id}")
    run_output = subprocess.check_output(run_cmd).decode()
    # print(run_output)
    if "Receipt written to" in run_output:
        print(f"Completed: {recipe_id}")
        print(run_output.split("Receipt written to", 1)[1].split("\n", 1)[1])
    else:
        print(f"ERROR: {recipe_id}")


def run_all_recipes(recipe_identifiers):
    print("run_all_recipes()")
    print(f"Number of Recipes to Run: {len(recipe_identifiers)}")

    # randomize list of recipes to not run same vendor in order
    # https://stackoverflow.com/questions/9252373/random-iteration-in-python
    random.shuffle(recipe_identifiers)

    for recipe_id in recipe_identifiers:
        run_recipe(recipe_id)
        # sleep 5 seconds between each
        time.sleep(5)


def run_firsttime_recipes(recipe_identifiers):
    # print function name:
    print(sys._getframe().f_code.co_name + "()")
    print(f"Total Recipes: {len(recipe_identifiers)}")
    # ~/Library/AutoPkg/Cache
    autopkg_cache_path = os.path.expanduser("~/Library/AutoPkg/Cache")
    # get directories in cache
    dir_listing = os.listdir(autopkg_cache_path)
    for name in dir_listing:
        if name in recipe_identifiers:
            # remove recipe_id if directory in cache
            recipe_identifiers.remove(name)

    run_all_recipes(recipe_identifiers)


def main():
    print("main()")
    recipe_path_array = get_all_files()
    recipe_identifiers = get_all_identifiers(recipe_path_array)
    run_firsttime_recipes(recipe_identifiers)


if __name__ == "__main__":
    main()
