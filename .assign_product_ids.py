"""
assign unique content_product_id to bigfix.recipie.yaml files in repo if not found
"""

import os


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
                vendor_folders.append(item)
                # TODO: remove this line once done testing:
                break

    return vendor_folders


def main(root_folder=None):
    """Execution starts here"""
    print("main()")
    if not root_folder:
        root_folder = os.path.abspath(os.path.curdir)

    print(get_vendor_folders(root_folder))


if __name__ == "__main__":
    main()
