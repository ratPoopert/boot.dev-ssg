from enum import Enum


class TextType(Enum):
    NORMAL = "Normal Text"
    BOLD = "Bold Text"
    ITALIC = "Italic Text"
    CODE = "Inline Code"
    LINK = "Link"
    IMAGE = "Inline Image"


class BlockType(Enum):
    PARAGRAPH = "Paragraph Block"
    HEADING = "Heading Block"
    CODE = "Code Block"
    QUOTE = "Quote Block"
    UNORDERED_LIST = "Unordered List"
    ORDERED_LIST = "Ordered List"
