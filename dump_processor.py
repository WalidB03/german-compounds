import bz2
from lxml import etree
import re

def extract_entries(bz2_file, xml_file):
    NS = "{http://www.mediawiki.org/xml/export-0.11/}"
    GER_MARKER = re.compile(r"\{\{Sprache\|Deutsch\}\}")

    with bz2.open(bz2_file, "rb") as input_file, open(xml_file, "wb") as output_file:
        output_file.write(b"<?xml version='1.0' encoding='utf-8'?>\n<ger-dict>")

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

            word = etree.Element("word")
            word_title = etree.SubElement(word, "title")
            word_title.text = title.text
            word_info = etree.SubElement(word, "info")
            word_info.text = text.text
            output_file.write(etree.tostring(word, encoding="UTF-8"))

            elem.clear()

        output_file.write(b"</ger-dict>")

def main():
    extract_entries("resources/dewiktionary-20250801-pages-articles.xml.bz2", "resources/ger_dict.xml")

if __name__ == "__main__":
    main()

