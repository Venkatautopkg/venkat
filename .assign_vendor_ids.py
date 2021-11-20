"""
assign unique content_vendor_id to vendor_metadata.cfg files in repo if not found
"""

import configparser
import glob
import io
import os
from contextlib import contextmanager


@contextmanager
def cwd(path):
    """change the current working directory temporarily"""
    oldcwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(oldcwd)


def get_metadata_files(root_folder, meta_file_name="vendor_metadata.cfg"):
    """get all metadata files"""
    with cwd(root_folder):
        return glob.glob("*/" + meta_file_name)


def get_vendor_id(file_path):
    """read vendor id from file"""
    # https://stackoverflow.com/a/25493615/861745
    with open(file_path, "r") as f:
        config_string = "[DEFAULT]\n" + f.read()
    config = configparser.ConfigParser()
    config.read_string(config_string)
    content_id_vendor = None
    try:
        content_id_vendor = config.getint("DEFAULT", "content_id_vendor")
    except (KeyError, configparser.NoOptionError):
        pass
    return content_id_vendor


def write_vendor_id(folder_path, vendor_id, meta_file_name="vendor_metadata.cfg"):
    """write vendor id to file"""
    print("write_vendor_id(folder_path, meta_file_name)")

    config_file_path = os.path.join(folder_path, meta_file_name)
    # write ini format with no starting section
    # https://stackoverflow.com/a/66137956/861745
    config = configparser.ConfigParser()

    if os.path.isfile(config_file_path):
        with open(config_file_path, "r") as f:
            config_string = "[DEFAULT]\n" + f.read()
        config.read_string(config_string)
    config.set("DEFAULT", "content_id_vendor", str(vendor_id))
    buf = io.StringIO()
    config.write(buf)
    buf.seek(0)
    next(buf)

    with open(config_file_path, "w") as f:
        f.write(buf.read())


def get_vendor_ids(root_folder):
    """get existing vendor ids"""
    print("get_vendor_ids(root_folder)")
    meta_files = get_metadata_files(root_folder)
    vendor_ids = []
    for item in meta_files:
        vendor_id = get_vendor_id(item)
        if vendor_id:
            vendor_ids.append(vendor_id)

    if len(vendor_ids) != len(set(vendor_ids)):
        print("ERROR: duplicate vendor ids found!")

    return vendor_ids


def write_missing_vendor_ids(root_folder, meta_file_name="vendor_metadata.cfg"):
    """write missing vendor ids to file"""
    print("write_missing_vendor_ids(root_folder)")
    vendor_ids = get_vendor_ids(root_folder)
    next_id = max(vendor_ids) + 1
    with cwd(root_folder):
        folder_paths = glob.glob("*/")

    for folder_path in folder_paths:
        # exclude special folders:
        if not folder_path.startswith("_") and not folder_path.startswith("."):
            # exclude folders that already have the metadata file:
            if not os.path.isfile(os.path.join(folder_path, meta_file_name)):
                print(folder_path)
                write_vendor_id(folder_path, next_id, meta_file_name)
                next_id += 1


def main(root_folder=None):
    """Execution starts here"""
    print("main()")
    if not root_folder:
        root_folder = os.path.abspath(os.path.curdir)
    print(get_vendor_ids(root_folder))
    write_missing_vendor_ids(root_folder)


if __name__ == "__main__":
    main()
