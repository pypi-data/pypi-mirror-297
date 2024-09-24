from mkdocs.config import base, config_options as c

class _OldToNewStrings(base.Config):
    old_value = c.Type(str)
    new_value = c.Type(str)

class StringsMarkdownReplacementPluginConfig(base.Config):
    strings_replacements = c.ListOfItems(c.SubConfig(_OldToNewStrings))

class StringsMarkdownReplacementPlugin(mkdocs.plugins.BasePlugin[StringsMarkdownReplacementPluginConfig]):

    def on_page_markdown(self, markdown: str, config: MkDocsConfig, **kwargs):
        return markdown.replace('[[_TOSP_]]', '')