"""
run `gh` command to check for issues that need added to a project
"""
import subprocess
import sys


def get_issues_to_fix(label):
    # https://github.com/_USER_/_REPO_/issues?q=is%3Aissue+is%3Aopen+no%3Aproject+label%3A{label}
    # gh issue list --label recipe --search no:project --json number --template ';{{ range .}}{{.number}};{{end}}'
    gh_command = [
        "gh",
        "issue",
        "list",
        "--label",
        label,
        "--search",
        "no:project",
        "--json",
        "number",
        "--template",
        "';{{ range .}}{{.number}};{{end}}'",
    ]
    # print(gh_command)

    gh_output = subprocess.check_output(gh_command).decode()
    # print(gh_output)

    if ";" not in gh_output:
        print("No Issues found that need fixed.")
        sys.exit(0)

    issue_array = gh_output.split(";")
    # print(issue_array)

    issue_array_int = []
    for item in issue_array:
        try:
            # if item is int, add to array
            issue_array_int.append(int(item))
        except ValueError:
            continue

    if len(issue_array_int) == 0:
        print("No Issues found that need fixed.")
        sys.exit(0)

    return issue_array_int


def add_issue_to_project(issue_number, project_name):
    print(f" - fixing issue # {issue_number} -")
    # gh issue edit ## --add-project "AutoPkg BigFix Automation"
    gh_command = [
        "gh",
        "issue",
        "edit",
        str(int(issue_number)),
        "--add-project",
        f"'{project_name}'",
    ]
    gh_output = subprocess.check_output(gh_command).decode()
    print(gh_output)


def main(label_name, project_name, autofix=False):
    """Execution starts here"""
    # print(f"\nRunning {__file__}")
    issue_array_int = get_issues_to_fix(label_name)
    issue_count = len(issue_array_int)
    print(f"{issue_count} issues to fix: {issue_array_int}")
    if autofix:
        for issue_number in issue_array_int:
            add_issue_to_project(issue_number, project_name)
    else:
        # exit with code = number of issues to fix
        print(f"WARNING: {issue_count} issues not autofixed.")
        sys.exit(issue_count)


if __name__ == "__main__":
    main("recipe", "AutoPkg BigFix Automation")
