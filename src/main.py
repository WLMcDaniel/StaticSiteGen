from textnode import TextNode, TextType

def main():
    node = TextNode("hello test", TextType.LINK, "https://I'mbadatthis.com")
    print(node)

main()