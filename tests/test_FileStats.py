from project1 import FileStats

def test_FileStats():
    # check FileStates init function
    test_stats = FileStats.FileStats("filename", "This is a sample text string written by John Smith.")
    stats_expected = {"names": 0,"genders": 0,"dates": 0,"phones": 0,"address": 0,"concept": 0}
    assert (test_stats != None) # checks to see if a FileStats object has been created
    assert (test_stats.file_name == "filename") # checks that filename was assigned correctly
    assert (test_stats.input_str == "This is a sample text string written by John Smith.") # checks that input_str was assigned correctly
    assert (test_stats.output_str == "This is a sample text string written by John Smith.") # checks that output_str was set equal to input_str
    assert (test_stats.redact_indexes == set({})) # checks that redact_indexes is initalized as an empty set
    assert (test_stats.redact_stats == stats_expected) # checks that redact_stats is set to 0 for all stats categories

    # check add_redact function
    redactions = [["John Smith", 40, 50]] # test redaction of removing name
    test_stats.add_redact(redactions, "names") # adds redaction
    redactstats_expected = {"names": 1,"genders": 0,"dates": 0,"phones": 0,"address": 0,"concept": 0} # expected new stats
    redactindexes_expected = {40,41,42,43,44,45,46,47,48,49} # expected redaction indexes

    assert(test_stats.redact_indexes == redactindexes_expected) # check that expected matches
    assert(test_stats.redact_stats == redactstats_expected) # check that expected matches

    # check redact output
    redactout_expected = "This is a sample text string written by \u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588."
    test_stats.redact_output_str()
    assert (test_stats.output_str == redactout_expected)

    # check stats_strings function
    statsstring_expected = ["filename", "This is a sample text string written by John Smith.",
                            "This is a sample text string written by \u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588."]
    statsstring_actual = test_stats.stats_strings()
    assert (statsstring_actual == statsstring_expected) # checks formatted string list matches expected

    # check formatted_stats_string function
    statsformatted_expected = (
            "Filename: filename\n"
            "Redaction Indexes: {40, 41, 42, 43, 44, 45, 46, 47, 48, 49}\n"
            "Redaction Stats:\n"
            "\tnames:   1\n"
            "\tgenders: 0\n"
            "\tdates:   0\n"
            "\tphones:  0\n"
            "\taddress: 0\n"
            "\tconcept: 0\n")
    statsformatted_actual = test_stats.formatted_stats_string() # gets expected formatted string
    assert (statsformatted_actual == statsformatted_expected) # checks formatted string list matches expected