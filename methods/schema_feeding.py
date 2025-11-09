# Preprocess OWL into simple schema representation
from owlready2 import get_ontology, Thing
import os

path = "../kg-data/Updated Knowledge Base/cmeo-core.owl"
onto = get_ontology(path).load()

def print_subclasses(cls, indent=2):
    # Recursively print subclasses with labels
    for sub in cls.subclasses():
        if sub == Thing:
            continue
        labels = getattr(sub, "label", [])
        print(" " * indent + f"SubClassOf: {sub.name}, label(en): {labels}")
        print_subclasses(sub, indent + 2)

for cls in onto.classes():
    if cls == Thing:
        continue
    labels = getattr(cls, "label", [])
    print(f"Class: {cls.name}, label(en): {labels}")
    print_subclasses(cls)

for cls in onto.classes():
    print("Class", cls.name, " label(en): ", getattr(cls, "label", []))
for prop in onto.object_properties():
    print("Object property:", prop.name, "-> domain: ", prop.domain, " range: ", prop.range, " label(en): ", getattr(prop, "label", []))
for dp in onto.data_properties():
    print("Data property: ", dp.name, "-> domain: ", dp.domain, " range: ", dp.range, " label(en): ", getattr(dp, "label", []))

