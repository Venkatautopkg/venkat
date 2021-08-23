---
name: AutoPkg Recipe
about: Track creation of AutoPkg Recipe
title: 'Recipe: PRODUCT_NAME'
labels: recipe
assignees: ''
---

Create the PRODUCT_NAME AutoPkg recipe to generate BigFix content

## ToDo:
- [ ] **Assign yourself this issue**
  - Add yourself under "Assignees" in right side column
  - Add this issue to Project "AutoPkg BigFix Automation" in right side column
  - Set issue to "in progress" under project once started
  - Mark yourself as assigned in "Software Priorities" spreadsheet in Teams
  - Check for duplicate entries in "Software Priorities" spreadsheet
- [ ] **Software Download WebPage:** https://example/download.html
- [ ] **Example Download URL:** https://example/setup.exe
- [ ] **Silent Install Command(s):**
  - `setup.exe /S` (from chocolatey or existing BigFix example or similar)
- [ ] **Working Example Fixlet:** (link to GitHub or BigFix.Me example)
  - [ ] Suppress or [Delete Desktop](https://github.com/bigfix/bigfix-recipes/blob/580dfc444bcbd53c9f68b927ed26bc724ac8c67c/MSI-Tools/SuperOrca-Win64-Install_Update.bes.mustache#L48-L50) Shortcut
- [ ] **Fixlet/Task Mustache Template:** Vendor/ProductName-Win.bes.mustache
  - [Example BES Template](https://github.com/bigfix/bigfix-recipes/blob/main/Example-Win64-Install_Update.bes.mustache)
- [ ] **Download Recipe:** Vendor/ProductName-Win.download.recipe.yaml
  - [Download Recipe Template](https://github.com/bigfix/bigfix-recipes/blob/main/Example.download.recipe.yaml)
- [ ] **BigFix Recipe:** Vendor/ProductName-Win.bigfix.recipe.yaml
  - [BigFix Recipe Template](https://github.com/bigfix/bigfix-recipes/blob/main/Example.bigfix.recipe.yaml)
- [ ] **Test and Validate generated bigfix content**
  - Test on Windows 10 x64-bit
- [ ] **Set Issue to "Done"** Under project in right side column
