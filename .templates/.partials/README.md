# .partials folder

This folder is for partial mustashe templates

For use with Templates and the `com.github.jgstew.SharedProcessors/ContentFromTemplate` Processor

It is possible to reference partials from within a subfolder of this folder, but generally partials would be found directly within this `.partials` folder.

The default partials path for the `ContentFromTemplate` Processor is `.templates/.partials` which should be the relative path of this folder from root project folder.

## Example:

Within a template you may have:

```
This is an example template {{> DescriptionIcon }}
```

Where `{{> DescriptionIcon }}` is within the template will be replaced by the template info found within `.templates/.partials/DescriptionIcon.mustache`
