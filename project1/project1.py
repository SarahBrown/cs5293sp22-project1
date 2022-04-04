from errno import ENOTSOCK
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
                ent_label = ent_label.split("<")[0] # removes any non-name parts from email header
                while (ent_label[-1] == " "): # removes any extra spaces from end of name
                    ent_label = ent_label[0:-1]
                ENTS.append([ent_label, ent.start_char, ent.start_char+len(ent_label)]) # string text, start char, end char

        # get document tokens and then check NER 
        for token in doc_lg:
            if (token.pos_ == "PROPN"):
                tok_text = token.text
                tok_test = nlp(tok_text) # creates a nlp doc for each token to perform NER

                for ent in tok_test.ents:
                    if (ent.label_ == "PERSON"):
                        PROPN_ENT.append([tok_text, token.idx, token.idx+len(tok_text)]) # string text, start char, end char
                    
        # merges two lists for all names recognized by NER
        names = merge_lists(ENTS, PROPN_ENT)        
        print(names)

        # takes combined list and creates a set of names to search document via regex
        regex_names = set()
        for name in names:
            name_parts = name[0].split(" ") # splits strings to individually search for first/last name
            for part in name_parts:
                if (len((re.sub("[^a-zA-Z]+", "",part))) > 1):
                    regex_names.add("\\b"+part+"\\b")


        # searches input text string for matches to regex set
        name_matches = find_regex(regex_names, inp.input_str)
        # merges both lists so multiple name (eg first and last) items are together
        name_matches = merge_lists(names, name_matches)
        # add input files redactions to stats file
        inp.add_redact(name_matches, "names")

def redact_genders(input_files):
    for inp in input_files:
        doc = nlp(inp.input_str)
        propn = []

        for token in doc:
            if (token.tag_ == "PRP" or token.tag_ == "PRP$"):
                if (token.text in ["she","She","her","Her","hers","Hers","he","He","him","Him","his","His"]):
                    propn.append([token.text, token.i])

    print(propn)

    return input_files

def redact_dates(input_files):
    for inp in input_files:
        doc = nlp(inp.input_str)
        ENTS = []

        for ent in doc.ents:
            if (ent.label_ == "DATE"):
                ENTS.append([ent.text, ent.start_char, ent.start_char+len(ent.text)]) # string text, start char, end char
                print(re.sub("\n","(NL)",ent.text))

        print("\n")

def redact_phones(input_files):
    for inp in input_files:
        phone_patterns = {
            r"[+1(-]{0,3}[0-9]{0,3}[- )]{1,2}[0-9]{3}[- ][0-9]{4}",
        }

        phones = find_regex(phone_patterns, inp.input_str)
        print(phones)
        print(len(phones))
        if (len(phones)>0):
            inp.add_redact(phones, "phones")

def redact_address(input_files):
    for inp in input_files:
        doc = nlp(inp.input_str)
        ENTS = []

        for ent in doc.ents:
            if (ent.label_ == "LOC"):
                ENTS.append([ent.text, ent.start_char, ent.start_char+len(ent.text)]) # string text, start char, end char
                print(re.sub("\n","(NL)",ent.text))

def redact_concepts(input_files, concept):
    for inp in input_files:
        doc = nlp(inp.input_str)
        nlp_concept = nlp(concept)
        similar = []
        sentences = []
        sent_added = set()

    if(nlp_concept and nlp_concept.vector_norm): # checks for valid word vector
        for token in doc:
            if (token and token.vector_norm): # checks for valid word vector
                simil = nlp_concept.similarity(token)
                if (simil > 0.5):
                    #print(f"{token}--{simil}--{token.i}")
                    similar.append([token.text, token.sent.start_char, token.sent.end_char]) # token text, sentence start char, sentence end char

    for similar_tok in similar:
        if (similar_tok[1] not in sent_added):
            sent_added.add(similar_tok[1])
            sentences.append(similar_tok)
    inp.add_redact(sentences, "concept")

def merge_lists(list1, list2):
    merged = list1.copy()
    list1_range = range(len(list1))

    for item in list2:
        skip_flag = False
        item_len = item[2]-item[1]

        for i in list1_range:
            len_i = list1[i][2]-list1[i][1]
            if ((item[1]==list1[i][1]) or (item[1]+item_len+1==list1[i][1]) or (list1[i][1]+len_i+1==item[1])):
                skip_flag = True
                break
        
        if (not skip_flag):
            merged.append(item)

    return merged

def find_regex(reg_set, input_str):
    matches = []
    for reg in reg_set:
        iter = re.finditer(reg, input_str) # pattern, string, flags
        for match in iter:
            matches.append([match.group(), match.span()[0], match.span()[1]]) # string text, dx from start, string end char 

    return matches   