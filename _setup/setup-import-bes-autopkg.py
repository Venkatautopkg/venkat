#!/usr/bin/env python
"""
Import BES files to setup AutoPkg user
"""

import random
import string
import sys

import bescli


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


def main():
    # print function name:
    print(sys._getframe().f_code.co_name + "()")

    print(rand_password())
    bigfix_conn = bigfix_login()
    print(get_group_resource(bigfix_conn))


if __name__ == "__main__":
    print("This is a work in progress!")
    sys.exit(0)
    main()
