import re
import os
from blocks_markdown import markdown_to_html_node

def extract_title(markdown):
    match = re.search(r'^\s*#\s+(.*)$', markdown, re.MULTILINE)
    if not match:
        raise ValueError("Title is missing.")
    
    return match.group(1).strip()

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    from_path = os.path.abspath(from_path)
    dest_path = os.path.abspath(dest_path)
    template_path = os.path.abspath(template_path)
    
    # read the markdown
    try:
        with open(from_path, "r") as f:
            markdown = f.read()
    except Exception as e:
        raise RuntimeError(f"Failed to read markdown file: {e}")
    
    # read the template file
    try:
        with open(template_path, "r") as f:
            template = f.read()
    except Exception as e:
        raise RuntimeError(f"Failed to read template file: {e}")
    
    # convert markdown to html
    html_string = markdown_to_html_node(markdown).to_html()

    # extract title
    title = extract_title(markdown)

    # replace placeholders
    template = template.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", html_string)
    page = page.replace("href=\"/", f"href=\"{basepath}")
    page = page.replace("src=\"/", f"src=\"{basepath}")

    # ensure dest. dir exists
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    # write html to dest. file
    with open(dest_path, "w") as f:
        f.write(template)

def generate_pages_recursive(content_dir_path, template_path, dest_dir_path, basepath):
    print(f"Generating pages from {content_dir_path} to {dest_dir_path}")

    content_dir_path = os.path.abspath(content_dir_path)
    template_path = os.path.abspath(template_path)
    dest_dir_path = os.path.abspath(dest_dir_path)

    # ensure destination directory exists
    os.makedirs(dest_dir_path, exist_ok=True)

    # load template
    try:
        with open(template_path, "r") as f:
            template = f.read()
    except Exception as e:
        raise RuntimeError(f"Failed to read template file: {e}")

    for entry in os.listdir(content_dir_path):
        content_path = os.path.join(content_dir_path, entry)
        dest_path = os.path.join(dest_dir_path, entry)

        # recurse into subdirectories
        if os.path.isdir(content_path):
            generate_pages_recursive(content_path, template_path, dest_path, basepath)

        # process markdown files
        elif entry.endswith(".md"):
            try:
                with open(content_path, "r") as f:
                    markdown = f.read()
            except Exception as e:
                raise RuntimeError(f"Failed to read markdown file: {e}")

            title = extract_title(markdown)
            html_content = markdown_to_html_node(markdown).to_html()

            page = template.replace("{{ Title }}", title)
            page = page.replace("{{ Content }}", html_content)
            page = page.replace("href=\"/", f"href=\"{basepath}")
            page = page.replace("src=\"/", f"src=\"{basepath}")

            html_filename = entry.replace(".md", ".html")
            html_path = os.path.join(dest_dir_path, html_filename)

            with open(html_path, "w") as f:
                f.write(page)
        
        else:
            continue