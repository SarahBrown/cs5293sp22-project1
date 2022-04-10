import spacy
import en_core_web_lg
import re
import nltk

nlp = en_core_web_lg.load()

def redact_names(input_files):
    """Function to redact names in input text file."""
    # loops through each input file and finds names
    for inp in input_files:
        doc_lg = nlp(inp.input_str)
        names = []
        PROPN_ENT = []
        ENTS = []
        nltk_names = []

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

        # looks for names via nltk
        sentences = nltk.sent_tokenize(inp.input_str)
        sentences = [nltk.word_tokenize(sent) for sent in sentences]
        sentences = [nltk.pos_tag(sent) for sent in sentences]

        for tagged_sentence in sentences:
            for chunk in nltk.ne_chunk(tagged_sentence):
                if type(chunk) == nltk.tree.Tree:
                    if chunk.label() == 'PERSON':
                        found_name = chunk.leaves()[0][0]
                        if (re.search(r'[0-9]',found_name) == None): # contains no numbers
                            if (found_name not in ["Mon","Tue","Wed","Thu","Fri","Sat","Sun","Hello"]): # removes days of week abbreivations and Hello
                                nltk_names.append(found_name)                            
                    
        # merges two lists for all names recognized by NER
        names = merge_lists(ENTS, PROPN_ENT)        

        # takes combined list and creates a set of names to search document via regex. also adds in nltk names
        regex_names = set()
        for name in names:
            name_parts = name[0].split(" ") # splits strings to individually search for first/last name
            for part in name_parts:
                if (len((re.sub("[^a-zA-Z]+", "",part))) > 1):
                    regex_names.add("\\b"+part+"\\b") # to avoid getting forever when searching for eve
            for nltk_n in nltk_names: # adds names found via nltk
                regex_names.add("\\b"+nltk_n+"\\b") 


        # searches input text string for matches to regex set
        name_matches = find_regex(regex_names, inp.input_str, False)
        # merges both lists so multiple name (eg first and last) items are together
        name_matches = merge_lists(names, name_matches)
        # add input files redactions to stats file
        inp.add_redact(name_matches, "names")

def redact_genders(input_files):
    """Function to redact genders in input text file."""
    # loops through each input file
    for inp in input_files:
        genders = []
        formatted_terms = []
        # gendered terms, titles, and pronouns to search for
        gendered_terms = ["father","mother","son","daughter","boy","girl","man","woman","dad","mom","husband",
        "wife","sister","brother","widow","widower","bride","groom","bachelor","bachelorette","father-in-law",
        "mother-in-law","lady","lord","gentleman","king","queen","grandfather","grandmother","uncle","aunt",
        "niece","nephew","host","hostess","heir","heiress","duke","duchess","earl","countess","count","headmaster",
        "headmistress","mistress","mister","lad","lass","landlord","landlady","male","girlfriend","boyfriend"
        "female","miss","sir","madam","ma'am","son-in-law","daughter-in-law","prince","princess","stepfather",
        "stepmother","stepson","stepdaughter","waiter","waiteress","she","her","hers","he","him","his"]
        gender_titles=[r'\\bmrs\.',r'\\bms\.',r'\\bmr\.']

        # adds word breaks to terms for regex
        for term in gendered_terms:
            formatted_terms.append("\\b"+term+"s{0,1}\\b")

        # adds any term that matches gender list    
        genders = find_regex(formatted_terms, inp.input_str, True)
        found_titles = find_regex(gender_titles, inp.input_str, True)

        # adds found terms to list
        for found in found_titles:
            genders.append(found)
        # add input file redaction to stats file
        inp.add_redact(genders, "genders")

def redact_dates(input_files):
    """Function to redact dates from input."""
    # loops through each inp file
    for inp in input_files:
        doc = nlp(inp.input_str)
        ent_dates = []
        date_patterns = [r'[A-Z][a-z]{2}, [0-9]{1,2} [A-Z][a-z]{2} [0-9]{4}',r'[0-9]{1,2}[ ,/-]{1}[0-9]{1,2}[ ,/-]{1}[0-9]{2,4}'] # regex patterns to look for

        # looks for DATE entities 
        for ent in doc.ents:
            if (ent.label_ == "DATE"):
                if ((re.search(r"@",ent.text) == None)): # filters to DATE labels not including @ 
                    end_char = ent.start_char+len(ent.text)
                    added = False
                    if (end_char + 5 < len(inp.input_str)): # checks to make sure not going outside of len of txt doc
                        etc_char = ""
                        for i in range(end_char,end_char+5):
                            etc_char = etc_char + (inp.input_str[i]) # creates a string with characters that follow
                        
                        if (re.match(r' & [0-9]{1,2}', etc_char)): # checkes to see if matches month day & day format
                            ent_dates.append([ent.text+etc_char, ent.start_char, end_char+5]) # string text, start char, end char
                            added = True
                    if (not added): # checks if ent has been added in the above check for extra characters
                        ent_dates.append([ent.text, ent.start_char, end_char]) # string text, start char, end char

        # checks for other dates matching regex format and merges lists
        other_dates = find_regex(date_patterns , inp.input_str, True)
        dates = merge_lists(other_dates, ent_dates)

        inp.add_redact(dates, "dates") # add redacted dates to stats object

