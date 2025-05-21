# Recommended Tools 🤝

## The Basics
1. ON Windows? Use [wsl2](https://learn.microsoft.com/en-us/windows/wsl/about) for development.
2. Use [markdown](https://www.markdownguide.org/) for ALL your writing. It supports images, formulas, tables, etc. There is no excuse for using .docx, .pdf, etc...
3. Use [git](https://git-scm.com/), or make your life very, very hard.
   1. Learn Git (from complete beginner to intermediate)
      1. https://rogerdudler.github.io/git-guide/
      2. https://ohshitgit.com/
      3. https://www.git-tower.com/blog/workflow-of-git/
      4. https://ndpsoftware.com/git-cheatsheet.html
      5. https://learngitbranching.js.org/
      6. https://dev.to/godcrampy/git-cheat-sheet-infographic-pdf-1bj4
      7. https://marklodato.github.io/visual-git-guide/index-en.html
      8. https://salferrarello.com/intermediate-git/
4. Use a [clipboard manager](https://en.wikipedia.org/wiki/Clipboard_manager) like:
    - Windows: https://github.com/sabrogden/Ditto
    - Windows, Linux, OSX: https://github.com/hluk/CopyQ
 

## Gather Context

### What format?
- use Markdown format: https://www.markdownguide.org/ LLMs understand it best. Markdown supports math formulas, tables, etc.
- use mermain diagrams: https://mermaid.js.org/

### How large can the context be?
- Theoretically pretty large. Gemini 1.5 Pro allows for 1M context window (this is larger than "War and Peace" by Tolstoy ~0.7M tokens).
- Try to keep it as small and specific to the task as possible.

### How to add information to context?
> How to get the context information from websites, pdfs, journals, multiple local files and folders etc...?
- copy paste what you can copy paste. Pay attention to how the information is being pasted: the indentation might be off, or there might be artifacts which might throw the LLM off.
- use tools to merge the contents of whole github repos into a single markdown file:
  - https://github.com/travisvn/gptree | https://gptree.dev/
  - https://github.com/cyclotruc/gitingest | https://gitingest.com/
  - https://github.com/yamadashy/repomix | https://repomix.com/ 

- use scripts like `scripts/dir_ingest.py` and `scripts/urls_ingest.py` to merge the content of all files in a directory or download the content of a list of urls into a single markdown file.
- use tools to convert pdfs and urls to markdown:
    - https://jina.ai/reader/ (free tier, no signup)
    - https://cloud.llamaindex.ai/ (free tier, signup)
    - https://www.firecrawl.dev/ (free tier, signup)
    - Crawl4AI: Open-source LLM Friendly Web Crawler & Scraper (python library): https://github.com/unclecode/crawl4ai
    - Docling (convert PDF, DOCX, XLSX, HTML, images, and more): https://github.com/docling-project/docling
    - Marker (supports complex layouts, tables, formulas) (python library): https://github.com/VikParuchuri/marker
- use https://gitdiagram.com to draw a component diagram of any github repo. For example landlab: https://gitdiagram.com/landlab/landlab. Use this tool to generate mermaid diagrams that can be added to the context to improve understanding of large codebases.

## Experimental Tools

### Project Planning (Task Splitting) Tools for AI IDEs
1. https://www.task-master.dev/
2. https://github.com/vanzan01/cursor-memory-bank