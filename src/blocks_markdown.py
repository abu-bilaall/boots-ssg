import re
from enum import Enum
from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block:
            filtered_blocks.append(stripped_block)
    return filtered_blocks


def block_to_block_type(block):
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING

    lines = block.split("\n")

    if all(re.match(r"^> ?", line) for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    ordered_match = True
    for i, line in enumerate(lines, start=1):
        if not re.match(rf"^{i}\. ", line):
            ordered_match = False
            break
    if ordered_match:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


# helper functions for markdown_to_html
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.CODE:
            node = LeafNode(tag="code", value=text_node.text)
            return node


def get_heading_level_and_text(block: str) -> tuple[int, str] | tuple[None, None]:
    match = re.match(r"\s*(#{1,6})\s+(.*)", block)
    if not match:
        return None, None
    length = len(match.group(1))
    text = match.group(2)
    return length, text


def format_quote_text(block: str) -> str:
    lines = block.strip().split("\n")
    quote_lines = []

    for line in lines:
        match = re.match(r"^\s*>\s*(.*)", line)
        if match:
            quote_lines.append(match.group(1))

        quote_text = "\n".join(quote_lines)
    
    return quote_text


def format_html_list_items(block: str, list_type: str) -> list:
    lines = block.strip().split("\n")
    list_nodes = []

    for line in lines:
        if list_type == "ol":
            match = re.match(r"^\s*\d+\.\s*(.*)", line)
        else:
            match = re.match(r"^\s*-\s*(.*)", line)
        if match:
            value = match.group(1).rstrip()
            text_nodes = text_to_textnodes(value)
            li_value = format_inline_nodes(text_nodes)
            list_nodes.append(LeafNode(tag="li", value=li_value))

    return list_nodes


def format_inline_nodes(text_nodes: list) -> str:
    html_nodes = []
    for node in text_nodes:
        match node.text_type:
            case TextType.BOLD:
                b = LeafNode(tag="b", value=node.text)
                html_nodes.append(b.to_html())
            case TextType.ITALIC:
                em = LeafNode(tag="i", value=node.text)
                html_nodes.append(em.to_html())
            case TextType.CODE:
                code = LeafNode(tag="code", value=node.text)
                html_nodes.append(code.to_html())
            case TextType.LINK:
                a = LeafNode(tag="a", value=node.text, props={"href": node.url})
                html_nodes.append(a.to_html())
            case TextType.ALT:
                img = LeafNode(
                    tag="img", value="", props={"src": node.url, "alt": node.text}
                )
                html_nodes.append(img.to_html())
            case _:
                text = LeafNode(tag=None, value=node.text)
                html_nodes.append(text.to_html())

    return "".join(html_nodes)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.CODE:
                # a <code> tag nested inside a <pre> tag
                match = re.search(r"```(.*?)```", block, re.DOTALL)
                text = match.group(1).lstrip("\n") if match else None
                text_node = TextNode(text, TextType.CODE)
                code_node = text_node_to_html_node(text_node)
                pre_node = ParentNode(tag="pre", children=[code_node])
                block_nodes.append(pre_node)

            case BlockType.HEADING:
                # <h1> to <h6> tag, depending on the number of # characters.
                level, text = get_heading_level_and_text(block)
                heading_node = LeafNode(tag=f"h{level}", value=text)
                block_nodes.append(heading_node)

            case BlockType.QUOTE:
                quote_text = format_quote_text(block)
                blockquote = LeafNode(tag="blockquote", value=quote_text)
                block_nodes.append(blockquote)

            case BlockType.UNORDERED_LIST:
                # a <ul> parent tag, and each list item should be surrounded by a <li> tag.
                list_items = format_html_list_items(block, "ul")
                ul = ParentNode(tag="ul", children=list_items)
                block_nodes.append(ul)

            case BlockType.ORDERED_LIST:
                # a <ol> parent tag, and each list item should be surrounded by a <li> tag.
                list_items = format_html_list_items(block, "ol")
                ol = ParentNode(tag="ol", children=list_items)
                block_nodes.append(ol)

            case _:
                # <p> tag. I removed the newlines and replaced them with spaces.
                p_text = block.strip().replace("\n", " ")
                text_nodes = text_to_textnodes(p_text)
                p_value = format_inline_nodes(text_nodes)
                p_node = LeafNode(tag="p", value=p_value)
                block_nodes.append(p_node)

    if block_nodes:
        return ParentNode(tag="div", children=block_nodes)
    else:
        return LeafNode(tag="div", value="")
