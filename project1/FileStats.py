class FileStats:
    def __init__(self, file_name, input_str):
        self.file_name = file_name
        self.input_str = input_str
        self.output_str = input_str
        self.redact_indexes = set({})
        self.redact_stats = {
            "names": 0,
            "genders": 0,
            "dates": 0,
            "phones": 0,
            "address": 0,
            "concept": 0
        }
    
    def add_redact(self, redactions, redact_type):
        for redact in redactions:
            for index in range(redact[1], redact[2]):
                self.redact_indexes.add(index)
            new_value = self.redact_stats[redact_type]+1
            self.redact_stats.update({redact_type: new_value})

    def stats_strings(self):
        return [self.file_name, self.input_str, self.output_str]

    def formatted_stats_string(self):
        return (
            f"Filename: {self.file_name}\n"
            f"Redaction Indexes: {self.redact_indexes}\n"
            f"Redaction Stats:\n"
            f"\tnames:   {self.redact_stats['names']}\n"
            f"\tgenders: {self.redact_stats['genders']}\n"
            f"\tdates:   {self.redact_stats['dates']}\n"
            f"\tphones:  {self.redact_stats['phones']}\n"
            f"\taddress: {self.redact_stats['address']}\n"
            f"\tconcept: {self.redact_stats['concept']}\n"
        )

    def redact_output_str(self):
        output_str = self.output_str
        for index in self.redact_indexes:
            output_str = output_str[:index] + "\u2588" + output_str[index+1:]
        
        self.output_str = output_str
        