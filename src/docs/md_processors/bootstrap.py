from xml.etree.ElementTree import Element

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
    def __init__(self, md):
        super().__init__(md)
        self.level_from = 0

    def run(self, root):
        for element in list(root.iter('*')):
            element: Element
            if len(element.tag) == 2 and element.tag.startswith('h') and element.tag[1].isdigit():
                if int(element.tag[1]) >= self.level_from:
                    element.set('class', element.tag)
                    element.tag = 'div'

                if element.text:
                    element.set('id', element.text.replace('?', '').strip().replace(' ', '-').lower())
            if element.tag == "img":
                src = element.get('src')
                alt = element.get('alt', None)

                element.tag = "figure"
                element.set('class', 'figure mx-auto d-block')

                img = Element("img", attrib={"src": src, "alt": alt, "class": "img-fluid rounded mx-auto d-block"})
                element.append(img)

                figcaption = Element("figcaption", attrib={"class": "figure-caption text-center"})
                figcaption.text = alt
                element.append(figcaption)


        # No return statement is same as `return None`


def get_fake_title_extension(level_from=3):
    class BootstrapFakeTitlesExtension(Extension):
        """ Bootstrap extension for Python-Markdown to add bootstrap specific title classes. """

        def extendMarkdown(self, md):
            md.registerExtension(self)
            ftp = FakeTitlesTreeprocessor(md.parser)
            ftp.level_from = level_from
            md.treeprocessors.register(ftp, 'bootstrapfaketitles', 0)

    return BootstrapFakeTitlesExtension
