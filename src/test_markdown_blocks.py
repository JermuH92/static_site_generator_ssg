import unittest
import textwrap
from markdown_blocks import markdown_to_blocks

class TestMarkdownBlocks(unittest.TestCase):
        
        def test_markdown_to_blocks(self):
            md = textwrap.dedent("""
                This is **bolded** paragraph

                This is another paragraph with _italic_ text and `code` here
                This is the same paragraph on a new line

                - This is a list
                - with items
            """)
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )
        
        def test_markdown_to_blocks_extra_blank_lines(self):
            md = textwrap.dedent("""\
                # Title


                Paragraph here
            """)
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                 blocks,
                 [
                    "# Title",
                    "Paragraph here"  
                 ],
            )
        
        def test_markdown_to_blocks_single_block(self):
             md = textwrap.dedent("""
                Just one block
                with two lines
            """)
             blocks = markdown_to_blocks(md)
             self.assertEqual(
                  blocks,
                  ["Just one block\nwith two lines"],
             )
        
        def test_markdown_to_blocks_empty_string(self):
             md = ""
             blocks = markdown_to_blocks(md)
             self.assertEqual(blocks, [])
        
        def test_markdown_to_blocks_strips_whitespace(self):
             md = textwrap.dedent("""\
                First block
                    
                Second block
            """)
             blocks = markdown_to_blocks(md)
             self.assertEqual(
                  blocks,
                  ["First block", "Second block"]
             )
