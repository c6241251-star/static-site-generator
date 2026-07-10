import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        if node.text.count(delimiter) % 2 != 0:
            raise Exception(f"closing {delimiter} not found, invalid markdown")
        
        texts = node.text.split(delimiter)
        if len(texts) == 1:
            new_nodes.append(node)
            continue

        for i in range(0, len(texts)):
            if texts[i].strip() == "":
                continue

            if i % 2 == 1:
                new_nodes.append(TextNode(texts[i], text_type))
            else:
                new_nodes.append(TextNode(texts[i], TextType.TEXT))

    return new_nodes


def extract_markdown_images(text: str) -> tuple[str, str]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str) -> tuple[str, str]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        
        text = node.text
        i = 0
        for (alt, src) in images:
            i += 1
            image_md = f"![{alt}]({src})"
            prev_text, text = text.split(image_md, 1)
            if prev_text != '':
                new_nodes.append(TextNode(prev_text, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, src))
            if i == len(images) and text != '':
                new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        
        text = node.text
        i = 0
        for (title, url) in links:
            i += 1
            link_md = f"[{title}]({url})"
            prev_text, text = text.split(link_md, 1)
            if prev_text != '':
                new_nodes.append(TextNode(prev_text, TextType.TEXT))
            new_nodes.append(TextNode(title, TextType.LINK, url))
            if i == len(links) and text != '':
                new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = split_nodes_link([TextNode(text, TextType.TEXT)])
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    return nodes
