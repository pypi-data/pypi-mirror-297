import re

import markdownify
import six

BANNED_SECTION_PREFIXES = [
    "bibliography of",
]
_BANNED_SECTION_PREFIXES_REGEXP_PART = "|".join(BANNED_SECTION_PREFIXES)
BANNED_SECTION_PREFIXES_REGEXP = re.compile(
    rf"^({_BANNED_SECTION_PREFIXES_REGEXP_PART})"
)


BANNED_SECTIONS = {
    "contents",
    "index",
    "table of content",
    "author contribution",
    "data availability statement",
    "data availability",
    "declaration of competing interest",
    "acknowledgment",
    "acknowledgments",
    "acknowledgements",
    "supporting information",
    "conflict of interest disclosures",
    "conflict of interest",
    "conflict of interest statement",
    "ethics statement",
    "references",
    "external links",
    "further reading",
    "works cited",
    "bibliography",
    "notes",
    "sources",
    "footnotes",
    "suggested readings",
    "academic journal articles",
    "academic books",
    "table of contents",
    "keywords",
    "содержание",
    "оглавление",
    "список литературы" "источники",
    "ссылки",
    "благодарность",
    "благодарности",
}

SECTIONS_MAPS = {
    "Authors": "Authors",
    "AUTHORS": "Authors",
    "Abstract": "Abstract",
    "ABSTRACT": "Abstract",
    "Date": "Date",
    "DATE": "Date",
    "acknowledgements": "Acknowledgements",
    "INTRODUCTION": "Introduction",
    "MATERIALS AND METHODS": "Methods",
    "Materials and methods": "Methods",
    "METHODS": "Methods",
    "RESULTS": "Results",
    "CONCLUSIONS": "Conclusions",
    "CONCLUSIONS AND FUTURE APPLICATIONS": "Conclusions",
    "DISCUSSION": "Discussion",
    "ACKNOWLEDGMENTS": "Acknowledgements",
    "TABLES": "Tables",
    "Tabnles": "Tables",
    "DISCLOSURE": "Disclosure",
    "CONFLICT OF INTEREST": "Disclosure",
    "Declaration of conflicting interests": "Disclosure",
    "Declaration of competing interest": "Disclosure",
    "Acknowledgement": "Acknowledgements",
    "Acknowledgments": "Acknowledgements",
    "conflictofintereststatement": "Disclosure",
    "FUNDING": "Funding",
    "fundinginformation": "Funding",
    "BIOGRAPHIES": "Biographies",
    "disclaimer": "Disclosure",
    "referencesfigure": "References Figure",
    "declaration of competing interest": "Disclosure",
    "conflict of interest disclosures": "Disclosure",
    "conflict of interest statement": "Disclosure",
    "authors' contributions": "Author Contribution",
}


def is_banned_section(text: str):
    text = text.lower()
    stripped_text = re.sub(r"^\d+\s*\.\s*", "", text).strip()
    return (
        text in BANNED_SECTIONS
        or stripped_text in BANNED_SECTIONS
        or BANNED_SECTION_PREFIXES_REGEXP.match(text)
        or BANNED_SECTION_PREFIXES_REGEXP.match(stripped_text)
    )


class MarkdownConverter(markdownify.MarkdownConverter):
    convert_b = markdownify.abstract_inline_conversion(lambda self: "**")
    convert_i = markdownify.abstract_inline_conversion(lambda self: "__")
    convert_em = markdownify.abstract_inline_conversion(lambda self: "__")

    def process_text(self, el):
        text = six.text_type(el) or ""

        # dont remove any whitespace when handling pre or code in pre
        if not (
            el.parent.name == "pre"
            or el.parent.name == "math"
            or (el.parent.name == "code" and el.parent.parent.name == "pre")
        ):
            text = markdownify.whitespace_re.sub(" ", text)

        if (
            el.parent.name != "code"
            and el.parent.name != "pre"
            and el.parent.name != "math"
        ):
            text = self.escape(text)

        # remove trailing whitespaces if any of the following condition is true:
        # - current text node is the last node in li
        # - current text node is followed by an embedded list
        if el.parent.name == "li" and (
            not el.next_sibling or el.next_sibling.name in ["ul", "ol"]
        ):
            text = text.rstrip()

        return text

    def convert_header(self, el, text, convert_as_inline):
        return self.convert_hn(2, el, text, convert_as_inline)

    def convert_math(self, el, text, convert_as_inline):
        return text

    def convert_title(self, el, text, convert_as_inline):
        return self.convert_hn(2, el, text, convert_as_inline)

    def convert_soup(self, soup):
        r = super().convert_soup(soup)
        return re.sub(r"\n{2,}", "\n\n", r).replace("\r\n", "").strip()

    def convert_td(self, el, text, convert_as_inline):
        return " " + text.strip().replace("\n", "  ") + " |"

    def convert_th(self, el, text, convert_as_inline):
        return super().convert_th(
            el, text.strip().replace("\n", "  "), convert_as_inline
        )

    def convert_li(self, el, text, convert_as_inline):
        parent = el.parent
        is_inside_table = False
        grand_parent = parent

        while grand_parent is not None:
            if grand_parent.name in ("tr", "th", "tbody", "table", "td"):
                is_inside_table = True
                break
            grand_parent = grand_parent.parent

        if parent is not None and parent.name == "ol":
            if parent.get("start"):
                start = int(parent.get("start"))
            else:
                start = 1
            bullet = "%s." % (start + parent.index(el))
        else:
            depth = -1
            while el:
                if el.name == "ul":
                    depth += 1
                el = el.parent
            bullets = self.options["bullets"]
            bullet = bullets[depth % len(bullets)]

        text = (text or "").strip()
        if is_inside_table:
            text = text.replace("\n", " ")
        return "%s %s\n" % (bullet, text)

    def convert_tr(self, el, text, convert_as_inline):
        cells = el.find_all(["td", "th"])
        is_headrow = (
            all([cell.name == "th" for cell in cells])
            or (not el.previous_sibling and not el.parent.name == "tbody")
            or (
                not el.previous_sibling
                and el.parent.name == "tbody"
                and len(el.parent.parent.find_all(["thead"])) < 1
            )
        )
        overline = ""
        underline = ""
        if is_headrow and not el.previous_sibling:
            # first row and is headline: print headline underline
            underline += "| " + " | ".join(["---"] * len(cells)) + " |" + "\n"
        elif not el.previous_sibling and (
            el.parent.name == "table"
            or (el.parent.name == "tbody" and not el.parent.previous_sibling)
        ):
            # first row, not headline, and:
            # - the parent is table or
            # - the parent is tbody at the beginning of a table.
            # print empty headline above this row
            overline += "| " + " | ".join([""] * len(cells)) + " |" + "\n"
            overline += "| " + " | ".join(["---"] * len(cells)) + " |" + "\n"
        return overline + "|" + text.strip().replace("\n", "  ") + "\n" + underline

    def convert_blockquote(self, el, text, convert_as_inline):
        if convert_as_inline:
            return text

        return (
            "\n" + (markdownify.line_beginning_re.sub("> ", text.strip()) + "\n\n")
            if text
            else ""
        )


md = MarkdownConverter(
    sub_symbol="~",
    sup_symbol="^",
    heading_style=markdownify.ATX,
    autolinks=False,
)
