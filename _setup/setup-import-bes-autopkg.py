#!/usr/bin/env python
"""
Import BES files to setup AutoPkg user
"""

import random
import string
import sys

import bescli
import lxml.etree
import validate_bes_xml


def rand_password(length=20):
    """get a random password"""
    # print function name:
    print(sys._getframe().f_code.co_name + "()")

    all_safe_chars = string.ascii_letters + string.digits + "!#()*+,-.:;<=>?[]^_|~"

    # https://medium.com/analytics-vidhya/create-a-random-password-generator-using-python-2fea485e9da9
    password = "".join(random.sample(all_safe_chars, length))
    return password


def bigfix_login():
    """do login with besapi"""
    # print function name:
    print(sys._getframe().f_code.co_name + "()")

    bigfix_cli = bescli.bescli.BESCLInterface()
    bigfix_cli.do_conf()
    if bigfix_cli.bes_conn:
        print(f"Connected to: {bigfix_cli.BES_ROOT_SERVER}")
    else:
        bigfix_cli.do_login()

    if not bigfix_cli.bes_conn:
        print("ERROR: Not Connected! Fix Login!")
        sys.exit(99)
    else:
        bigfix_cli.do_saveconf()

    return bigfix_cli


def get_user_resource(bigfix_conn, user_name="autopkg"):
    """get bigfix operator resource URI"""
    # print function name:
    print(sys._getframe().f_code.co_name + "()")

    result_users = bigfix_conn.get(f"operator/{user_name}")

    if result_users and "Operator does not exist" not in str(result_users):
        # print(result_users)
        return result_users.besobj.Operator.attrib["Resource"]


def create_user(bigfix_conn, bes_file_path):
    """create new user"""
    # print function name:
    print(sys._getframe().f_code.co_name + "()")

    xml_parsed = lxml.etree.parse(bes_file_path)
    new_user_name = xml_parsed.xpath("/BESAPI/Operator/Name/text()")[0]
    result_user = get_user_resource(bigfix_conn, new_user_name)

    if result_user:
        print(f"WARNING: User Already Exists: {new_user_name}")
        return result_user
    print(f"Creating User {new_user_name}")
    _ = bigfix_conn.post("operators", lxml.etree.tostring(xml_parsed))
    # print(user_result)
    return get_user_resource(bigfix_conn, new_user_name)


def get_group_resource(
    bigfix_conn, site_path="master", group_name="AutoPkg Test Machines"
):
    """get computer group resource URI"""
    # print function name:
    print(sys._getframe().f_code.co_name + "()")

    result_groups = bigfix_conn.get(f"computergroups/{site_path}")

    for group in result_groups.besobj.ComputerGroup:
        if group_name in str(group.Name):
            return group.attrib["Resource"]


def create_group(bigfix_conn, bes_file_path, site_path="master"):
    """create a new group"""
    # print function name:
    print(sys._getframe().f_code.co_name + "()")
    xml_parsed = lxml.etree.parse(bes_file_path)
    new_group_name = xml_parsed.xpath("/BES/ComputerGroup/Title/text()")[0]

    existing_group_resource = get_group_resource(bigfix_conn, site_path, new_group_name)

    if existing_group_resource:
        print(f"WARNING: Group Already Exists: {new_group_name}")
        return existing_group_resource

    # print(lxml.etree.tostring(xml_parsed))

    _ = bigfix_conn.post(f"computergroups/{site_path}", lxml.etree.tostring(xml_parsed))

    return get_group_resource(bigfix_conn, site_path, new_group_name)


def get_site_output(bigfix_conn, site_path="custom", site_name="autopkg"):
    """get output of site"""
    # print function name:
    print(sys._getframe().f_code.co_name + "()")
    result_site = bigfix_conn.get(f"site/{site_path}/{site_name}")
    print(result_site)

    if result_site and "does not exist" not in str(result_site):
        # print(result_users)
        return result_site


def create_site(bigfix_conn, bes_file_path, site_path="custom"):
    """create new site"""
    # print function name:
    print(sys._getframe().f_code.co_name + "()")
    xml_parsed = lxml.etree.parse(bes_file_path)
    new_site_name = xml_parsed.xpath("/BES/CustomSite/Name/text()")[0]
    print(new_site_name)
    result_site = get_site_output(bigfix_conn, site_path, new_site_name)

    if result_site:
        print(f"WARNING: Site already exists: {new_site_name}")
        return result_site

    _ = bigfix_conn.post("sites", lxml.etree.tostring(xml_parsed))

    return get_site_output(bigfix_conn, site_path, new_site_name)


def main():
    """execution starts here:"""
    # print function name:
    print(sys._getframe().f_code.co_name + "()")

    print(rand_password())
    exit_code = validate_bes_xml.validate_bes_xml.validate_all_files()
    if exit_code != 0:
        print("ERROR: XML Validation!")
        sys.exit(exit_code)
    bigfix_cli = bigfix_login()
    group_resource = create_group(
        bigfix_cli.bes_conn, r"./_setup/Group-AutoPkgTestMachines.bes",
    )
    print(group_resource)
    print(create_user(bigfix_cli.bes_conn, r"./_setup/Operator-API_AutoPkg.bes"))

    print(create_site(bigfix_cli.bes_conn, r"./_setup/Site-autopkg.bes"))


if __name__ == "__main__":
    print("This is a work in progress!")
    sys.exit(0)
    main()
