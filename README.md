# bigfix-recipes

AutoPkg recipes created by the BigFix org

Check your Windows Dev Env Setup using `check_setup_win.bat`

## gh api command line:

- Get issue statuses: `gh issue list --label recipe --limit 333 --state all --json state,assignees,projectCards,number,title --template '{{range .}}{{range .assignees}}{{if ne .name \"\"}}{{.name}}{{else}}{{.login}}{{end}},{{end}}{{range .projectCards}}{{if eq .column.name \"To do\"}}0.5{{ end }}{{if eq .column.name \"In progress\"}}1{{ end }}{{if eq .column.name \"Done\"}}2{{ end }}{{if eq .column.name \"Verified\"}}4{{ end }},{{.column.name}}{{end}},{{.number}},{{.title}}{{println}}{{end}}'`
- Get issues without project assignment: `gh issue list --label recipe --search no:project --json createdAt,number,url,title`

## Related Documentation:

- https://github.com/jgstew/jgstew-recipes/wiki/Getting-Started-with-AutoPkg-Recipes
- https://github.com/autopkg/autopkg/wiki/Getting-Started-On-Windows
