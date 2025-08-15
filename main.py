from ahocorasick import Automaton

def build_automaton(words_set):
    automaton = Automaton()
    for word in words_set:
        automaton.add_word(word, word)
    automaton.make_automaton()
    return automaton

def find_relations(words):
    words = {w.lower() for w in words if len(w) > 2}
    automaton = build_automaton(words)
    relations = set()
    for compound in words:
        if len(compound) < 6:
            continue
        for end_index, component in automaton.iter(compound):
            if component != compound:
                relations.add((compound, component))
    return relations

def main():
    words = {
        "Tag", "Geburtstag","Auto",
        "Autobahn", "Bahn", "Zeit",
        "Zeitung","See", "Hund",
        "Katze", "Baum", "Blume",
        "Mutter", "Vater", "Spiel",
        "Spielzeug", "Zeug", "Schiff",
        "Schifffahrt", "Fahrt", "Frei",
        "Freiheit", "Obst", "Obstkuchen",
        "Kuchen", "Stab", "Buchstabieren",
        "Wasser", "Wassermelone", "Melone",
        "Haus", "Land", "Feuer",
        "Tagung", "Haustür", "Feuerwehr",
        "Landkreis", "Hand","geburt"
    }
    relations = find_relations(words)
    for relation in relations:
        print(relation)

if __name__ == "__main__":
    main()

