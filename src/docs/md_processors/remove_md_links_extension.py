from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension


class MdLinksTreeprocessor(Treeprocessor):
    def run(self, root):
        for element in root.iter('a'):
            href = element.get('href')
            if href.endswith('.md'):
                element.set('href', href[:-3])

        # No return statement is same as `return None`


class MdLinksExtension(Extension):
    """ Remove .md from links """

    def extendMarkdown(self, md):
        md.registerExtension(self)

        md.treeprocessors.register(MdLinksTreeprocessor(md.parser), 'mdlinks', 0)
