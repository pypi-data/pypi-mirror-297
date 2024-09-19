from pathlib import Path
from typing import Optional
import typer
from typing_extensions import Annotated

from .document import docx_from_htmlbook


def convert(
    file: Annotated[str, typer.Argument(help="Htmlbook file to be converted")],
    output: Annotated[Optional[str], typer.Argument()] = None,
):
    """
    Takes an htmlbook FILE and creates a docx, with an optional
    output filename.
    """
    fp = Path(file)
    assert fp.is_file()
    assert fp.suffix == ".html"

    if output:
        out_fn = Path(output)
    else:
        out_fn = Path(fp.stem + ".docx")

    docx_from_htmlbook(fp, out_fn)

def main():
    typer.run(convert)
