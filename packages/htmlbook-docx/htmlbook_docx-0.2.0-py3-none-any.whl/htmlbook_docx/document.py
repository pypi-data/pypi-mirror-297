import logging
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Tag
from docx import Document
from docx.shared import Inches

from htmlbook_docx.elements import process_tag
from htmlbook_docx.styles import apply_manuscript_defaults


def docx_from_htmlbook(fn: Path, out_fn: Path):
    """
    Generates a docx from an htmlbook file
    """
    assert fn.suffix == ".html"

    doc = Document()
    # styles and layout
    apply_manuscript_defaults(doc)

    with open(fn, "rt") as f:
        soup = BeautifulSoup(f, "lxml")

    sections = soup.find_all("section")

    for section in sections:
        for element in section.contents:
            match element:
                case NavigableString():
                    # my understanding is that these are just
                    # blank line strings
                    if not str(element).strip() == "":
                        logging.warning(f"Unexpected skip: {element}")
                    else:
                        pass
                case Tag():
                    process_tag(doc, element)

    for s in doc.sections:
        s.left_margin = Inches(1)
        s.right_margin = Inches(1)
        s.top_margin = Inches(1)
        s.bottom_margin = Inches(1)

    doc.save(str(out_fn))
