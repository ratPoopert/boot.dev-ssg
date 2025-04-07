import sys
from pathlib import Path

from ssg.extractors import extract_title
from ssg.converters import markdown_to_html_node

PROJECT_DIR = Path(__file__).parent.parent
CONTENT_DIR = PROJECT_DIR/"content"
TEMPLATE = PROJECT_DIR/"ssg"/"template.html"
DEST_DIR = PROJECT_DIR/"docs"


def main():
    basepath = "/" if len(sys.argv) < 2 else sys.argv[1]
    generate_pages_recursive(CONTENT_DIR, TEMPLATE, DEST_DIR, basepath)


def generate_pages_recursive(dir_path_content,
                             template_path,
                             dest_dir_path,
                             basepath: str):
    markdown_files = dir_path_content.glob("**/*.md")
    for file in markdown_files:
        dest_str = str(file).replace(str(dir_path_content), str(dest_dir_path))
        dest_path = Path(dest_str).with_suffix(".html")
        generate_page(file, TEMPLATE, dest_path, basepath)


def generate_page(from_path: Path,
                  template_path: Path,
                  dest_path: Path,
                  basepath: str) -> None:
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
              .replace("{{ Content }}", content)
              .replace('href="/', f'href="{basepath}')
              .replace('src="/', f'src="{basepath}'))
    dest_path.write_text(output)


if __name__ == "__main__":
    main()
