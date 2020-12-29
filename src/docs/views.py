from django.http import Http404
from django.shortcuts import render
import pathlib
import markdown
from django.utils.safestring import mark_safe

from docs.md_processors.bootstrap import BootstrapExtension
from docs.md_processors.hints import HintExtension
from docs.md_processors.remove_md_links_extension import MdLinksExtension

MARKDOWN_FILES = pathlib.Path(__file__).parent.absolute() / "markdown_files/"


# Create your views here.
def index(request):
    return display_page(request, category=None, page="README")


def category_index(request, category):
    return display_page(request, category=category, page="INDEX")


def display_page(request, page, category=None):
    if category:
        file = f"{category}/{page}.md"
    else:
        file = f"{page}.md"

    gh_file = "https://github.com/DuckHunt-discord/duckhunt.me-docs/blob/master/" + file

    file = MARKDOWN_FILES / file

    if not file.exists():
        raise Http404("This page does not exist in the documentation. Can you create it ?")

    with open(file, "r") as f:
        markdown_text = f.read()

    parsed = markdown.markdown(markdown_text,
                               extensions=['tables',
                                           'fenced_code',
                                           HintExtension(),
                                           BootstrapExtension(),
                                           MdLinksExtension()]
                               )

    return render(request, "docs/index.jinja2", {"page": page, "category": category, "file": file,
                                                 "parsed_content": mark_safe(parsed), "gh_file": gh_file})
