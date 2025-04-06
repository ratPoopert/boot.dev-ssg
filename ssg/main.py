from pathlib import Path

from ssg.extractors import extract_title
from ssg.converters import markdown_to_html_node

PROJECT_DIR = Path(__file__).parent.parent
CONTENT_DIR = PROJECT_DIR/"content"
TEMPLATE = PROJECT_DIR/"ssg"/"template.html"
DEST_DIR = PROJECT_DIR/"public"


def main():
    generate_pages_recursive(CONTENT_DIR, TEMPLATE, DEST_DIR)


def generate_pages_recursive(dir_path_content,
                             template_path,
                             dest_dir_path):
    markdown_files = CONTENT_DIR.glob("**/*.md")
    for file in markdown_files:
        dest_str = str(file).replace(str(CONTENT_DIR), str(DEST_DIR))
        dest_path = Path(dest_str).with_suffix(".html")
        generate_page(file, TEMPLATE, dest_path)


def generate_page(from_path: Path, template_path: Path, dest_path: Path) -> None:
    print("Generating page from {} to {} using {}".format(from_path,
                                                          template_path,
                                                          dest_path))
    markdown = from_path.read_text()
    template = template_path.read_text()
    title = extract_title(markdown)
    content = markdown_to_html_node(markdown).to_html()

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    output = (template
              .replace("{{ Title }}", title)
              .replace("{{ Content }}", content))
    dest_path.write_text(output)


if __name__ == "__main__":
    main()