def redact_phones(input_files):
    """Function to redact phones from input."""
    # loops through each input file
    for inp in input_files:
        phone_patterns = {
            r"[+1(-]{0,3}[0-9]{0,3}[- )]{1,2}[0-9]{3}[- ][0-9]{4}", # regex pattern for US phone numbers
        }

        # find and add matches
        phones = find_regex(phone_patterns, inp.input_str,False)
        if (len(phones)>0):
            inp.add_redact(phones, "phones")

def redact_address(input_files):
    """Function to redact addresses from input file."""
    for inp in input_files:
        # suffix forms that are primary street suffix names, common street suffixes or suffix abbreviations, and recommended official Postal Service standard suffix abbreviations
        street_copypaste = "ALLEY ALLEE    ALY  ALLEY  ALLY  ALY  ANEX    ANEX    ANX  ANNEX  ANNX  ANX  ARCADE    ARC    ARC  ARCADE  AVENUE    AV    AVE  AVE  AVEN  AVENU  AVENUE  AVN  AVNUE  BAYOU    BAYOO    BYU  BAYOU  BEACH    BCH    BCH  BEACH  BEND    BEND    BND  BND  BLUFF    BLF    BLF  BLUF  BLUFF  BLUFFS    BLUFFS    BLFS  BOTTOM     BOT    BTM  BTM  BOTTM  BOTTOM  BOULEVARD    BLVD    BLVD  BOUL  BOULEVARD  BOULV  BRANCH    BR    BR  BRNCH  BRANCH  BRIDGE    BRDGE    BRG  BRG  BRIDGE  BROOK    BRK    BRK  BROOK  BROOKS    BROOKS    BRKS  BURG    BURG    BG  BURGS    BURGS    BGS  BYPASS    BYP    BYP  BYPA  BYPAS  BYPASS  BYPS  CAMP    CAMP    CP  CP  CMP  CANYON     CANYN    CYN  CANYON  CNYN  CAPE     CAPE    CPE  CPE  CAUSEWAY     CAUSEWAY    CSWY  CAUSWA  CSWY  CENTER    CEN    CTR  CENT  CENTER  CENTR  CENTRE  CNTER  CNTR  CTR  CENTERS    CENTERS    CTRS  CIRCLE    CIR    CIR  CIRC  CIRCL  CIRCLE  CRCL  CRCLE  CIRCLES    CIRCLES    CIRS  CLIFF    CLF    CLF  CLIFF  CLIFFS    CLFS    CLFS  CLIFFS  CLUB    CLB    CLB  CLUB  COMMON    COMMON    CMN  COMMONS    COMMONS    CMNS  CORNER    COR    COR  CORNER  CORNERS    CORNERS    CORS  CORS  COURSE    COURSE    CRSE  CRSE  COURT    COURT    CT  CT  COURTS    COURTS    CTS  CTS  COVE    COVE    CV  CV  COVES    COVES    CVS  CREEK    CREEK    CRK  CRK  CRESCENT    CRESCENT    CRES  CRES  CRSENT  CRSNT  CREST    CREST    CRST  CROSSING     CROSSING    XING  CRSSNG  XING  CROSSROAD    CROSSROAD    XRD  CROSSROADS    CROSSROADS    XRDS  CURVE    CURVE    CURV  DALE    DALE    DL  DL  DAM    DAM    DM  DM  DIVIDE    DIV    DV  DIVIDE  DV  DVD  DRIVE    DR    DR  DRIV  DRIVE  DRV  DRIVES    DRIVES    DRS  ESTATE    EST    EST  ESTATE  ESTATES    ESTATES    ESTS  ESTS  EXPRESSWAY    EXP    EXPY  EXPR  EXPRESS  EXPRESSWAY  EXPW  EXPY  EXTENSION    EXT    EXT  EXTENSION  EXTN  EXTNSN  EXTENSIONS    EXTS    EXTS  FALL    FALL    FALL  FALLS    FALLS    FLS  FLS  FERRY    FERRY    FRY  FRRY  FRY  FIELD    FIELD    FLD  FLD  FIELDS    FIELDS    FLDS  FLDS  FLAT    FLAT    FLT  FLT  FLATS    FLATS    FLTS  FLTS  FORD    FORD    FRD  FRD  FORDS    FORDS    FRDS  FOREST    FOREST    FRST  FORESTS  FRST  FORGE    FORG    FRG  FORGE  FRG  FORGES    FORGES    FRGS  FORK    FORK    FRK  FRK  FORKS    FORKS    FRKS  FRKS  FORT    FORT    FT  FRT  FT  FREEWAY    FREEWAY    FWY  FREEWY  FRWAY  FRWY  FWY  GARDEN    GARDEN    GDN  GARDN  GRDEN  GRDN  GARDENS    GARDENS    GDNS  GDNS  GRDNS  GATEWAY    GATEWAY    GTWY  GATEWY  GATWAY  GTWAY  GTWY  GLEN    GLEN    GLN  GLN  GLENS    GLENS    GLNS  GREEN    GREEN    GRN  GRN  GREENS    GREENS    GRNS  GROVE    GROV    GRV  GROVE  GRV  GROVES    GROVES    GRVS  HARBOR    HARB    HBR  HARBOR  HARBR  HBR  HRBOR  HARBORS    HARBORS    HBRS  HAVEN    HAVEN    HVN  HVN  HEIGHTS    HT    HTS  HTS  HIGHWAY    HIGHWAY    HWY  HIGHWY  HIWAY  HIWY  HWAY  HWY  HILL    HILL    HL  HL  HILLS    HILLS    HLS  HLS  HOLLOW    HLLW    HOLW  HOLLOW  HOLLOWS  HOLW  HOLWS  INLET    INLT    INLT  ISLAND    IS    IS  ISLAND  ISLND  ISLANDS    ISLANDS    ISS  ISLNDS  ISS  ISLE    ISLE    ISLE  ISLES  JUNCTION    JCT    JCT  JCTION  JCTN  JUNCTION  JUNCTN  JUNCTON  JUNCTIONS    JCTNS    JCTS  JCTS  JUNCTIONS  KEY    KEY    KY  KY  KEYS    KEYS    KYS  KYS  KNOLL    KNL    KNL  KNOL  KNOLL  KNOLLS    KNLS    KNLS  KNOLLS  LAKE    LK    LK  LAKE  LAKES    LKS    LKS  LAKES  LAND    LAND    LAND  LANDING    LANDING    LNDG  LNDG  LNDNG  LANE    LANE    LN  LN  LIGHT    LGT    LGT  LIGHT  LIGHTS    LIGHTS    LGTS  LOAF    LF    LF  LOAF  LOCK    LCK    LCK  LOCK  LOCKS    LCKS    LCKS  LOCKS  LODGE    LDG    LDG  LDGE  LODG  LODGE  LOOP    LOOP    LOOP  LOOPS  MALL    MALL    MALL  MANOR    MNR    MNR  MANOR  MANORS    MANORS    MNRS  MNRS  MEADOW    MEADOW    MDW  MEADOWS    MDW    MDWS  MDWS  MEADOWS  MEDOWS  MEWS    MEWS    MEWS  MILL    MILL    ML  MILLS    MILLS    MLS  MISSION    MISSN    MSN  MSSN  MOTORWAY    MOTORWAY    MTWY  MOUNT    MNT    MT  MT  MOUNT  MOUNTAIN    MNTAIN    MTN  MNTN  MOUNTAIN  MOUNTIN  MTIN  MTN  MOUNTAINS    MNTNS    MTNS  MOUNTAINS  NECK    NCK    NCK  NECK  ORCHARD    ORCH    ORCH  ORCHARD  ORCHRD  OVAL    OVAL    OVAL  OVL  OVERPASS    OVERPASS    OPAS  PARK    PARK    PARK  PRK  PARKS    PARKS    PARK  PARKWAY    PARKWAY    PKWY  PARKWY  PKWAY  PKWY  PKY  PARKWAYS    PARKWAYS    PKWY  PKWYS  PASS    PASS    PASS  PASSAGE    PASSAGE    PSGE  PATH    PATH    PATH  PATHS  PIKE    PIKE    PIKE  PIKES  PINE    PINE    PNE  PINES    PINES    PNES  PNES  PLACE    PL    PL  PLAIN    PLAIN    PLN  PLN  PLAINS    PLAINS    PLNS  PLNS  PLAZA    PLAZA    PLZ  PLZ  PLZA  POINT    POINT    PT  PT  POINTS    POINTS    PTS  PTS  PORT    PORT    PRT  PRT  PORTS    PORTS    PRTS  PRTS  PRAIRIE    PR    PR  PRAIRIE  PRR  RADIAL    RAD    RADL  RADIAL  RADIEL  RADL  RAMP    RAMP    RAMP  RANCH    RANCH    RNCH  RANCHES  RNCH  RNCHS  RAPID    RAPID    RPD  RPD  RAPIDS    RAPIDS    RPDS  RPDS  REST    REST    RST  RST  RIDGE    RDG    RDG  RDGE  RIDGE  RIDGES    RDGS    RDGS  RIDGES  RIVER    RIV    RIV  RIVER  RVR  RIVR  ROAD    RD    RD  ROAD  ROADS    ROADS    RDS  RDS  ROUTE    ROUTE    RTE  ROW    ROW    ROW  RUE    RUE    RUE  RUN    RUN    RUN  SHOAL    SHL    SHL  SHOAL  SHOALS    SHLS    SHLS  SHOALS  SHORE    SHOAR    SHR  SHORE  SHR  SHORES    SHOARS    SHRS  SHORES  SHRS  SKYWAY    SKYWAY    SKWY  SPRING    SPG    SPG  SPNG  SPRING  SPRNG  SPRINGS    SPGS    SPGS  SPNGS  SPRINGS  SPRNGS  SPUR    SPUR    SPUR  SPURS    SPURS    SPUR  SQUARE    SQ    SQ  SQR  SQRE  SQU  SQUARE  SQUARES    SQRS    SQS  SQUARES  STATION    STA    STA  STATION  STATN  STN  STRAVENUE    STRA    STRA  STRAV  STRAVEN  STRAVENUE  STRAVN  STRVN  STRVNUE  STREAM    STREAM    STRM  STREME  STRM  STREET    STREET    ST  STRT  ST  STR  STREETS    STREETS    STS  SUMMIT    SMT    SMT  SUMIT  SUMITT  SUMMIT  TERRACE    TER    TER  TERR  TERRACE  THROUGHWAY    THROUGHWAY    TRWY  TRACE    TRACE    TRCE  TRACES  TRCE  TRACK    TRACK    TRAK  TRACKS  TRAK  TRK  TRKS  TRAFFICWAY    TRAFFICWAY    TRFY  TRAIL    TRAIL    TRL  TRAILS  TRL  TRLS  TRAILER    TRAILER    TRLR  TRLR  TRLRS  TUNNEL    TUNEL    TUNL  TUNL  TUNLS  TUNNEL  TUNNELS  TUNNL  TURNPIKE    TRNPK    TPKE  TURNPIKE  TURNPK  UNDERPASS    UNDERPASS    UPAS  UNION    UN    UN  UNION  UNIONS    UNIONS    UNS  VALLEY    VALLEY    VLY  VALLY  VLLY  VLY  VALLEYS    VALLEYS    VLYS  VLYS  VIADUCT    VDCT    VIA  VIA  VIADCT  VIADUCT  VIEW    VIEW    VW  VW  VIEWS    VIEWS    VWS  VWS  VILLAGE    VILL    VLG  VILLAG  VILLAGE  VILLG  VILLIAGE  VLG  VILLAGES    VILLAGES    VLGS  VLGS  VILLE    VILLE    VL  VL  VISTA    VIS    VIS  VIST  VISTA  VST  VSTA  WALK    WALK    WALK  WALKS    WALKS    WALK  WALL    WALL    WALL  WAY    WY    WAY  WAY  WAYS    WAYS    WAYS  WELL WL  WELLS WLS "

        # process street suffixes copy pasted from USPS website into something that can be used with regex and spacy patterns
        sts = street_copypaste.split(' ')
        street_labels = ""
        for s in sts:
            if (s != ""):
                street_labels = street_labels + s + "|"
        street_labels = street_labels.lower()
        street_labels = street_labels[0:-1]

        # first priority patterns
        patterns_check1 = [
            [{"IS_DIGIT": True},{"TEXT": {"REGEX": ".*"}},{"TEXT": {"REGEX": ".*"}},{"TEXT": {"REGEX": '^('+street_labels+')$'}}],
            [{"TEXT": {"REGEX": "[a-z]*"}}, {"TEXT":","}, {"TEXT": {"REGEX": "[a-z]*"}}, {"TEXT": {"REGEX": "[0-9]{5}"}}, {"IS_PUNCT":True}, {"TEXT": {"REGEX": "[0-9]{4}"}}]        
        ]
        
        # second priority patterns
        patterns_check2 = [
            [{"IS_DIGIT": True},{"TEXT": {"REGEX": ".*"}},{"TEXT": {"REGEX": '^('+street_labels+')$'}}],
            [{"TEXT": {"REGEX": "[a-z]*"}}, {"TEXT":","}, {"TEXT": {"REGEX": "[a-z]*"}}, {"TEXT": {"REGEX": "[0-9]{5}"}}],
            [{"TEXT": {"REGEX": "[a-z]*"}}, {"TEXT":","}, {"TEXT": {"REGEX": "[a-z]*"}}, {"IS_SPACE":True},{"TEXT": {"REGEX": "[0-9]{5}"}}] # edge case if two spaces before zipcode
        ]

        # find matches for patterns
        matches_check1 = find_spacy_matches(inp.input_str, patterns_check1)
        matches_check2 = find_spacy_matches(inp.input_str, patterns_check2)

        # merges different prioty lists and adds redacts to object
        addy = merge_lists(matches_check1, matches_check2)
        inp.add_redact(addy, "address")

