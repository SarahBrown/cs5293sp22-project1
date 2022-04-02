import spacy
import en_core_web_lg
import re

nlp = en_core_web_lg.load()

def redact_names(input_files):
    for inp in input_files:
        doc_lg = nlp(inp.input_str)
        names = []
        PROPN_ENT = []
        ENTS = []

        # check for entities in document
        for ent in doc_lg.ents:
            if (ent.label_ == "PERSON"):
                ent_label = ent.text.split("\n")[0] # removes any new lines from name
                if (ent_label[-1] == " "): # removes any extra spaces from name
                    ent_label = ent_label[0:-1]
                ENTS.append([ent_label, ent.start, ent.start_char, len(ent_label)])


        # get document tokens and then check NER 
        for token in doc_lg:
            if (token.pos_ == "PROPN"):
                tok_test = nlp(token.text)

                for ent in tok_test.ents:
                    if (ent.label_ == "PERSON"):
                        PROPN_ENT.append([token.text, token.i, token.idx, len(token.text)])
                    
        names = merge_lists(ENTS, PROPN_ENT)        

        print(inp.file_name)
        print(names)
        print("\n")

        regex_names = []
        for name in names:
            regex_names.append(name[0])

        for reg_name in regex_names:
            x = re.search(reg_name, inp.input_str)
            print(x)

    return input_files

def merge_lists(list1, list2):
    merged = list1.copy()
    list1_range = range(len(list1))

    for item in list2:
        skip_flag = False
        
        for i in list1_range:
            if (abs(item[1] - list1[i][1]) < 2):
                skip_flag = True
                break
        
        if (not skip_flag):
            merged.append(item)

    return merged    

def redact_genders(input_files):
    for inp in input_files:
        doc = nlp(inp.input_str)
        propn = []

        for token in doc:
            if (token.tag_ == "PRP" or token.tag_ == "PRP$"):
                if (token.text in ["she", "She", "her", "Her","hers","Hers","he", "He", "him", "Him","his","His"]):
                    propn.append([token.text, token.i])

    print(propn)

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
                    print("\n")
                    print(f"{token}--{simil}--{token.i}")
                    print(f"---------{token.sent}")