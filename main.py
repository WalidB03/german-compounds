def find_relations(words):
    words = [word.lower() for word in words]
    words.sort(key=len)
    relations = []
    for i, component in enumerate(words):
        if len(component) <= 2:
            continue

        for compound in words[i+1:]:
            if len(compound) <= len(component) + 2:
                continue

            pos = compound.find(component)
            if pos != -1:
                relations.append([compound, component, pos])
    return relations

def main():
    words = [
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
    ]
    relations = find_relations(words)
    for relation in relations:
        print(relation)

if __name__ == "__main__":
    main()

