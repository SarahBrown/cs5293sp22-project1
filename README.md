# cs5293sp22-project1

### Author: Sarah Brown

# Directions to Install and Use Package
To download and use package, follow the steps below:

1. git clone https://github.com/SarahBrown/cs5293sp22-project1.git
2. cd cs5293sp22-project1/
3. pipenv install
4. Install models used with NLTK. Unfortunately, NLTK data must be downloaded via its downloader and cannot be done via pip/pipenv. The following command will download all necessary parts to run redactor.py
* pipenv run python project1/nltk_modules.py

5. 
pipenv run python redactor.py --input 'resources/*.txt' \
                    --names --dates --phones --genders --address\
                    --concept 'kids' \
                    --output 'files/' \
                    --stats stderr

# Web or External Libraries
For this project I used several packages from the standard library and some external libraries. These included argparse, glob, os, re, and sys. In addition, the external libraries that were imported included spacy and its model en_core_web_lg. In addition, I also imported nltk and its models punkt, averaged_perceptron_tagger, maxent_ne_chunker, and words.

# Functions and Approach to Development
This project uses various functions to filter to terms/concepts, redact information, and return output/stats data.

## Redaction Flags
This project uses argparse and a variety of arguments to process user input. The following are the flags used and their parameters:
* --input. type=str, required=True, help="Glob of local files stored in resources folder."
* --output. type=str, required=True, help="Output file or special files (stderr, stdout) to store redacted files."
* --stats.type=str, help="Word that represents a concept to redact."
* --concept. type=str, action="append",help="Word that represents a concept to redact.
* --names. action='store_true', help="Boolean flag to redact names.
* --genders. action='store_true', help="Boolean flag to redact genders.
* --dates. action='store_true', help="Boolean flag to redact dates.
* --phones. action='store_true', help="Boolean flag to redact phones.
* --address. action='store_true', help="Boolean flag to redact address.

### Redaction of Whitespace
Whitespace is redacted between first and last names, e.g. John Smith. This is done to further redact information about the document. However, some address patterns do not redact whitespace between the street address and the City, State Zipcode portions of the address. This is done to avoid Regex errors when processing.

## Concepts
Concepets are defined to be a singular word that represents an idea. This word is then compared against other words in the input document to determine similarity. If the similarity passes a given threshold (0.5) they are declared to be a match. This similarity is found via Spacy's similarity function. For more descriptive words like "trade" in a document discussing trade and comodity, this works very effectively. However, sometimes with less specific words this can cause some aspect of randomness. To combat this, the statistics count for concepts is only updated once per sentence redacted instead of once per concept match found.

## Stats
The output of the stats file is shown below. The stats file output has an entry per input file that contains information on the input filename, the indexes of the input string to redact, and the number of times that each flag was redacted. As listed above, concept is counted once per sentence redacted instead of once per concept matched. 
    "Filename: filename\n"
    "Redaction Indexes: {}\n"
    "Redaction Stats:\n"
    "\tnames:   0\n"
    "\tgenders: 0\n"
    "\tdates:   0\n"
    "\tphones:  0\n"
    "\taddress: 0\n"
    "\tconcept: 0\n")

### FileStats.py
To make it easier to store stats information as well as keep track of which string indexes to redact, I created FileStats.py. In this python class, I store the filename, the input string, the redacted output string, the redaction indexes, and the redaction stats. In addition to storing this information in one spot, this class has functions to format output strings of various types, add redaction indexes, and create the redacted string.

## Functions
### redact_names(input_files)
The redact names function takes in a list of FileStats objects and processes them one at a time. This function makes three different passes over the input document to try and find names and then combines the various lists at the end of the function. The first pass that is done is done with Spacy's NER and looks for entities that are labeled as a PERSON. A small ammount of filtering is then done to remove any newlines or emails from the results. In addition, if there are any extra spaces in the found entity text, they are removed to make redaction clearer. 

Next, NER is used again but isntead of looking for entities in the whole document, the document is tokenized and each token is then passed through the process one at a time to see if there are any PERSON entities that were missed. These first two lists are then merged using the merge_lists function (described later below). 

Finally, the NLTK library is then used and the document is again tokenized and the labels are checked for PERSON. These identified tokens and the merged lists from the first two methods are then combined together into a set of regular expression terms. A search is then done with the re library and searches for any additional matches found with the first three methods. Between all  of these processes, a majority of names are identified correctly. These names are then added back into the respective FileStats object in the form of string indexes to redact.

