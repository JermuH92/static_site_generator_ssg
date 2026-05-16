from textnode import TextType, TextNode
from htmlnode import HTMLNode

def main():

    new_node = TextNode("This is some text", TextType.LINK_TEXT, "https://www.boot.dev")
    print(new_node)


if __name__ == "__main__":
    main()