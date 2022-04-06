from project1 import project1
from project1 import FileStats

def test_names():
    # creates a test FileStats object
    file = open("tests/test_files/names.txt", "r")
    test_stats = FileStats.FileStats("tests/test_files/names.txt", file.read())
    file.close()

    # reads in the expected redactions and stores the text in a string
    expected_redactions = "██████████ is a mother, she is a wife of to █████████████. █████ and ████ have two kids, ██████ and █████. There are many different names in their family including their dog ██████."

    # expected indexes to be redacted based on known test file
    expected_indexes = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 178, 179, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 
    56, 176, 177, 59, 60, 61, 62, 63, 69, 70, 71, 72, 89, 90, 91, 92, 93, 94, 100, 101, 102, 103, 104, 174, 175}

    # finds and indexes addresses for redaction in test file
    project1.redact_names([test_stats])
    actual_indexes = test_stats.redact_indexes

    # checks expected indexes for redaction against actual indexes for redaction
    assert (expected_indexes == actual_indexes)

    # gets redacted output str
    test_stats.redact_output_str()
    actual_redactions = test_stats.output_str

    # checks expected redaction string against actual
    assert(expected_redactions == actual_redactions)