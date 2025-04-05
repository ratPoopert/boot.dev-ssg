import re


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    if not isinstance(text, str):
        raise TypeError("Text must be a string.")
    regexpr = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    result = re.findall(regexpr, text)
    return result


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    if not isinstance(text, str):
        raise TypeError("Text must be a string.")
    regexpr = r"\[([^\[\]]*)\]\(([^\(\)]*)\)"
    result = re.findall(regexpr, text)
    return result
