from textnode import TextType, TextNode

def main():

    new_node = TextNode("This is some text", TextType.LINK_TEXT, "https://www.boot.dev")
    print(new_node)

    print(TextNode.__repr__)

if __name__ == "__main__":
    main()