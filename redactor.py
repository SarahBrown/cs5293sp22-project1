import argparse
import glob

from project1 import project1
from project1 import FileStats

def add_arguments():
    """Function to add and parse arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True, 
                            help="Glob of local files stored in resources folder.")

    parser.add_argument("--output", type=str, required=True, 
                        help="Output file or special files (stderr, stdout) to store redacted files.")
                        
    parser.add_argument("--stats", type=str, 
                        help="Name of file or special files (stderr, stdout) to write summary of redaction process to.")

    parser.add_argument("--concept", type=str, 
                        help="Word that represents a concept to redact.")
                        
    parser.add_argument("--names", action='store_true', 
                        help=".")

    parser.add_argument("--genders", action='store_true', 
                        help=".")
        
    parser.add_argument("--dates", action='store_true',  
                        help=".")

    parser.add_argument("--phones", action='store_true', 
                        help=".")

    parser.add_argument("--address", action='store_true', 
                        help="Flag .")
        
    args = parser.parse_args()

    return args

def get_inputfiles(input_glob):
    files = glob.glob(input_glob)
    file_list = []

    for f in files:
        file = open(f, "r")
        new_file = FileStats.FileStats(f, file.read())
        file_list.append(new_file)
        file.close()

    return file_list

def redact(args, input_file):
    if (args.names): # checks names flag to see if true
        input_file = project1.redact_names(input_file)

    if (args.genders):
        input_file = project1.redact_genders(input_file)

    if (args.dates):
        input_file = project1.redact_dates(input_file)

    if (args.phones):
        input_file = project1.redact_phones(input_file)

    if (args.address):
        input_file = project1.redact_address(input_file)

    if (args.concept):
        input_file = project1.redact_concepts(input_file, args.concept)

stats = []

args = add_arguments()
input_files = get_inputfiles(args.input)

input_files = redact(args, input_files)

if (args.stats):
    for inp in input_files:
        print(inp.stats_string())