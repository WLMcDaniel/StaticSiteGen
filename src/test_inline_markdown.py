import re
import unittest
from inline_markdown import *
from textnode import TextNode, TextType

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "   This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
        "   This is text with an [link](https://www.boot.dev/dashboard)"
        )
        self.assertListEqual([("link", "https://www.boot.dev/dashboard")], matches)

    def test_extract_multiple_markdown_links(self):
        text = "Link 1 [regexr](https://regexr.com/) and link 2 [to boot dev](https://www.boot.dev/dashboard)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("regexr","https://regexr.com/"),("to boot dev","https://www.boot.dev/dashboard")], matches)

    def test_extract_multiple_markdown_images(self):
        text = "Link 1 ![image](https://www.google.com/imgres?q=boot%20dev%20bear&imgurl=https%3A%2F%2Fwww.boot.dev%2F_nuxt%2Fnew_boots_profile.DriFHGho.webp&imgrefurl=https%3A%2F%2Fwww.boot.dev%2F&docid=5mYIXY0RchQQPM&tbnid=hOoZorls3nP7VM&vet=12ahUKEwj_-tOK3t2WAxWpSjABHU-BC2EQnPAOegQIPRAA..i&w=250&h=250&hcb=2&ved=2ahUKEwj_-tOK3t2WAxWpSjABHU-BC2EQnPAOegQIPRAA) and link 2 ![image](https://www.google.com/imgres?q=images&imgurl=https%3A%2F%2Fimages.unsplash.com%2Fphoto-1526779259212-939e64788e3c%3Ffm%3Djpg%26q%3D60%26w%3D3000%26auto%3Dformat%26fit%3Dcrop%26ixlib%3Drb-4.1.0%26ixid%3DM3wxMjA3fDB8MHxzZWFyY2h8M3x8ZnJlZSUyMGltYWdlc3xlbnwwfHwwfHx8MA%253D%253D&imgrefurl=https%3A%2F%2Funsplash.com%2Fs%2Fphotos%2Ffree-images&docid=rSJymaiqlIbilM&tbnid=salFp-bzk6qAVM&vet=12ahUKEwi-zPWl3t2WAxUlSzABHQ_kLUEQnPAOegQISxAA..i&w=3000&h=1993&hcb=2&ved=2ahUKEwi-zPWl3t2WAxUlSzABHQ_kLUEQnPAOegQISxAA)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image","https://www.google.com/imgres?q=boot%20dev%20bear&imgurl=https%3A%2F%2Fwww.boot.dev%2F_nuxt%2Fnew_boots_profile.DriFHGho.webp&imgrefurl=https%3A%2F%2Fwww.boot.dev%2F&docid=5mYIXY0RchQQPM&tbnid=hOoZorls3nP7VM&vet=12ahUKEwj_-tOK3t2WAxWpSjABHU-BC2EQnPAOegQIPRAA..i&w=250&h=250&hcb=2&ved=2ahUKEwj_-tOK3t2WAxWpSjABHU-BC2EQnPAOegQIPRAA"),("image","https://www.google.com/imgres?q=images&imgurl=https%3A%2F%2Fimages.unsplash.com%2Fphoto-1526779259212-939e64788e3c%3Ffm%3Djpg%26q%3D60%26w%3D3000%26auto%3Dformat%26fit%3Dcrop%26ixlib%3Drb-4.1.0%26ixid%3DM3wxMjA3fDB8MHxzZWFyY2h8M3x8ZnJlZSUyMGltYWdlc3xlbnwwfHwwfHx8MA%253D%253D&imgrefurl=https%3A%2F%2Funsplash.com%2Fs%2Fphotos%2Ffree-images&docid=rSJymaiqlIbilM&tbnid=salFp-bzk6qAVM&vet=12ahUKEwi-zPWl3t2WAxUlSzABHQ_kLUEQnPAOegQISxAA..i&w=3000&h=1993&hcb=2&ved=2ahUKEwi-zPWl3t2WAxUlSzABHQ_kLUEQnPAOegQISxAA")], matches)

    def test_no_links(self):
        text = "The quick brown fox jumped over the lazy dog"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_no_images(self):
        text = "I hate writing unittests"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://regexr.com/) and another [second link](https://www.boot.dev/dashboard)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://regexr.com/"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://www.boot.dev/dashboard"),
            ],
            new_nodes,
        )    


if __name__ == "__main__": unittest.main()