### redact_genders(input_files)
The redact genders function takes in a list of FileStats objects and processes them one at a time. This function matches gendered terms and pronouns to words in the input string via regular expressions. These terms were taken from a list of gendered terms in the english language (https://www.iluenglish.com/gender-in-english-masculine-and-feminine-words/). These terms are then passed into a find_regex() function (described later below), which returns a list. This list is then used to redact the terms via the FileStats's function add_redact().

### redact_dates(input_files)
The redact dates function takes in a list of FileStats objects and processes them one at a time. This functions matches regex patterns for two different date formats and combines it with a list generated via Spacy's NER. The NER searches for labels that match DATE. These lists are combined like previous lists have been with the merge_lists function. The final result is then passed back to FileStats and added to the redaction statistics. 

### redact_phones(input_files)
The redact phones function takes in a list of FileStats objects and processes them one at a time. Phone number patterns are matched via regex and are found with the find_regex() function. Phone numbers are assumed to be US phone numbers for ease of processing. Additional assumptions are described below in the assumptions section.

### redact_address(input_files)
The redact address function takes in a list of FileStats objects and processes them one at a time. The addresses are processed with Spacy pattern matching. These are done with a combination of regex and street suffixes and abbreviations. A list of common abbreviations are process from a USPS website (https://pe.usps.com/text/pub28/28apc_002.htm) and put into a format where they are all OR-ed together in one regex expression. This regex expression serves as the end of a pattern to identify street addresses. This is paired with the pattern starting with some number. In addition, a pattern is also provided to search for CITY, STATE ZIPCODE formats. Combined, this results in a good coverage of US standard addresses. No support is provided for non-US formatted addresses.

### redact_concepts(input_files, concept)
The redact concepts function takes in a list of FileStats objects and processes them one at a time. This function takes the input concept and processes it with spacy's nlp. Then the concept and a token in the input string document are compared and if their similarity is above a threshold of 0.5, they are declared a match. However, to account for some concepts being more vague, the stats count for concepts is only incremented once per each sentence that is redacted. Since a whole sentence is redacted instead of just the one word, this helps cover some of the overlap that may occur due to non-specific concepts. The similar sentences are then added to the redacted indexes and stats.

### find_spacy_matches(input_str, patterns)
The find spacy matches function takes in a an input_str and a list of patterns. It then creates a spacy matcher object and adds the patterns to said object. This matcher is then applied to the input_str and the matches and their indexes are returned.

### merge_lists(list1, list2)
The merge lists function takes in a pair of lists and merges them together. This is done to add different results from various lists together, but is also done to allow priority of one list over the other. List 1 has priority and if one term is in list 1 as "John Doe" and in list 2 as "John" at nearby indexes will only add "John Doe". This priority helps avoid duplicate matches.

### find_regex(reg_set, input_str, ignore_case)
The find regex function takes in a set of regex terms, an input string, and a boolean for whether to ignore case. This function then loops through each term in the regex set and adds any matches to a list. If the boolean is set to ignore case, an IGNORECASE flag is added to the re.finditer.

# Assumptions Made and Known Bugs
## Known Bugs
Due to the addition of NLTK to the redact_names function, it is more likely that words that are not definitely names will be redacted. However, the improved accuracy of getting all of the names outweighs the risk of accidentally getting some non-names. In particular, this bug is directed towards proper nouns as the tagging is based off of those. This issue does not impact performance.

When running pytests there are warnings that are shown due to deprecation and spacy, as these do not impact the tests they are ignored.

## Assumptions About Names
Emails are ignored with regards to names even though they may contain some information regarding names. In addition, names are assumed to be Proper Nouns and as such are case sensitive. Names may still be found even if they are lowercase, but priority is centered on properly capitalized names.

## Assumptions About Genders
Terms that can identify genders in this case is assumed to be binary genders of man and woman. Other terms, such as they/them pronouns could also be filtered and redacted, but as a whole these already obfuscate gender and are thus ignored. There are more gendered terms than just the ones included in the redactor, but these are used as a good sample set of commonly used gender terms in the US.

## Assumptions About Dates
Dates are assumed not to include time. One of the regex patterns accounts for an edge case where there are two spaces between the state and the zipcode.

## Assumptions About Phone Numbers
Phone numbers are assumed to be formatted in standard US format. Supported formats are local 7 digit numbers and various forms of full US numbers. Also supported is the 1-800 format. See below for examples of supported formats.
* xxx-xxxx
* xxx xxx xxxx
* xxx-xxx-xxxx
* (xxx) xxx-xxxx
* +x-xxx-xxx-xxx
* x-xxx-xxx-xxx

## Assumptions About Addresses
Addresses are assumed to be uniquely identifiable locations that could roughly pinpoint a destination. This could either be a street address, a city, state zipcode, or a combination of them. For the purposes of this redactor, addresses are assumed to be in US format. 

## Assumptions About Concepts
Concepts are a selected to be a singular word to represent an idea.

# Tests
Tests are performed with PyTest and local data. Tests are also set up with Github Actions and PyTest to run automatically when code is pushed to the repository. 

## Test File Stats
FileStats was tested by confirming that the various functions worked. The functions tested included the init function, the add_redact function, the redact_output_str function, the stats_strings function, and the formatted_stats_string function. These were tested by taking a sample string, "This is a sample text string written by John Smith." and hand redacting the name and passing it in as a name redaction. 

## Test 
The various types of redaction methods were all tested in a very similar way. A FileStats object was created and then used to redact a selected type (address, date, name, etc.). This was then tested against an easy to produce test case where the results could be confirmed by hand. The expected results were compared to the actual results generated to confirm that the tests passed.
