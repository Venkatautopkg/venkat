#!/usr/bin/env python
"""
run all AutoPkg recipes in repo
"""
import datetime
import glob
import os
import random
import subprocess
import sys
import time

import yaml

datetime_NOW = datetime.datetime.now()


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
    try:
        # check if recipe has icon
        recipe_process = yaml_data["Process"]
        for item in recipe_process:
            # print(item["Processor"])
            if "com.github.jgstew.SharedProcessors/FileGetBase64" in item["Processor"]:
                return yaml_data["Identifier"]
            else:
                if "Arguments" in item:
                    if "append_key" in item["Arguments"]:
                        if "icon_base64" in item["Arguments"]["append_key"]:
                            return yaml_data["Identifier"]
    except KeyError:
        print(f"ERROR: Yaml KeyError {recipe_path}")
        return None
    # https://stackoverflow.com/a/50432697/861745
    print(f"ERROR: icon_base64 missing: {recipe_path}")
    return None


def get_all_identifiers(recipe_path_array):
    print("get_all_identifiers(recipe_path_array)")
    recipe_identifiers = []
    for path in recipe_path_array:
        recipe_id = get_recipe_identifier(path)
        if recipe_id:
            recipe_identifiers.append(recipe_id)
        else:
            print(f"WARNING: skipping {path}")
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
        # sleep 2 seconds between each
        time.sleep(2)


def get_last_runtime_recipe(recipe_identifier):
    # print(recipe_identifier)
    recipe_receipt_dir = os.path.expanduser(
        f"~/Library/AutoPkg/Cache/{recipe_identifier}/receipts"
    )
    # https://stackoverflow.com/a/39327156/861745
    files_path = os.path.join(recipe_receipt_dir, "*.plist")
    list_of_files = glob.iglob(files_path)
    latest_file = max(list_of_files, key=os.path.getctime)
    # print(latest_file)
    # datetime.datetime.fromtimestamp(t)
    return datetime.datetime.fromtimestamp(os.path.getmtime(latest_file))


def run_first_or_oldreceipt_recipes(recipe_identifiers, min_age_hours=12):
    # print function name:
    print(sys._getframe().f_code.co_name + "()")
    print(f"Total Recipes: {len(recipe_identifiers)}")
    # ~/Library/AutoPkg/Cache
    autopkg_cache_path = os.path.expanduser("~/Library/AutoPkg/Cache")
    # get directories in cache
    dir_listing = os.listdir(autopkg_cache_path)
    previous_recipes = []
    for name in dir_listing:
        if name in recipe_identifiers:
            # remove recipe_id if directory in cache
            recipe_identifiers.remove(name)
            previous_recipes.append(name)

    max_age_minutes = 0
    # add back recipes that haven't been run for min_age_hours
    for recipe_id in previous_recipes:
        duration_s = (datetime_NOW - get_last_runtime_recipe(recipe_id)).total_seconds()
        # https://stackoverflow.com/a/47207182/861745
        max_age_minutes = max(max_age_minutes, int(divmod(duration_s, 60)[0]))
        duration_h = int(divmod(duration_s, 3600)[0])
        if duration_h > min_age_hours:
            recipe_identifiers.append(recipe_id)

    print(f"Oldest Recipe Run: {max_age_minutes} minutes ago.")
    run_all_recipes(recipe_identifiers)


def main():
    print("main()")
    recipe_path_array = get_all_files()
    recipe_identifiers = get_all_identifiers(recipe_path_array)
    run_first_or_oldreceipt_recipes(recipe_identifiers)


if __name__ == "__main__":
    main()
