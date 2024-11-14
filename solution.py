import json


class Solution:
    def __init__(self):
        self.solution = {}

    def add_shop_sequence(self, shop_name, entry_sequence, exit_sequence):
        """Add the entry and exit sequence for a given shop."""
        self.solution[shop_name] = {
            "entry": entry_sequence,
            "exit": exit_sequence
        }

    def to_json(self):
        """Convert the solution to JSON format."""
        return json.dumps(self.solution, indent=4)

    def save_to_file(self, filename):
        """Save the solution as a JSON file."""
        with open(filename, 'w') as file:
            json.dump(self.solution, file, indent=4)
