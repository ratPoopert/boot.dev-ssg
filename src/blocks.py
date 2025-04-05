import enum


class BlockType(enum.Enum):
    PARAGRAPH = "Paragraph Block"
    HEADING = "Heading Block"
    CODE = "Code Block"
    QUOTE = "Quote Block"
    UNORDERED_LIST = "Unordered List"
    ORDERED_LIST = "Ordered List"
