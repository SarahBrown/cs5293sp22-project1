import spacy
#import nltk

nlp = spacy.load("en_core_web_lg")

def redact_namesv1(input_files):
    for inp in input_files:
        doc = nlp(inp.input_str)

        print("---------spacy---------")
        for ent in doc.ents:
            if (ent.label_ == "PERSON"): #and (not "_" in ent.text)):
                print(f"{ent.text}--{ent.label_}--{ent.start_char}--{ent.end_char}")
            else:
                print(f"-----{ent.text}--{ent.label_}")
        
        print("---------POS---------")
        for token in doc:
            if (token.pos_ == "PROPN"):
                print(f"{token.text}--PROPN--{token.i}")

        print("---------POS & ent---------")
        for token in doc:
            if (token.pos_ == "PROPN"):
                tok_test = nlp(token.text)

                for ent in tok_test.ents:
                    if (ent.label_ == "PERSON"):
                        print(f"{token.text}--{ent.label_}--{token.i}")
                    else:
                        print(f"-----{ent.text}--{ent.label_}")

    return input_files

def redact_names(input_files):
    for inp in input_files:
        doc = nlp(inp.input_str)
        propn = []

        for token in doc:
            if (token.tag_ == "NNP"):
                propn.append([token.text, token.i])
        
        print(propn)

        # for ent in doc.ents:
        #     if (ent.label_ == "PERSON"): #and (not "_" in ent.text)):
        #         print(f"{ent.text}--{ent.label_}--{ent.start_char}--{ent.end_char}")


        # print("---------POS & ent---------")
        # for token in doc:
        #     if (token.pos_ == "PROPN"):
        #         tok_test = nlp(token.text)

        #         for ent in tok_test.ents:
        #             if (ent.label_ == "PERSON"):
        #                 print(f"{token.text}--{ent.label_}--{token.i}")
        #             else:
        #                 print(f"-----{ent.text}--{ent.label_}")

    return input_files

def redact_genders(input_files):
    for inp in input_files:
        doc = nlp(inp.input_str)
        propn = []

        for token in doc:
            if (token.tag_ == "PRP" or token.tag_ == "PRP$"):
                if (token.text in ["she", "She", "her", "Her","hers","Hers","he", "He", "him", "Him","his","His"]):
                    propn.append([token.text, token.i])

    print(propn)

    test = nlp("Mailwoman")
    for token in test:
        print(f"{token.text}--{token.lemma_}")

    return input_files


def redact_dates(input_files):
    for inp in input_files:
        pass

def redact_phones(input_files):
    for inp in input_files:
        pass

def redact_address(input_files):
    for inp in input_files:
        pass

def redact_concepts(input_files, concept):
    for inp in input_files:
        doc = nlp(inp.input_str)
        nlp_concept = nlp(concept)

    if(nlp_concept and nlp_concept.vector_norm): # checks for valid word vector
        for token in doc:
            if (token and token.vector_norm): # checks for valid word vector
                simil = nlp_concept.similarity(token)
                if (simil > 0.5):
                    print(f"{token}--{simil}")