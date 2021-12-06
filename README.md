# bigfix-recipes

AutoPkg recipes created by the BigFix org

Check your Windows Dev Env Setup using `check_setup_win.bat`

## gh api command line:

- Get issue statuses: `gh issue list --label recipe --limit 333 --state all --json state,assignees,projectCards,number,title --template '{{range .}}{{range .assignees}}{{if ne .name \"\"}}{{.name}}{{else}}{{.login}}{{end}},{{end}}{{range .projectCards}}{{if eq .column.name \"To do\"}}0.5{{ end }}{{if eq .column.name \"In progress\"}}1{{ end }}{{if eq .column.name \"Done\"}}2{{ end }}{{if eq .column.name \"Verified\"}}4{{ end }},{{.column.name}}{{end}},{{.number}},{{.title}}{{println}}{{end}}'`
- Get issues without project assignment: `gh issue list --label recipe --search no:project --json createdAt,number,url,title`
- Get closed patch recipes issues for publish: `gh issue list --label recipe,patch --limit 333 --state all --json title --template '{{range .}}{{.title}}{{println}}{{end}}'`

## Helpful Relevance Queries:

- Get all recipes with incorrect MinimumVersion: `pathnames of descendants whose(name of it ends with ".yaml" and exists lines containing "MinimumVersion:" whose(it contains "1.") of it) of folders "Documents\_Code\bigfix-recipes" of folders of folders "C:\Users"`
- all recipes with duplicated "patch" processing: `descendants whose(name of it ends with "bigfix.recipe.yaml" and 2 = number of lines containing "append_key: " whose(it contains "patch") of it) of folders "Documents\_Code\bigfix-recipes" of folders of folders "C:\Users"`
- recipes missing DisplayName in Input: `following texts of firsts "bigfix-recipes\" of pathnames of descendants whose(name of it ends with "bigfix.recipe.yaml" and 0 = number of lines containing " DisplayName:" whose(it starts with " DisplayName:") of it) of folders "Documents\_Code\bigfix-recipes" of folders of folders "C:\Users"`
- recipes missing VendorFolder and what the vendor folder should be: `(it, (" VendorFolder: " & it) of preceding texts of firsts "\" of it) of following texts of firsts "bigfix-recipes\" of pathnames of descendants whose(name of it ends with ".bigfix.recipe.yaml" and 0 = number of lines containing " VendorFolder: " of it) of folders "Documents\_Code\bigfix-recipes" of folders of folders "C:\Users"`
- get bes patch files: `pathnames of files whose(name of it ends with "-Update.bes") of folders whose(name of it starts with "com.github.bigfix.bigfix.") of folders "Library/AutoPkg/Cache" of folders of folders "/Users"`
- get generated CPE vendor:product that are not in real world list: `elements of (it - set of (it as trimmed string) of lines of files "/tmp/cpe vendor product.txt") of sets of preceding texts of lasts ":" of preceding texts of firsts ":*" of following texts of firsts "cpe:2.3:a:" of lines containing "cpe:2.3:a:" of files whose(exists lines containing "cpe:2.3:a:" of it AND name of it ends with ".bes") of (it; folders of it) of folders "updates-for-win-apps" of folders "Documents/_Code" of folders of folders "/Users"`

## Helpful RegEx:

- parse flat ini file for vendor_id: `^\s*vendor_id\s*=\s*(\d+)`

## Related Documentation:

- https://github.com/jgstew/jgstew-recipes/wiki/Getting-Started-with-AutoPkg-Recipes
- https://github.com/autopkg/autopkg/wiki/Getting-Started-On-Windows
