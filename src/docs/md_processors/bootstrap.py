from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension


class BootstrapTreeprocessor(Treeprocessor):
    def run(self, root):
        for table_element in root.iter('table'):
            table_element.set('class', f'table table-dark')
        # No return statement is same as `return None`


class BootstrapExtension(Extension):
    """ Bootstrap extension for Python-Markdown to add bootstrap specific classes. """

    def extendMarkdown(self, md):
        md.registerExtension(self)

        md.treeprocessors.register(BootstrapTreeprocessor(md.parser), 'bootstrap', 100)


class FakeTitlesTreeprocessor(Treeprocessor):
    def run(self, root):
        for element in root.iter('*'):
            if len(element.tag) == 2 and element.tag.startswith('h'):
                element.set('class', element.tag)
                element.tag = 'div'
        # No return statement is same as `return None`


class BootstrapFakeTitlesExtension(Extension):
    """ Bootstrap extension for Python-Markdown to add bootstrap specific title classes. """

    def extendMarkdown(self, md):
        md.registerExtension(self)

        md.treeprocessors.register(FakeTitlesTreeprocessor(md.parser), 'bootstrapfaketitles', 0)
