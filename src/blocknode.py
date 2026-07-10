from enum import Enum

class BlockType(Enum):
    PARAGRAPH      = "paragraph"
    HEADING        = "heading"
    CODE           = "code"
    QUOTE          = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST   = "ordered list"

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    blocks = list(filter(lambda s: s.strip() != '', blocks))
    blocks = list(   map(lambda s: s.strip(),       blocks))
    return blocks

def block_to_block_type(block: str) -> BlockType:
    pass

