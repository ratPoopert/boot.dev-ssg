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


def extract_title(markdown: str) -> str:
    if not isinstance(markdown, str):
        raise TypeError("markdown must be a string.")
    lines = markdown.split("\n")
    h1_lines = list(map(
        lambda line: line.split(" ", maxsplit=1)[1],
        filter(lambda line: line.startswith("# "), lines)
    ))
    if len(h1_lines) != 1:
        raise ValueError("markdown must contain exactly 1 level one heading.")
    return h1_lines[0]
