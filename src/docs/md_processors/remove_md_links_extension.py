from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension


def get_all_element_children(root):
    childs = []
    for child in root:
        childs.append(child)
        childs.extend(get_all_element_children(child))
    return childs

class MdLinksTreeprocessor(Treeprocessor):
    def run(self, root):
        for element in get_all_element_children(root):
            if element.tag == 'a':
                href = element.get('href')
                if href.endswith('.md'):
                    element.set('href', href[:-3])

        # No return statement is same as `return None`


class MdLinksExtension(Extension):
    """ Remove .md from links """

    def extendMarkdown(self, md):
        md.registerExtension(self)

        md.treeprocessors.register(MdLinksTreeprocessor(md.parser), 'mdlinks', 0)
