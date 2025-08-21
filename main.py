from gzip import open as zopen
from orjson import loads as jloads
from ahocorasick import Automaton

def find_relations(file_path):
    words = set()
    automaton = Automaton()

    with zopen(file_path, "rb") as file:

        for line in file:
            line = line.strip()

            if not line:
                continue

            entry = jloads(line)
            if "word" not in entry:
                continue

            word = entry["word"].lower()
            if entry["lang_code"] != "de" or entry["lang"] != "Deutsch" or len(word) < 3 or " " in word:
                continue

            print(word)
            words.add(word)
            automaton.add_word(word, word)

    automaton.make_automaton()

    for compound in words:
        if len(compound) < 6:
            continue

        components = set()
        for _, component in automaton.iter(compound):
            if component != compound:
                components.add(component)

        if components:
            yield {"compound": compound, "components": components}

def main():
    for relation in find_relations("resources/de-extract.jsonl.gz"):
        print(relation)

if __name__ == "__main__":
    main()

