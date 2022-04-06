from project1 import project1
from project1 import FileStats

def test_dates():
    # creates a test FileStats object
    file = open("tests/test_files/dates.txt", "r")
    test_stats = FileStats.FileStats("tests/test_files/dates.txt", file.read())
    file.close()

    # reads in the expected redactions and stores the text in a string
    expected_redactions = "This is a sentence with dates, ████████████████. The project is due ████████████. The thing is on ██████████. ████████████ are ████████████ of the event. ██████████ being ██████████████████████████████████████████████████. The party is on █████████"

    # expected indexes to be redacted based on known test file
    expected_indexes = {31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 98, 99, 100, 101, 102, 103, 104, 105, 106, 
    107, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 
    171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 
    206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 239, 240, 241, 242, 243, 244, 245, 246, 247}

    # finds and indexes addresses for redaction in test file
    project1.redact_dates([test_stats])
    actual_indexes = test_stats.redact_indexes

    # checks expected indexes for redaction against actual indexes for redaction
    assert (expected_indexes == actual_indexes)

    # gets redacted output str
    test_stats.redact_output_str()
    actual_redactions = test_stats.output_str

    # checks expected redaction string against actual
    assert(expected_redactions == actual_redactions)