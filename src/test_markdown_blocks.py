import unittest
import textwrap
from markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,   
)
from markdown_blocks import BlockType

class TestMarkdownToBlocks(unittest.TestCase):
        
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

class TestBlockToBlockType(unittest.TestCase):

    def test_block_to_block_headings(self):
        result = block_to_block_type("# Largest Heading")
        result2 = block_to_block_type("### Mid-size Heading")
        result3 = block_to_block_type("###### Smallest Heading")

        assert result == BlockType.HEADING
        assert result2 == BlockType.HEADING
        assert result3 == BlockType.HEADING
    
    def test_block_to_block_code(self):
        code_block = textwrap.dedent("""\
            ```
            def func():
                print("hello")
            ```""")
        
        result = block_to_block_type(code_block)
        self.assertEqual(result, BlockType.CODE)
    
    def test_block_to_block_quote(self):
        quotes = textwrap.dedent("""\
            > This is a quote.
            > This is a second line of a quote.""")  
               
        result = block_to_block_type(quotes)
        self.assertEqual(result, BlockType.QUOTE)
    
    def test_block_to_block_unordered_list(self):
        u_list = textwrap.dedent("""\
            - This is first line of an unordered list.
            - This is a second line.
            - This is a third line with an asterisk to test if it works here.""")
        
        result = block_to_block_type(u_list)
        self.assertEqual(result, BlockType.U_LIST)
    
    def test_block_to_block_ordered_list(self):
        o_list = textwrap.dedent("""\
            1. Number 1
            2. Number 2
            3. Number 3 """)
        
        result = block_to_block_type(o_list)
        self.assertEqual(result, BlockType.O_LIST)
    
    def test_block_to_block_paragraph(self):
        paragraph = textwrap.dedent("""\
            This is just multiple,
            lines of paragraphs, to
            check that paragraph blocks,
            passthrough without problems.""")
        
        result = block_to_block_type(paragraph)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_block_to_block_edge_case_headings(self):
        self.assertEqual(block_to_block_type("####### Too many hashes"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("#No space"), BlockType.PARAGRAPH)
    
    def test_block_to_block_edge_case_broken_lists(self):
        broken_quote = textwrap.dedent("""\
            > This is a quote.
            But this line forgot the arrow.""")
        self.assertEqual(block_to_block_type(broken_quote), BlockType.PARAGRAPH)

        broken_u_list = textwrap.dedent("""\
            - Good line
            -Bad line without space""")
        self.assertEqual(block_to_block_type(broken_u_list), BlockType.PARAGRAPH)

    def test_block_to_block_edge_case_ordered_lists(self):
        bad_start_o_list = textwrap.dedent("""\
            2. Started with two
            3. Three""")
        self.assertEqual(block_to_block_type(bad_start_o_list), BlockType.PARAGRAPH)

        skipping_o_list = textwrap.dedent("""\
            1. One
            3. Three""")
        self.assertEqual(block_to_block_type(skipping_o_list), BlockType.PARAGRAPH)
