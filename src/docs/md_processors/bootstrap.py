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
