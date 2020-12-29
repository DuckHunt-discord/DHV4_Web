from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension


class MdLinksTreeprocessor(Treeprocessor):
    def __init__(self, md):
        super().__init__(md)
        self.absolute_path = ''

    def run(self, root):
        for element in root.iter('a'):
            href = element.get('href')
            if href.endswith('.md'):
                element.set('href', self.absolute_path + href[:-3])

        # No return statement is same as `return None`


def get_extension(absolute_path=''):
    class MdLinksExtension(Extension):
        """ Remove .md from links """

        def extendMarkdown(self, md):
            md.registerExtension(self)
            links = MdLinksTreeprocessor(md.parser)
            links.absolute_path = absolute_path
            md.treeprocessors.register(links, 'mdlinks', 0)

    return MdLinksExtension
