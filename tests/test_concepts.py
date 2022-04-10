from project1 import project1
from project1 import FileStats

def test_concepts():
    # creates a test FileStats object
    file = open("tests/test_files/concepts.txt", "r")
    test_stats = FileStats.FileStats("tests/test_files/concepts.txt", file.read())
    file.close()

    # reads in the expected redactions and stores the text in a string
    expected_redactions = "This is a test with a concept, the concept is in the next two sentences. ██████████████████████████████████████████████ ███████████████████████"

    # expected indexes to be redacted based on known test file
    expected_indexes = {128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 
    92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 120, 121, 122, 123, 124, 125, 126, 127}

    # finds and indexes addresses for redaction in test file
    project1.redact_concepts([test_stats],["pet"])
    actual_indexes = test_stats.redact_indexes

    # checks expected indexes for redaction against actual indexes for redaction
    assert (expected_indexes == actual_indexes)

    # gets redacted output str
    test_stats.redact_output_str()
    actual_redactions = test_stats.output_str

    # checks expected redaction string against actual
    assert(expected_redactions == actual_redactions)