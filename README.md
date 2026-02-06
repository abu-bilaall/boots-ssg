# Boots SSG

A lightweight, Python-based static site generator that converts Markdown content into HTML pages. Built as a learning project, it demonstrates core SSG concepts with a clean, extensible architecture.

## Features

- **Markdown to HTML Conversion**: Full support for standard Markdown syntax
  - Headings (H1-H6)
  - Bold, italic, and inline code
  - Links and images
  - Code blocks with syntax preservation
  - Ordered and unordered lists
  - Blockquotes
  - Paragraphs with inline formatting

- **Recursive Directory Processing**: Automatically processes nested content directories
- **Template System**: Simple placeholder-based templating
- **Static Asset Copying**: Copies CSS, images, and other static files to output
- **Configurable Base Path**: Support for deployment to subdirectories

## Quick Start

### Prerequisites

- Python 3.10 or higher

### Installation

```bash
git clone https://github.com/abu-bilaall/boots-ssg
cd boots-ssg
```

### Project Structure

```
boots-ssg/
├── content/          # Markdown source files
│   ├── index.md
│   └── blog/
├── static/           # Static assets (CSS, images)
│   ├── index.css
│   └── images/
├── template.html     # HTML template
├── docs/             # Generated output (gitignored)
└── src/              # Source code
    ├── main.py
    ├── generate_page.py
    ├── blocks_markdown.py
    ├── inline_markdown.py
    ├── htmlnode.py
    ├── textnode.py
    └── src_to_dest.py
```

### Usage

**Build the site:**
```bash
./build.sh
```

**Build with custom base path:**
```bash
python3 src/main.py "/custom-path/"
```

**Run tests:**
```bash
./test.sh
```

**Development server:**
```bash
./main.sh
# Serves on http://localhost:8888
```

## How It Works

### 1. Content Processing Pipeline

```
Markdown → TextNodes → HTMLNodes → HTML String
```

1. **Markdown Parsing**: Content is split into blocks (paragraphs, headings, lists, etc.)
2. **Inline Processing**: Each block is parsed for inline elements (bold, links, images)
3. **Node Tree Construction**: Creates an intermediate representation using `TextNode` and `HTMLNode` objects
4. **HTML Generation**: Renders the node tree to HTML strings
5. **Template Injection**: Inserts generated HTML into template placeholders

### 2. Core Components

**`textnode.py`**: Represents inline text with formatting (bold, italic, code, links, images)

**`htmlnode.py`**: HTML element representation with `LeafNode` (no children) and `ParentNode` (with children)

**`inline_markdown.py`**: Parses inline Markdown syntax (bold, italic, code, links, images)

**`blocks_markdown.py`**: Parses block-level Markdown (headings, lists, quotes, code blocks)

**`generate_page.py`**: Orchestrates the conversion process and handles file I/O

**`src_to_dest.py`**: Copies static assets from source to destination

### 3. Template System

Templates use simple placeholder syntax:

```html
<!doctype html>
<html>
  <head>
    <title>{{ Title }}</title>
  </head>
  <body>
    {{ Content }}
  </body>
</html>
```

**Available placeholders:**
- `{{ Title }}`: Extracted from first H1 heading in Markdown
- `{{ Content }}`: Generated HTML content

## Writing Content

### Basic Markdown Example

```markdown
# My Page Title

This is a paragraph with **bold** and _italic_ text.

## Subheading

- List item 1
- List item 2

1. Numbered item
2. Another item

> This is a blockquote

[Link text](https://example.com)

![Alt text](/images/photo.png)

Inline `code` and code blocks:

\`\`\`
def hello():
    print("Hello, world!")
\`\`\`
```

### Content Requirements

- **Every Markdown file must have an H1 heading** (used as page title)
- Images and links use absolute paths from site root (e.g., `/images/photo.png`)
- Code blocks use triple backticks

## Configuration

### Base Path

The base path allows deployment to subdirectories:

```bash
# Deploy to root
python3 src/main.py "/"

# Deploy to subdirectory
python3 src/main.py "/my-site/"
```

This automatically adjusts all `href` and `src` attributes in the generated HTML.

## Testing

The project includes comprehensive unit tests:

```bash
# Run all tests
python3 -m unittest discover -s src

# Run specific test file
python3 -m unittest src.test_inline_markdown
```

**Test coverage includes:**
- Inline Markdown parsing (bold, italic, code, links, images)
- Block Markdown parsing (headings, lists, quotes, code blocks)
- HTML node generation
- Text node transformations

## Extending Boots SSG

### Roadmap to Hugo-Level Features

To evolve this into a production-ready SSG like Hugo, consider implementing:

#### 1. Front Matter Support
```yaml
---
title: "My Post"
date: 2026-02-06
author: "John Doe"
tags: ["python", "ssg"]
draft: false
---
```

**Implementation**: Use `python-frontmatter` or `PyYAML` to parse metadata from Markdown files.

#### 2. Taxonomies & Organization
- **Tags and Categories**: Group content by topics
- **Series**: Link related posts together
- **Pagination**: Split long lists across multiple pages

**Implementation**: Build an index of all content with metadata, then generate taxonomy pages.

#### 3. Themes & Layouts
- Multiple layout templates (single, list, homepage)
- Partial templates (header, footer, navigation)
- Template inheritance
- Custom shortcodes

