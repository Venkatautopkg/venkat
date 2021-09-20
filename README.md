# bigfix-recipes

AutoPkg recipes created by the BigFix org

Check your Windows Dev Env Setup using `check_setup_win.bat`

## gh api command line:

- Get issue statuses: `gh issue list --label recipe --limit 300 --state all --json state,assignees,projectCards,number,title --template '{{range .}}{{range .assignees}}{{.login}},{{.name}},{{end}}{{range .projectCards}}{{.column.name}}{{end}},{{.number}},{{.title}}{{println}}{{end}}'`
- Get issues without project assignment: `gh issue list --label recipe --search no:project --json createdAt,number,url,title`

## Related Documentation:

- https://github.com/jgstew/jgstew-recipes/wiki/Getting-Started-with-AutoPkg-Recipes
- https://github.com/autopkg/autopkg/wiki/Getting-Started-On-Windows
