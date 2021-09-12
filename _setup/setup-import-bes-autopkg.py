#!/usr/bin/env python
"""
Import BES files to setup AutoPkg user
"""

import random
import string
import sys

import bescli
import validate_bes_xml
import lxml.etree


def rand_password(length=20):
    # print function name:
    print(sys._getframe().f_code.co_name + "()")

    all = string.ascii_letters + string.digits + "!#()*+,-.:;<=>?[]^_|~"
    # print(all)
    password = "".join(random.sample(all, length))
    return password


def bigfix_login():
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

    return bigfix_cli.bes_conn


def get_group_resource(
    bigfix_conn, site_path="master", group_name="AutoPkg Test Machines"
):
    # print function name:
    print(sys._getframe().f_code.co_name + "()")

    result_groups = bigfix_conn.get(f"computergroups/{site_path}")

    for group in result_groups.besobj.ComputerGroup:
        if group_name in str(group.Name):
            return group.attrib["Resource"]


def create_group(bigfix_conn, bes_file_path, site_path="master"):
    # print function name:
    print(sys._getframe().f_code.co_name + "()")
    xml_parsed = lxml.etree.parse(bes_file_path)
    new_group_name = xml_parsed.xpath("/BES/ComputerGroup/Title/text()")[0]

    existing_group_resource = get_group_resource(bigfix_conn, site_path, new_group_name)

    if existing_group_resource:
        print("WARNING: Group Already Exists")
        return existing_group_resource

    print(lxml.etree.tostring(xml_parsed))

    result_new_group = bigfix_conn.post(
        f"computergroups/{site_path}", lxml.etree.tostring(xml_parsed)
    )

    return get_group_resource(bigfix_conn, site_path, new_group_name)


def main():
    # print function name:
    print(sys._getframe().f_code.co_name + "()")

    print(rand_password())
    exit_code = validate_bes_xml.validate_bes_xml.validate_all_files()
    if exit_code != 0:
        print("ERROR: XML Validation!")
        sys.exit(exit_code)
    bigfix_conn = bigfix_login()
    group_resource = create_group(
        bigfix_conn,
        r"./_setup/Group-AutoPkgTestMachines.bes",
    )
    print(group_resource)


if __name__ == "__main__":
    print("This is a work in progress!")
    sys.exit(0)
    main()
