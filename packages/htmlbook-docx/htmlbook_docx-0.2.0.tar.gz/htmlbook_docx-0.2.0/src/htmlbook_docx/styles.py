from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Pt, Inches
from docx.styles.style import ParagraphStyle, CharacterStyle
from docx.enum.style import WD_STYLE_TYPE


def apply_manuscript_defaults(doc: Document):
    doc_styles = doc.styles


    # "normal"
    normal: ParagraphStyle = doc_styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(12)
    normal.paragraph_format.widow_control = True
    normal.paragraph_format.line_spacing = 2.0
    normal.paragraph_format.first_line_indent = Inches(0.5)
    normal.paragraph_format.space_after = Pt(0)
    normal.paragraph_format.space_before = Pt(0)

    # Heading
    heading: ParagraphStyle = doc_styles["Heading1"]
    heading.base_style = normal
    heading.font.name = "Times New Roman"
    heading.font.size = Pt(12)
    heading.font.bold = True
    heading.paragraph_format.line_spacing = 2.0
    heading.paragraph_format.first_line_indent = Inches(0)

    # playintro
    playintro: ParagraphStyle = doc_styles.add_style(
        "playintro", WD_STYLE_TYPE.PARAGRAPH
    )
    playintro.base_style = doc_styles["Normal"]
    playintro.font.italic = True

    # instruction
    instruction: ParagraphStyle = doc_styles.add_style(
        "instruction", WD_STYLE_TYPE.PARAGRAPH
    )
    instruction.base_style = doc_styles["Normal"]
    instruction.font.italic = True
    fmt = instruction.paragraph_format
    fmt.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
    fmt.left_indent = Inches(0.25)
    fmt.right_indent = Inches(0.25)
    fmt.first_line_indent = Inches(0)
    fmt.space_before = Pt(18)
    fmt.space_after = Pt(18)

    # aside
    aside: ParagraphStyle = doc_styles.add_style(
        "aside", WD_STYLE_TYPE.PARAGRAPH
    )
    aside.base_style = doc_styles["Normal"]
    aside.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
    aside.paragraph_format.left_indent = Inches(0.25)
    aside.paragraph_format.right_indent = Inches(0.25)
    aside.paragraph_format.first_line_indent = Pt(0.5)

    playspace: ParagraphStyle = doc_styles.add_style(
        "playspace", WD_STYLE_TYPE.PARAGRAPH
    )
    playspace.base_style = doc_styles["Normal"]
    playspace.paragraph_format.space_before = Pt(18)
    playspace.paragraph_format.space_after = Pt(18)

    # "no-indent",
    noindent: ParagraphStyle = doc_styles.add_style(
        "noindent", WD_STYLE_TYPE.PARAGRAPH
    )
    noindent.base_style = doc_styles["Normal"]
    noindent.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
    noindent.paragraph_format.left_indent = Inches(0)
    noindent.paragraph_format.first_line_indent = Inches(0)

    # collages
    for group in [1, 5, 9]:
        collage_group: ParagraphStyle = doc_styles.add_style(
            f"collagegroup{group}", WD_STYLE_TYPE.PARAGRAPH
        )
        collage_group.base_style = doc_styles["Normal"]
        collage_group.paragraph_format.left_indent = Inches(0.25)

    for group in [2, 6, 10]:
        collage_group: ParagraphStyle = doc_styles.add_style(
            f"collagegroup{group}", WD_STYLE_TYPE.PARAGRAPH
        )
        collage_group.base_style = doc_styles["Normal"]
        collage_group.paragraph_format.left_indent = Inches(0.5)

    for group in [3, 7, 11]:
        collage_group: ParagraphStyle = doc_styles.add_style(
            f"collagegroup{group}", WD_STYLE_TYPE.PARAGRAPH
        )
        collage_group.base_style = doc_styles["Normal"]
        collage_group.paragraph_format.left_indent = Inches(0.75)

    for group in [4, 8, 12]:
        collage_group: ParagraphStyle = doc_styles.add_style(
            f"collagegroup{group}", WD_STYLE_TYPE.PARAGRAPH
        )
        collage_group.base_style = doc_styles["Normal"]
        collage_group.paragraph_format.left_indent = Inches(1)

    for style in doc_styles:
        style.next_paragraph_style = normal

    # CHARACTER STYLES

    # inlineinstruction
    inlineinstruction: CharacterStyle = doc_styles.add_style(
        "inlineinstruction", WD_STYLE_TYPE.CHARACTER
    )
    inlineinstruction.font.italic = True

    # text-texts
    textmsg: CharacterStyle = doc_styles.add_style(
        "textmsg", WD_STYLE_TYPE.CHARACTER
    )
    textmsg.font.small_caps = True
