import re
import xml.etree.ElementTree as etree

from markdown.extensions import Extension
from markdown.blockprocessors import BlockProcessor


class HintBlockProcessor(BlockProcessor):
    RE_FENCE_START = r'^{% hint style="(?P<style>[a-z]{3,})" %}\n'  # start line, e.g., `   !!!! `
    RE_FENCE_END = r'\n{% endhint %}$'  # last non-blank line, e.g, '!!!\n  \n\n'

    def test(self, parent, block):
        return re.match(self.RE_FENCE_START, block)

    def run(self, parent, blocks):
        original_block = blocks[0]
        hint_style = re.match(self.RE_FENCE_START, blocks[0]).group('style')
        blocks[0] = re.sub(self.RE_FENCE_START, '', blocks[0])

        # Find block with ending fence
        for block_num, block in enumerate(blocks):
            if re.search(self.RE_FENCE_END, block):
                # remove fence
                blocks[block_num] = re.sub(self.RE_FENCE_END, '', block)
                # render fenced area inside a new div
                e = etree.SubElement(parent, 'div')
                e.set('class', f'alert alert-{hint_style}')
                self.parser.parseBlocks(e, blocks[0:block_num + 1])
                # remove used blocks
                for i in range(0, block_num + 1):
                    blocks.pop(0)
                return True  # or could have had no return statement
        # No closing marker!  Restore and do nothing
        blocks[0] = original_block
        return False  # equivalent to our test() routine returning False


class DescriptionBlockProcessor(BlockProcessor):
    RE_FENCE_START = r'^---\ndescription'  # start line
    RE_FENCE_END = r'\n---$'  # last non-blank line

    def test(self, parent, block):
        return re.match(self.RE_FENCE_START, block)

    def run(self, parent, blocks):
        original_block = blocks[0]
        blocks[0] = re.sub(self.RE_FENCE_START, '', blocks[0])

        # Find block with ending fence
        for block_num, block in enumerate(blocks):
            if re.search(self.RE_FENCE_END, block):
                for i in range(0, block_num + 1):
                    blocks.pop(0)
                return True  # or could have had no return statement
        # No closing marker!  Restore and do nothing
        blocks[0] = original_block
        return False  # equivalent to our test() routine returning False


class HintExtension(Extension):
    """ Hint extension for Python-Markdown to support gitbook-style hints. """

    def extendMarkdown(self, md):
        """ Add Hint to Markdown instance. """
        md.registerExtension(self)

        md.parser.blockprocessors.register(HintBlockProcessor(md.parser), 'hint', 100)
        md.parser.blockprocessors.register(DescriptionBlockProcessor(md.parser), 'description', 500)
