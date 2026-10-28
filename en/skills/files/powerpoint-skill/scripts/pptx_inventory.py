"""List every text-bearing shape of a .pptx so the agent can address it by slide + shape id.

Usage:
  python3 pptx_inventory.py DECK.pptx                 # all slides
  python3 pptx_inventory.py DECK.pptx --slides 2-5,8  # some slides (big decks: stdout is limited)
  python3 pptx_inventory.py DECK.pptx --check         # only report leftover dummy text; exit 2 if any

Output per slide: layout name, then one line per shape:
  id=<shape id> <kind> "<name>" followed by its paragraphs as  [0] text  [1] text ...
Kinds: ph:<type> = real placeholder (layout tools can fill it), box = plain shape/text box,
pic = picture, tbl = table (cells as r<row>c<col>), chart/smartart/ole = graphic frame.
Shapes inside groups are listed with their own id; the group id is shown as  in=<group id>.
Lines marked  !DUMMY  look like sample text (Text, XXX, TITEL, Lorem ...).
"""
import re
import sys

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

DUMMY = re.compile(
    r"^\s*("
    r"x{2,}|text(\s*\d+)?|titel|untertitel|title|subtitle|überschrift|headline|"
    r"abbildung|bild|image|picture|foto|photo|grafik|logo|firmenlogo|"
    r"platzhalter|placeholder|lorem ipsum.*|ipsum.*|"
    r"(klicken|click) .*(bearbeiten|edit|add|hinzuzufügen|einzugeben).*|"
    r"text(masterformat|platzhalter).*|\d{2}\s+titel"
    r")\s*$",
    re.IGNORECASE,
)
DUMMY_ANYWHERE = re.compile(r"x{3,}|lorem ipsum|\[\s*(text|name|datum|date|titel|title)\s*\]", re.IGNORECASE)


def is_dummy(text):
    return bool(text.strip()) and bool(DUMMY.match(text) or DUMMY_ANYWHERE.search(text))


def parse_ranges(spec, count):
    if not spec:
        return list(range(1, count + 1))
    out = []
    for part in spec.split(","):
        a, _, b = part.partition("-")
        out.extend(range(int(a), int(b or a) + 1))
    return [n for n in out if 1 <= n <= count]


def kind_of(shape):
    if shape.is_placeholder:
        return "ph:" + str(shape.placeholder_format.type).split(".")[-1].split(" ")[0].lower()
    st = shape.shape_type
    if st == MSO_SHAPE_TYPE.PICTURE:
        return "pic"
    if getattr(shape, "has_table", False) and shape.has_table:
        return "tbl"
    if getattr(shape, "has_chart", False) and shape.has_chart:
        return "chart"
    if st == MSO_SHAPE_TYPE.GROUP:
        return "group"
    tag = shape._element.tag
    if tag.endswith("graphicFrame"):
        uri = shape._element.xpath(".//a:graphicData/@uri")
        return "smartart" if uri and "diagram" in uri[0] else "ole"
    return "box"


def walk(shapes, parent=None):
    for sh in shapes:
        yield sh, parent
        if sh.shape_type == MSO_SHAPE_TYPE.GROUP:
            yield from walk(sh.shapes, sh.shape_id)


def paragraphs_of(shape):
    """[(key, text)] for a shape: paragraph index for text, r<row>c<col>.<para> for tables."""
    out = []
    if getattr(shape, "has_text_frame", False) and shape.has_text_frame:
        for i, p in enumerate(shape.text_frame.paragraphs):
            out.append((str(i), p.text))
    elif getattr(shape, "has_table", False) and shape.has_table:
        for ri, row in enumerate(shape.table.rows):
            for ci, cell in enumerate(row.cells):
                text = "\n".join(p.text for p in cell.text_frame.paragraphs)
                out.append((f"r{ri}c{ci}", text))
    return out


def smartart_text(slide, shape):
    """SmartArt text lives in a separate diagram part; read it so the agent knows it is there."""
    ids = shape._element.xpath(".//*[local-name()='relIds']/@*[local-name()='dm']")
    if not ids:
        return []
    try:
        part = slide.part.related_part(ids[0])
    except KeyError:
        return []
    from lxml import etree

    root = etree.fromstring(part.blob)
    return [t.text for t in root.iter("{http://schemas.openxmlformats.org/drawingml/2006/main}t") if t.text]


def clip(text, n=90):
    text = text.replace("\v", "⏎").replace("\x0b", "⏎")
    return text if len(text) <= n else text[: n - 1] + "…"


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    path = args[0]
    check = "--check" in args
    spec = args[args.index("--slides") + 1] if "--slides" in args else None
    prs = Presentation(path)
    slides = list(prs.slides)
    numbers = parse_ranges(spec, len(slides))
    findings = []
    if not check:
        print(f"{path}: {len(slides)} slides, {len(prs.slide_layouts)} layouts, "
              f"size {prs.slide_width}x{prs.slide_height} EMU")
    for n in numbers:
        slide = slides[n - 1]
        if not check:
            print(f"\n== slide {n} | layout \"{slide.slide_layout.name}\"")
        for shape, parent in walk(slide.shapes):
            kind = kind_of(shape)
            paras = paragraphs_of(shape)
            if kind == "smartart":
                paras = [(f"s{i}", t) for i, t in enumerate(smartart_text(slide, shape))]
            dummy = [(k, t) for k, t in paras if is_dummy(t)]
            for k, t in dummy:
                findings.append(f"slide {n} id={shape.shape_id} [{k}] {clip(t, 60)!r}")
            if check or kind == "group":
                continue
            if not paras and kind not in ("pic", "chart", "smartart", "ole"):
                continue
            where = f" in={parent}" if parent else ""
            flag = "  !DUMMY" if dummy else ""
            line = f"  id={shape.shape_id} {kind} \"{clip(shape.name, 40)}\"{where}{flag}"
            if paras:
                line += "  " + "  ".join(f"[{k}] {clip(t)!r}" for k, t in paras)
            print(line)
        if not check and slide.has_notes_slide:
            notes = slide.notes_slide.notes_text_frame.text.strip()
            if notes:
                print(f"  notes: {clip(notes, 120)!r}")
    if check:
        if findings:
            print(f"CHECK FAILED: {len(findings)} paragraph(s) still look like sample text:")
            for f in findings:
                print("  " + f)
            print("Fill them, delete the shape, or tell the user why they stay.")
            sys.exit(2)
        print(f"CHECK OK: no sample text found on {len(numbers)} slide(s).")


if __name__ == "__main__":
    main()
