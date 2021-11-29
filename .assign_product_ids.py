"""
assign unique content_product_id to bigfix.recipie.yaml files in repo if not found
"""

import os

import ruamel.yaml
import yaml


def patch_ruamel_yaml_emitter_no_blank_lines():
    """change ruamel.yaml to not produce blank lines after comments"""
    # https://stackoverflow.com/a/53890725/861745
    ruamel.yaml.emitter.Emitter.old_write_comment = (
        ruamel.yaml.emitter.Emitter.write_comment
    )

    def write_comment(self, comment, *args, **kwargs):
        # print("{:02d} {:02d} {!r}".format(self.column, comment.start_mark.column, comment.value))
        comment.value = comment.value.replace("\r\n", "\n")
        # if comment.value.strip():
        self.old_write_comment(comment, *args, **kwargs)

    ruamel.yaml.emitter.Emitter.write_comment = write_comment


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
        item_path = os.path.join(folder_item, item)
        if os.path.isfile(item_path) and item.endswith(".bigfix.recipe.yaml"):
            product_id = get_file_product_id(item_path)
            if product_id:
                product_ids.append(product_id)

    return product_ids


def write_missing_product_id(file_item, next_id):
    """write product id into yaml file"""
    print("00" + str(next_id))
    print(file_item)
    ruamel_yaml = ruamel.yaml.YAML()
    # keep current quotes in place:
    ruamel_yaml.preserve_quotes = True
    # add / keep starting `---` at top of file
    ruamel_yaml.explicit_start = True
    # https://stackoverflow.com/a/44389139/861745
    ruamel_yaml.indent(mapping=2, sequence=4, offset=2)

    with open(file_item, "rb") as stream:
        yaml_data = ruamel_yaml.load(stream)
    yaml_data["Input"][
        "content_id_product"
    ] = ruamel.yaml.scalarstring.DoubleQuotedScalarString("00" + str(next_id))
    print(yaml_data["Input"])
    with open(file_item, "w") as f:
        ruamel_yaml.dump(yaml_data, f)
    return next_id


def write_missing_product_ids(folder_item):
    """write missing content_id_products for bigfix recipes in a vendor folder"""

    product_ids = get_folder_product_ids(folder_item)
    if len(product_ids) == 0:
        product_ids.append(0)

    for item in os.listdir(folder_item):
        item_path = os.path.join(folder_item, item)
        if (
            os.path.isfile(item_path)
            and item.endswith(".bigfix.recipe.yaml")
            and not get_file_product_id(item_path)
        ):
            product_ids.append(
                write_missing_product_id(item_path, max(product_ids) + 1)
            )

    return product_ids


def main(root_folder=None):
    """Execution starts here"""
    print("main()")

    patch_ruamel_yaml_emitter_no_blank_lines()

    if not root_folder:
        root_folder = os.path.abspath(os.path.curdir)

    vendor_folders = get_vendor_folders(root_folder)
    # print(vendor_folders)

    print(write_missing_product_ids(vendor_folders[0]))
    print(write_missing_product_ids(vendor_folders[1]))


if __name__ == "__main__":
    main()
