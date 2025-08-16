import bz2
import xml.etree.ElementTree as ET
import re

def extract_entries(bz2_file, xml_file):
    NS = "{http://www.mediawiki.org/xml/export-0.11/}"
    GER_MARKER = re.compile(r"\{\{Sprache\|Deutsch\}\}")
    with bz2.open(bz2_file, "rb") as input_file, open(xml_file, "wb") as output_file:
        output_file.write(b"<?xml version='1.0' encoding='utf-8'?>\n<ger-dict>")
        context = ET.iterparse(input_file)
        for event, elem in context:
            if elem.tag == f"{NS}page":
                elem_ns = elem.find(f"{NS}ns")
                if elem_ns is not None and elem_ns.text == "0":
                    revision = elem.find(f"{NS}revision")
                    if revision is not None:
                        elem_text = revision.find(f"{NS}text")
                        if elem_text is not None and elem_text.text is not None and GER_MARKER.search(elem_text.text):
                            elem_title = elem.find(f"{NS}title")
                            if elem_title is not None:
                                minimal_elem = ET.Element("word")
                                word_title = ET.SubElement(minimal_elem, "title")
                                word_title.text = elem_title.text
                                word_info = ET.SubElement(minimal_elem, "info")
                                word_info.text = elem_text.text
                                output_file.write(ET.tostring(minimal_elem, encoding="UTF-8"))
                elem.clear()
        output_file.write(b"</ger-dict>")

extract_entries("resources/dewiktionary-20250801-pages-articles.xml.bz2", "resources/ger_dict.xml")

