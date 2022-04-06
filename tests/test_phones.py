from project1 import project1
from project1 import FileStats

def test_phones():
    # creates a test FileStats object
    file = open("tests/test_files/phones.txt", "r")
    test_stats = FileStats.FileStats("tests/test_files/phones.txt", file.read())
    file.close()

    # reads in the expected redactions and stores the text in a string
    expected_redactions = "Joe's phone is ████████████. Jannie's is ██████████████. These phone numbers are random ████████████. They are examples of different formats█████████. These are phones ██████████████ and ███████████████ and also this ████████████."

    # expected indexes to be redacted based on known test file
    expected_indexes = {15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 88, 89, 90, 91, 
    92, 93, 94, 95, 96, 97, 98, 99, 140, 141, 142, 143, 144, 145, 146, 147, 148, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 
    181, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228}

    # finds and indexes addresses for redaction in test file
    project1.redact_phones([test_stats])
    actual_indexes = test_stats.redact_indexes

    # checks expected indexes for redaction against actual indexes for redaction
    assert (expected_indexes == actual_indexes)

    # gets redacted output str
    test_stats.redact_output_str()
    actual_redactions = test_stats.output_str

    # checks expected redaction string against actual
    assert(expected_redactions == actual_redactions)