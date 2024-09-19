# Htmlbook to Docx

A very opinionated [htmlbook](https://oreillymedia.github.io/HTMLBook/) to docx
converter, providing formatting that is similar to what a "manuscript"
submission docx should look like.

This should work for most "run of the mill" prose documents.

## Why Htmlbook?

For one thing, there are [asciidoctor templates](https://github.com/oreillymedia/asciidoctor-htmlbook)
for it, but beyond that, compared to many "book-like" HTML outputs, it's
relatively clean in terms of its HTML markup. This makes processing into docx
both simpler and more reliable.

## Installation and Usage

This tool can be installed via pip:

```
pip install htmlbook-docx
```

Then, to convert a given HTML file, simply run:

```
htmlbook2docx FILE
```

## Contributing

I used this as a pilot project for trying [`uv`](https://github.com/astral-sh/uv)
over `poetry`, so:

1. Install [`uv`](https://docs.astral.sh/uv) (links to docs)
1. Clone the repo
1. Run `uv sync`, which will create the virtual environment and get the packages
   going.
1. Hack away.

## Quirks

Some quirks to keep in mind:

* `<code>` tags are rendered in small caps; this is an accidental feature of the
project I wrote this tool to solve for.
* There are a bunch of idiosyncratic styles included in the defaults; feel free
to use them, but mostly they are for the aforementioned project and can be
safely ignored.
* If you have styles (classes) on your paragraphs that aren't present in
`apply_manuscript_defaults`, the build will fail. Someday, maybe, I'll make that
pluggable.
* While there is handling for definition lists, there is not currently handling
for ordered or unordered lists. If these are present, instead of silently
failing, the script should log the error to the terminal. This should be true
for any "missed content."

## To Do

Things yet to do:

* Handle more or all expected htmlbook tags
* Better style handling for unexpected classes
* User-provided styling for various classes (or better: create an "empty" style
on-the-fly that the user can then modify inside Word or Libreoffice)
* Actually write tests. Whoops.
