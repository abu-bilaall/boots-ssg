import sys
from src_to_dest import src_to_dest
from generate_page import generate_pages_recursive

def main():
    src_to_dest("./static", "./docs")
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    generate_pages_recursive("./content", "./template.html", "./docs", basepath)

if __name__ == "__main__":
    main()