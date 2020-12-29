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
    summary_file = MARKDOWN_FILES / "SUMMARY.md"

    with open(summary_file, "r") as f:
        parsed_summary = markdown.markdown(f.read(),
                                           extensions=['tables',
                                                       'fenced_code',
                                                       HintExtension(),
                                                       BootstrapExtension(),
                                                       MdLinksExtension()]
                                           )
        parsed_summary = mark_safe(parsed_summary)

    return display_page(request, category=None, page="README", ctx={"parsed_summary": parsed_summary})


def category_index(request, category):
    return display_page(request, category=category, page="INDEX")


def display_page(request, page, category=None, subcategory=None, ctx=None):
    if ctx is None:
        ctx = {}
    if subcategory:
        file = f"{category}/{subcategory}/{page}.md"
    elif category:
        file = f"{category}/{page}.md"
    else:
        file = f"{page}.md"

    gh_file = "https://github.com/DuckHunt-discord/duckhunt.me-docs/blob/master/" + file

    file = MARKDOWN_FILES / file

    if not file.exists():
        raise Http404("This page does not exist in the documentation. Can you create it ?")

    with open(file, "r") as f:
        parsed = markdown.markdown(f.read(),
                                   extensions=['tables',
                                               'fenced_code',
                                               HintExtension(),
                                               BootstrapExtension(),
                                               MdLinksExtension()]
                                   )
        parsed = mark_safe(parsed)

    return render(request, "docs/index.jinja2", {"page": page, "category": category, "file": file,
                                                 "parsed_content": parsed,
                                                 "gh_file": gh_file, **ctx})
