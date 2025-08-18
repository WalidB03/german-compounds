import bz2
from lxml import etree
import re
from wiktextract import WiktextractContext, WiktionaryConfig, parse_page
from wikitextprocessor import Wtp
import json

def extract_entries(bz2_file):
    NS = "{http://www.mediawiki.org/xml/export-0.11/}"
    GER_MARKER = re.compile(r"\{\{Sprache\|Deutsch\}\}")

    config = WiktionaryConfig(
    dump_file_lang_code="de",
    capture_language_codes=["de", "mul"],
    capture_translations=True,
    capture_pronunciation=True,
    capture_linkages=True,
    capture_compounds=True,
    capture_redirects=True,
    capture_examples=True,
    capture_etymologies=True,
    capture_inflections=True,
    capture_descendants=True,
    verbose=True,
    expand_tables=True,
    )
    wtp = Wtp(lang_code="de")
    wxr = WiktextractContext(wtp, config)

    with bz2.open(bz2_file, "rb") as input_file:

        context = etree.iterparse(input_file, tag=f"{NS}page")
        for _, elem in context:
            title = elem.find(f"{NS}title")
            ns = elem.find(f"{NS}ns")
            revision = elem.find(f"{NS}revision")

            if title is None or ns is None or ns.text != "0" or revision is None:
                elem.clear()
                continue

            text = revision.find(f"{NS}text")
            if text is None or text.text is None or not GER_MARKER.search(text.text):
                elem.clear()
                continue

            entry = parse_page(wxr, title.text, text.text)
            for word in entry:
                yield word

            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]

def main():
    for word in extract_entries("resources/dewiktionary-20250801-pages-articles.xml.bz2"):
            print(word)

if __name__ == "__main__":
    main()