**Implementation**: Use Jinja2 or Mako for advanced templating with inheritance and includes.

#### 4. Asset Pipeline
- SASS/SCSS compilation
- JavaScript bundling and minification
- Image optimization and responsive images
- CSS/JS fingerprinting for cache busting

**Implementation**: Integrate `libsass`, `esbuild`, or `Pillow` for asset processing.

#### 5. Content Types
- Blog posts with dates and authors
- Documentation with navigation trees
- Landing pages with custom layouts
- Data-driven pages (JSON/YAML/CSV)

**Implementation**: Define content type schemas and custom rendering logic per type.

#### 6. Advanced Markdown
- Tables
- Footnotes
- Task lists
- Strikethrough
- Definition lists
- Math equations (LaTeX)
- Mermaid diagrams

**Implementation**: Switch to `python-markdown` with extensions or `mistune` with plugins.

#### 7. Performance Optimizations
- **Incremental builds**: Only rebuild changed files
- **Parallel processing**: Use multiprocessing for large sites
- **Caching**: Cache parsed Markdown and rendered HTML
- **Watch mode**: Auto-rebuild on file changes

**Implementation**: Track file modification times, use `multiprocessing.Pool`, implement a cache layer.

#### 8. Developer Experience
- Live reload development server
- Syntax highlighting for code blocks
- Better error messages with line numbers
- Configuration file (YAML/TOML)
- CLI with subcommands (`build`, `serve`, `new`)

**Implementation**: Use `watchdog` for file watching, `Pygments` for syntax highlighting, `click` or `typer` for CLI.

#### 9. SEO & Web Standards
- Sitemap generation
- RSS/Atom feeds
- robots.txt generation
- Open Graph and Twitter Card meta tags
- Canonical URLs
- Schema.org structured data

**Implementation**: Generate XML sitemaps and RSS feeds from content index.

#### 10. Deployment & Hosting
- GitHub Pages support
- Netlify/Vercel configuration
- S3/CloudFront deployment scripts
- Docker containerization

**Implementation**: Add deployment scripts and CI/CD configuration files.

#### 11. Plugin System
```python
# Example plugin architecture
class Plugin:
    def on_content_parsed(self, content):
        pass
    
    def on_html_generated(self, html):
        pass
    
    def on_build_complete(self):
        pass
```

**Implementation**: Define plugin hooks at key points in the build process, load plugins from a config file.

#### 12. Internationalization (i18n)
- Multi-language content
- Language-specific URLs
- Translation management
- RTL language support

**Implementation**: Organize content by language code, generate separate output directories per language.

#### 13. Search Functionality
- Client-side search with JSON index
- Full-text search
- Tag-based filtering

**Implementation**: Generate a search index JSON file, integrate with Lunr.js or Fuse.js.

#### 14. Content Management
- Draft posts (excluded from builds)
- Scheduled publishing (future dates)
- Content expiration
- Related posts suggestions

**Implementation**: Filter content based on metadata during build, implement similarity algorithms for related posts.

#### 15. Analytics & Monitoring
- Build time reporting
- Broken link detection
- Image optimization suggestions
- Bundle size analysis

**Implementation**: Add validation passes during build, generate reports.

## Architecture Improvements

### Recommended Refactoring

1. **Separate Parsing from Rendering**
   ```python
   # Parser returns AST
   ast = MarkdownParser().parse(markdown)
   
   # Renderer converts AST to HTML
   html = HTMLRenderer().render(ast)
   ```

2. **Configuration Management**
   ```python
   # config.yaml
   site:
     title: "My Site"
     baseURL: "https://example.com"
     language: "en"
   
   build:
     output: "docs"
     drafts: false
   ```

3. **Plugin System**
   ```python
   # plugins/syntax_highlight.py
   class SyntaxHighlightPlugin(Plugin):
       def on_code_block(self, code, language):
           return pygments.highlight(code, language)
   ```

4. **Content Model**
   ```python
   @dataclass
   class Page:
       title: str
       content: str
       metadata: dict
       path: Path
       url: str
       date: datetime
   ```

5. **Template Engine Integration**
   ```python
   from jinja2 import Environment, FileSystemLoader
   
   env = Environment(loader=FileSystemLoader('themes'))
   template = env.get_template('single.html')
   html = template.render(page=page, site=site)
   ```

## Known Issues

1. **Bug in `generate_page.py`**: Variable `page` is undefined (should be `template`)
2. **No HTML escaping**: User content could contain malicious HTML
3. **No error recovery**: Parser errors crash the entire build
4. **Limited Markdown support**: Missing tables, footnotes, strikethrough
5. **No incremental builds**: Rebuilds everything on every run

## Contributing

This is a learning project, but contributions are welcome! Areas for improvement:

- Fix known bugs
- Add missing Markdown features
- Improve error handling
- Add integration tests
- Implement configuration system
- Add front matter support

## License

[Add your license here]

## Acknowledgments

Built as part of the [Boot.dev](https://www.boot.dev) Static Site Generator course.

## Resources

- [CommonMark Spec](https://commonmark.org/)
- [Hugo Documentation](https://gohugo.io/documentation/)
- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [Python Markdown Libraries](https://github.com/Python-Markdown/markdown)
