#!/usr/bin/env python
"""
run all AutoPkg recipes in repo
"""
import os
import subprocess

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


def run_all_recipes(recipe_path_array):
    print("run_all_recipes()")
    print(len(recipe_path_array))
    recipe_identifiers = get_all_identifiers(recipe_path_array)

    for recipe_id in recipe_identifiers:
        run_recipe(recipe_id)


def main():
    print("main()")
    recipe_path_array = get_all_files()
    run_all_recipes(recipe_path_array)


if __name__ == "__main__":
    main()
