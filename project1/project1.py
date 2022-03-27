import spacy

nlp = spacy.load("en_core_web_sm")

def redact_names(input_files):
    for inp in input_files:
        print(inp.input_str)
        doc = nlp(inp.input_str)

        for ent in doc.ents:
            print(f"{ent.text}--{ent.label_}")

def redact_genders(input_files):
    for inp in input_files:
        pass

def redact_dates(input_files):
    for inp in input_files:
        pass

def redact_phones(input_files):
    for inp in input_files:
        pass

def redact_address(input_files):
    for inp in input_files:
        pass

def redact_concepts(input_files):
    for inp in input_files:
        pass