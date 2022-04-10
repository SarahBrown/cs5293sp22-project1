import argparse
import glob
import sys
import os

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

    parser.add_argument("--concept", type=str,action="append",
                        help="Word that represents a concept to redact.")
                        
    parser.add_argument("--names", action='store_true', 
                        help="Boolean flag to redact names.")

    parser.add_argument("--genders", action='store_true', 
                        help="Boolean flag to redact genders.")
        
    parser.add_argument("--dates", action='store_true',  
                        help="Boolean flag to redact dates.")

    parser.add_argument("--phones", action='store_true', 
                        help="Boolean flag to redact phones.")

    parser.add_argument("--address", action='store_true', 
                        help="Boolean flag to redact address.")
        
    # get and return args
    args = parser.parse_args()
    return args

def get_inputfiles(input_glob):
    """Function to process glob and add input files."""
    files = sorted(glob.glob(input_glob)) # reads in glob files and sorts them alphabetically for ease of debugging
    file_list = []

    # opens each file in glob and creates a FileStats object to hold its details
    for f in files:
        file = open(f, "r") 
        new_file = FileStats.FileStats(f, file.read()) # creates FileStats obj
        file_list.append(new_file) # adds to list of files
        file.close()

    return file_list # returns list

def redact(args, input_file):
    """Function to process args and redact requested redactions."""
    if (args.names): # checks names flag to see if true
        project1.redact_names(input_file)

    if (args.genders): # checks genders flag to see if true
        project1.redact_genders(input_file)

    if (args.dates): # checks dates flag to see if true
        project1.redact_dates(input_file)

    if (args.phones): # checks phones flag to see if true
        project1.redact_phones(input_file)

    if (args.address): # checks address flag to see if true
        project1.redact_address(input_file)

    if (args.concept): # checks concept flag to see if true
        project1.redact_concepts(input_file, args.concept)
    
    for inp in input_file:
        inp.redact_output_str() # perform redactions with indexes found in redact functions

"""Automatic redactor to redact certain terms/concepts based on user input."""
# adds arguments, inputfiles, and performs redaction
args = add_arguments()
input_files = get_inputfiles(args.input)
redact(args, input_files)

# processes the output flag
if (args.output):
    for inp in input_files:
        if (args.output == 'stderr'):
            sys.stderr.write(inp.output_str) # writes to std error
        elif (args.output == 'stdout'):
            sys.stdout.write(inp.output_str) # writes to std output
        else:
            if (not os.path.exists(args.output)): # checks that the output folder exists
                os.mkdir(args.output)
            out_filename = (f"{args.output}/{inp.file_name.split('/')[-1]}.redacted")
            if os.path.exists(out_filename):
                os.remove(out_filename)
            output_file = open(out_filename,"x")
            output_file.write(inp.output_str)
            output_file.close()

# processes the stats flag
if (args.stats):
    if (args.stats == 'stderr' or args.stats == 'stdout'):
        for inp in input_files:
            if (args.stats == 'stderr'):
                sys.stderr.write(inp.formatted_stats_string())  # writes to std error
            elif (args.stats == 'stdout'):
                sys.stdout.write(inp.formatted_stats_string()) # writes to std output
    else:
        # creates and writes to stats file
        out_filename = f"{args.stats}" 
        if os.path.exists(out_filename):
            os.remove(out_filename)
        output_file = open(out_filename,"x")
        for inp in input_files:
            output_file.write(inp.formatted_stats_string())
        output_file.close()