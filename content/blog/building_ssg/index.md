# The Making of my Custom SSG

[< Back Home](/)

![Static Site Generator Flow Chart](/images/ssgimage.png)

> "Another deep-end dive into an even more challenging project compared to building the first AI agent."
> -- Jere Kukkohovi
> -- May 24th, 2026

## The Introduction

This project was really challenging for me. Mostly because the data flow was even more complex compared to previous projects while also most if not all of the simple hand-holdy instructions and pseudocode was almost completely gone. 

Even after the previous course on Data Structures and Algorithms I had some difficulties on internalizing everything needed to easily push through this one.

But after struggling a bit over a week, I finally managed to make the last final push to Github and here I am, customizing the markdown
towards my own blogs needs after countless hours spent on fighting syntax, building functions and implementing unit tests for everything.

## The Build Diary and The Process

### Day 1

While the premise was pretty straightforward,
"Build the tools in **Python** that will build the actual website."

Then build it as per the course instructors set theme so the SSG generates a demo website of "Tolkien Fan Club". 

I truly wasn't prepared for the intricacies and how deep the projects concept actually went into. 
Even after gaining quite a lot of experience in making my own portfolio website, building a generator that builds the site itself in Python of all languages was a completely different beast.

- The project started off pretty simple, by throwing some HTML and CSS theory and simple stylesheets to copy into the root of the project.

- Then gave some useful links into some HTML and Markdown cheat sheets.

- And finally for the end of the first section it gave me a high-level architecture description on what will be built and why.


```Sounds simple right?```


## Day 2

### Playing around with Nodes

#### TextNodes, HTMLNodes, LeafNodes, ParentNodes and Nodes for all...


The next couple of days consisted on building different nodes and methods for these nodes, this is also where I was introduced to the usefulness using sum type enums to define the correct text type for the html nodes later down the road.

This section will be the one where I am going to be introduced and learn to dread writing unit tests for absolutely **EVERYTHING**!

> "self.assertYourself outta here!"

- `TextNode` **and** `TextType`: Built for carrying the inline block elements and their text types as enums. Plain, bold, italic and code text and also links and images.

- **First of many UnitTests**: I swear I've been seeing dreams about writing unit tests after this course. However I did find out exactly why doing so was a necessary evil for most of the building journey and also a necessary part of software development as a whole. But these tests tend to quickly explode into tens if not hundreds of lines of code per **class**.

- `HTMLNode`: Built to represent a node in an HTML document tree, like paragraph and anchor link tags and their contents, either inline or at block level.

- **UnitTests for HTMLNodes**: For every class and subclass. I learned a huge amount from functions input and test methodology just by writing test after test and considering possible edge cases for each function, aiming to eliminate most if not all of them, making building of those tests a longer process than implementing actual features.

- `LeafNode`: Child class built for the `HTMLNode` to take responsibility of a single html tag that has no children. Like a paragraph with only text inside of it. **Don't worry, I didn't forget the unit tests for it**

- **ParentNode of Recursion**: A subclass of an `HTMLNode`. Basically any node that is not a leaf node is assigned as a ParentNode. This subclass utilizes a recursive method that calls each nested child node, concatenates their generated HTML, and injects them between the parent nodes opening and closing tags. **And for this Node as well, believe it or not, even more tests written..**

- **TextNode to HTMLNode**: Built to convert and return a `TextNode` as an HTML Leaf Node with it's TextTypes tag and value. I used match case statement for this one and I truly enjoyed using it over constant if, elif, else -conditional statements. **By now you probably already know that it involved making a lot of test cases.**


Also here's only one example of the countless unit test classes and functions made throughout the course of this project.

```
class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)
#
    def test_not_eq(self):
        node3 = TextNode("This is a text node", TextType.PLAIN_TEXT)
        node4 = TextNode("This is a text node", TextType.CODE_TEXT)
        self.assertNotEqual(node3, node4)
#   
    def test_for_none(self):
        node5 = TextNode("This is more text", TextType.ITALIC_TEXT)
        node6 = TextNode("This is more text", TextType.ITALIC_TEXT, "https://www.boot.dev")
        self.assertNotEqual(node5, node6)
```

## Days 3-5

### Advantages of self-learning and AI-assistance

#### The Splitters by Delimiters (Inline Markdown Handling)

One thing that I definitely had as an advantage from the get-go, was my previous attempt on making a simple markdown parser using Python and some LLM assistance in my own personal projects and by it's design had a pretty similar splitter function, splitting by the delimiter, so at the beginning of day 3, I pretty much understood most of what was going on with this one:

- `split_nodes_delimiter`: This one I already had familiarity with. So simply explained, take old nodes that is just plain text with elements like double asterisk for bold around a word or sentence that is given as input to the function. This sentence in turn is split by it's delimiter being the double asterisks in to smaller parts, and then those parts and their values are enumerated by indices, divided in to new node compositions depending on their index remainder using modulo operator. The result is a new list of new nodes of plain text type as their own nodes and the bold asterisks divided word or sentence as a node with the bold or any other text type but plain text.

- **Regular Expressions or (regex)**: An interesting challenge, to say the least. This was actually my first time using regular expressions in two separate functions as part of a proper project. Once I figured out the patterns though, extraction for images and links inside their parentheses was very simple.

![regex meme](/images/regex.png)

- `split_nodes_image` **and** `split_nodes_link`: The usage of regular expressions and embedding the extraction process in to two helper functions, I made two new splitter functions for splitting images and links. Pretty much similar behavior, but this time I separated the plain text into two distinct parts and the first being plain text and rest being alternative texts in both links and images and obviously links and images themselves. I also made sure that if some text still remained after getting the main parts, that text would be appended as its own node at the end of the list.

- **And finally Text to TextNodes**: This functions purpose was to use all the functions together and like a factory pipeline, drive the long strings of text with all of the different words within asterisks, underscores, backticks, links and images through to produce a list of TextNode objects with correct text type for each node.

**Oh, did I almost forgot to mention the hundreds of lines of Unit Testing code for each function? Yeah.. I did that too, obviously.**

## Days 6-9

### Block Level Markdown and Page Generation

#### Splitting blocks, block types and blocks to html

By this point all the necessary inline elements that are inside the blocks were ready so now I went into building up functions for block level markdown and then follow up on handling the actual page generation.

- `markdown_to_blocks` **function**: This functions premise is to take raw markdown level string, process it by splitting it so the blocks are separated by a blank line (so two newlines needed for the split). The function returns a list of blocks, for example a heading separated by an empty line in between and then a paragraph with another empty line between the heading and paragraph blocks.

- **BlockType Enums and** `block_to_block_type`: First, I defined a class of enums so I can more easily define what a block type is. Then I built a function that returns the correct block type depending on conditionals such as if a block starts with hashes then that is a heading for sure.

**So in simple terms,** `block_to_block_type` **functions job is to assign a correct enum type depending on what special characters a block start with.** 

Currently the custom SSG supports the following block level elements:

1. headings (starting with hashes, from 1 to 6 hash characters followed by a space)
2. code (starting with three backticks a newline and ending with three backticks)
3. quotes (starting with "greater-than character and optionally a space")
4. unordered lists (starting with a dash character and followed by a space)
5. ordered lists (starting with a number 1 and followed by a period and a space, incrementing by one each new line)
6. the function checks if it's none of the above, then the block element is just a paragraph 

- **And finally** `markdown_to_html_node` **function with 8 helper functions**: This one was a long process, but definitely worth it. The main function gets help from `markdown_to_blocks` breaking the text down in to smaller blocks. I then loop over those and determine the type of the block, pass it to another helper function e.g (unordered list like this one) that splits the unordered list block in to lines, strips the dash and space using string slicing, pass the text to `text_to_children` that returns a list of LeafNodes that represent the children or "list items ("li") of the ParentNode "unordered list(ul)". This "ul" parent node is then wrapped further with a ParentNode "div".

The text passed through `text_to_children` allows us to handle inline parsing, like this paragraph has **text_to_children** in bold. It could just as well be in _italic_.

Only notable difference in helpers functionality is the code block handling.

Notice below the underscores that would normally change the words in them as italics,
or worse, raise ValueError for improper markdown syntax and crash the program:

```
def demo_code_block_no_inline_parsing():
#
    if "#" not in empty_line:
        raise ValueError
#   
    print("Not crashing this time.") 
```

> But can you guess by now, on what happened between every function implementation, as per usual? 
> Hint below.

![Unit Test Meme](/images/unit.png)

