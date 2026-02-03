import re
from enum import Enum

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
    if block.startswith("```\n") and block.endswith("```"):
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
