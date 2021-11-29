"""
assign unique content_product_id to bigfix.recipie.yaml files in repo if not found
"""

import os

import yaml


def get_vendor_folders(root_folder):
    """get the vendor folders to work on"""
    vendor_folders = []
    if not os.path.isdir(root_folder):
        return []

    for item in os.listdir(root_folder):
        if os.path.isdir(item):
            # Note: would be faster if this stopped on first success:
            if (
                len([f for f in os.listdir(item) if f.endswith(".bigfix.recipe.yaml")])
                > 0
            ):
                vendor_folders.append(os.path.join(root_folder, item))

    return vendor_folders


def get_file_product_id(file_item):
    """read content_id_product from yaml"""
    with open(file_item, "rb") as stream:
        try:
            yaml_data = yaml.safe_load(stream)
        except yaml.YAMLError as err:
            print(err)
    try:
        return int(yaml_data["Input"]["content_id_product"])
    except (KeyError, ValueError):
        return None


def get_folder_product_ids(folder_item):
    """get all content_id_products currently defined in the folder"""
    product_ids = []

    for item in os.listdir(folder_item):
        if os.path.isfile(os.path.join(folder_item, item)) and item.endswith(
            ".bigfix.recipe.yaml"
        ):
            print(item)
            product_id = get_file_product_id(os.path.join(folder_item, item))
            if product_id:
                product_ids.append(product_id)

    return product_ids


def main(root_folder=None):
    """Execution starts here"""
    print("main()")
    if not root_folder:
        root_folder = os.path.abspath(os.path.curdir)

    vendor_folders = get_vendor_folders(root_folder)
    # print(vendor_folders)

    print(get_folder_product_ids(vendor_folders[0]))
    print(get_folder_product_ids(vendor_folders[1]))


if __name__ == "__main__":
    main()
