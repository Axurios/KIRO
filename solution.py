import json


def computeExitPaint(entry, vehicles):
    exit = []
    return exit

# liste_2T = [False, False, False, True, True, False, False, True, True, False]
# permutation_exemple1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# def swap_paint(permutation, delta = 3):
#   for j in range(len(permutation)):
#     i = len(permutation) - j - 1

#     if liste_2T[permutation[i]]:
#       if i == len(permutation) - 1:
#         swap(permutation, i, i-1)

#       elif i == len(permutation) - 2:
#         swap(permutation, i, i+1)

#       elif i > len(permutation) - delta:
#         swap(permutation, i, -1)
#         swap(permutation, i, i+1)

#       else:
#         swap(permutation, i, i+2)
#         swap(permutation, i, i+1)
#   return permutation


class Solution:
    def __init__(self, parser):
        self.solution = {}
        self.parser = parser

    # def add_shop_sequence(self, shop_name, entry_sequence, exit_sequence):
    #     """Add the entry and exit sequence for a given shop."""
    #     self.solution[shop_name] = {
    #         "entry": entry_sequence,
    #         "exit": exit_sequence
    #     }

    def add_shop_entry(self, shop_name, entry_sequence):
        if shop_name != "paint":
            self.solution[shop_name] = {
                "entry": entry_sequence,
                "exit": entry_sequence
            }
        if shop_name == "paint":
            self.solution[shop_name] = {
                "entry": entry_sequence,
                "exit": computeExitPaint(entry_sequence, self.parser.get_vehicles()) # noqa:
            }

    # is useless :
    def isViable(self):
        """Check that non-paint shops have identical entry and exit lists."""
        for shop_name, sequences in self.solution.items():
            # If it's not a paint shop, entry and exit should be identical
            if shop_name != "paint":
                if sequences["entry"] != sequences["exit"]:
                    return False
        return True

    def to_json(self):
        """Convert the solution to JSON format."""
        return json.dumps(self.solution, indent=4)

    def save_to_file(self, filename):
        """Save the solution as a JSON file."""
        with open(filename, 'w') as file:
            json.dump(self.solution, file, indent=4)