_Credits: TheJenkinsComic_, [ProgrammerHumor.io](https://programmerhumor.io/testing-memes/complex-testing-for-a-simple-code/)

#### Copying Static Files, Single Page and Recursive Page Generation

Originally at this point of the project, I copied the ready-made Cascading Style Sheets in to my project's static folder, along with the picture of J.R.R Tolkien into static/images.

- `copy_static_recursive` **function**: The function itself was built to copy all the contents from static to public folder, first deleting the old contents in destination folder to provide a clean slate. Then with conditional branching determines in source path if it is a file or folder to be copied. If it is a file we copy it from the source path and point it to the destination directory, if it is a directory, the function creates a copy of that directory for the destination path, recursively dives deeper into the directory structure and also checks if those contain additional files or subdirectories.

- `extract_title`: Simple extraction function to grab the first single hash in the markdown text and strip it from its hash and space and returning it. Raises a ValueError if markdown doesn't contain a title or h1 heading.

- **Creation of template.html and the first markdown index file**: At this point I got the ready made boilerplate template.html file copied to root of the project and Tolkien main page index.md copied in to the content directory. The template.html contains placeholders of title and content at important points to make it such, that a title injection later will be giving the browser's tab the name of the injected header title, while content gets injected in between body and article tags of the html template, that the browser then renders.

- `generate_page` **with source, template and destination paths**: This is the base function for page generation. With some helpful developer print messages embedded, it reads the markdown from the source and template paths, stores them as variables. It converts the markdown file into an HTML string using the `markdown_to_html` function and the `.to_html()` method. Then extracts the title with `extract_title` and then replaces the title and content placeholders with generated HTML. Then writes and injects the html into the file at destination path.

_This here was the point where all the countless hours of writing unit tests, proved to be absolutely worth it. Tedious? Absolutely. But like I mentioned way earlier in this post, the necessary evil. No big problems on first pages generation when running a script to run the program on local http server. Only issue was the strictness in block to block type function, forcing a starting space on blockquotes, which in turn crashed the program not giving the necessary tags for quotes due to the mentioned strictness. This was an easy fix, just removed the space._

- After this I took extra markdown documents from course files to give content folder a blog structure, contact section and new images in static folder for each "blog post" on Lord of The Rings.

- **Enter Recursive Page Generation function**: This function takes the source directory content path, template path and destination directory paths, defines full source and full destination paths for each entry. This time if the crawled source path is a directory we recurse deeper in its subdirectories and files and this way create copy of the necessary final destination directory structure. If the pointer is a file we recursively turn the content entries with ".md" prefix into ".html" prefixes using `pathlib.Path` and drive them into the new final directory structure using the original `generate_page` function. This function allows us to generate multiple pages after we point the main.py function to execute it after defining and pointing a `base_path` to "/" for the generating functions, as well as source and destination paths.

> "Speaking of recursion..."

![recursion meme](/images/recursion.gif)

## Day 10

### Publishing to Internet

#### Using Github Pages

- The point of assigning a base path was to have options. The default of `/` is for local testing, but I needed an actual address assigned to it when working with actual domains or, in this project's case, GitHub Pages.

- The path is dynamically assigned by comparing the length of arguments in `sys.argv`. If it is greater than 1, then the CLI argument in my script will be assigned as the base path. For example, running `python3 src/main.py "/github_repo_name/"`.

- I then updated the directory location from "public" to "docs", as GitHub Pages serves its sites from the "docs" directory on the main branch by default.

- I deleted the old "public" directory, rebuilt the site in "docs", and changed "Code and automation" settings on GitHub to configure the publishing source.

- Then the last final `git add .` -> `git commit` -> `git push origin main` for **Project Completion**.

### The Road Ahead

Coming this far, I have yet to decide on where I want this project to go in the future. Obviously, I am redefining it **right now**, making the necessary changes to the Tolkien theme and changing it to become an extension blog for my portfolio website.

One idea could be to change the styling drastically later on, using CSS more strongly on the elements generated by the SSG.

A second idea that was suggested in the course materials was to add support for having multiple inline elements inside each other (e.g., a bold text sentence with an italic text word inside it).

**Some changes are definitely to be expected, just not sure how soon though.**

### Conclusion

Funnily enough, after the initial project completion, I was feeling a bit lost at times. However, I noticed that going over the project in this "post diary" format and rewriting this page's own markdown for my personal blog made things click. Concepts that were a bit foggy earlier suddenly made much more sense when reflecting on the build process and data flow as a whole.

While this project was definitely one of the hardest so far—even compared to building the AI Agent using the Gemini API a few weeks earlier—this is only the beginning. After this project's completion, a course on memory management in C is the only thing standing between me and the mid-point of the entire boot.dev curriculum. 

This mid-point culminates into a full-on unguided Personal Project. The goal is to bring all the things learned into a portfolio-grade project with independent effort.

For me, the main issue will probably be coming up with the idea for it, but once that is set in stone, I doubt that the technical implementation will be *that* hard.

I could also end up eating my words on that previous sentence, guess we'll see.

**But for now, onwards to C and some memory management.**

[< Back Home](/)