from textnode import TextNode, TextType

def main():
    dummy_node = TextNode("This is some anchor text", TextType.LINK_TEXT, "https://www.boot.dev")
    print(dummy_node) # TextNode(This is some anchor text, link, https://www.boot.dev)

main()