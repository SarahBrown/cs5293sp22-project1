class FileStats:
    def __init__(self, file_name, input_str):
        self.file_name = file_name
        self.input_str = input_str
        self.redact_indexes = set({})
        self.redact_stats = {
            "names": 0,
            "genders": 0,
            "dates": 0,
            "phones": 0,
            "address": 0,
            "concept": 0
        }
    
    def add_redact(self, redact_index, redact_type):
        for ind in redact_index:
            self.redact_indexes.add(ind)
        new_value = self.redact_stats[redact_type]+1
        self.redact_stats.update({redact_type: new_value})
        print(self.redact_indexes)

    def stats_string(self):
        return [self.file_name, self.input_str, self.redact_indexes, self.redact_stats]