def redact_concepts(input_files, concept):
    """Function to redact concepts."""
    for inp in input_files:
        doc = nlp(inp.input_str)
        similar = []
        sentences = []
        sent_added = set()
        for c in concept:
            nlp_concept = nlp(c)
            # compares concept word to words in document for similarity
            # if the similarity is above a threshold, adds to redactions
            if(nlp_concept and nlp_concept.vector_norm): # checks for valid word vector
                """Function to ."""
                for token in doc:
                    if (token and token.vector_norm): # checks for valid word vector
                        simil = nlp_concept.similarity(token)
                        if (simil > 0.5):
                            #print(f"{token}--{simil}--{token.i}")
                            similar.append([token.text, token.sent.start_char, token.sent.end_char]) # token text, sentence start char, sentence end char

            # only adds one redaction per sentence, there may be multiple concepts in a sentence but increases stats based on # of sentences
            for similar_tok in similar:
                """Function to ."""
                if (similar_tok[1] not in sent_added):
                    sent_added.add(similar_tok[1])
                    sentences.append(similar_tok)
        inp.add_redact(sentences, "concept")

def find_spacy_matches(input_str, patterns):
    """Function to make a spacy pattern and find matches."""
    doc = nlp(input_str.lower())
    matches_return = []
    # create matcher and add patterns
    matcher = spacy.matcher.Matcher(nlp.vocab) 
    matcher.add("patterns",patterns)

    # adds each match to a list and returns it
    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]  # The matched span
        if ((re.search(r"@",span.text) == None)):
            matches_return.append([span.text,doc[start].idx,doc[start].idx+len(span.text)])
    
    return(matches_return)

def merge_lists(list1, list2):
    """Function to merge two lists and remove any overlapping words."""
    merged = list1.copy()
    list1_range = range(len(list1))

    # list 1 has priority and if one term is in list 1 as "John Doe" and in list 2 as "John" at nearby indexes
    # will only add "John Doe"
    for item in list2:
        skip_flag = False
        item_len = item[2]-item[1]

        for i in list1_range:
            len_i = list1[i][2]-list1[i][1]
            if ((item[1]==list1[i][1]) or (item[1]+item_len+1==list1[i][1]) or (list1[i][1]+len_i+1==item[1])): # checks nearby indexes based on string length
                skip_flag = True
                break
        
        if (not skip_flag):
            merged.append(item)

    return merged

def find_regex(reg_set, input_str, ignore_case):
    """Function to find regex matches based on set of regex patterns."""
    matches = []
    for reg in reg_set:
        if (ignore_case): # ignores case
            iter = re.finditer(reg, input_str, re.IGNORECASE) # pattern, string, flags
        else: # looks for case differences
            iter = re.finditer(reg, input_str) # pattern, string, flags
        for match in iter:
            matches.append([match.group(), match.span()[0], match.span()[1]]) # string text, dx from start, string end char 

    return matches   