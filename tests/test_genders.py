from project1 import project1
from project1 import FileStats

def test_genders():
    # creates a test FileStats object
    file = open("tests/test_files/genders.txt", "r")
    test_stats = FileStats.FileStats("tests/test_files/genders.txt", file.read())
    file.close()

    # reads in the expected redactions and stores the text in a string
    expected_redactions = "Jane is a ██████, ███ is a ████ of a ███ who is ███ ███████. ██ is a ██████ to their ████████ and to their ███. These are gendered terms like ████ and █████."

    # expected indexes to be redacted based on known test file
    expected_indexes = {10, 11, 12, 13, 14, 15, 142, 143, 144, 145, 18, 19, 20, 151, 152, 153, 154, 27, 28, 29, 30, 155, 37, 38, 39, 
    48, 49, 50, 52, 53, 54, 55, 56, 57, 58, 61, 62, 69, 70, 71, 72, 73, 74, 85, 86, 87, 88, 89, 90, 91, 92, 107, 108, 109}

    # finds and indexes addresses for redaction in test file
    project1.redact_genders([test_stats])
    actual_indexes = test_stats.redact_indexes

    # checks expected indexes for redaction against actual indexes for redaction
    assert (expected_indexes == actual_indexes)

    # gets redacted output str
    test_stats.redact_output_str()
    actual_redactions = test_stats.output_str

    # checks expected redaction string against actual
    assert(expected_redactions == actual_redactions)