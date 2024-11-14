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

    def compute_costs(self):
        """Compute individual costs based on constraints."""
        batch_cost = 0
        lot_change_cost = 0
        rolling_window_cost = 0
        two_tone_cost = 0
        resequencing_cost = self.parameters.get('resequencing_cost', 0)

        for constraint in self.constraints:
            cost = constraint.get("cost", 0)

            if constraint['type'] == 'batch_size':
                for shop_name, sequences in self.solution.items():
                    if shop_name == constraint['shop']:
                        batch_count = 0
                        for vehicle in sequences['entry']:
                            if vehicle in constraint['vehicles']:
                                batch_count += 1
                            if batch_count > constraint['max_vehicles']:
                                batch_cost += constraint['cost']
                                batch_count = 0

            elif constraint['type'] == 'lot_change':
                for shop_name, sequences in self.solution.items():
                    if shop_name == constraint['shop']:
                        current_partition = None
                        for vehicle in sequences['entry']:
                            for partition in constraint['partition']:
                                if vehicle in partition:
                                    if current_partition is not None and current_partition != partition:
                                        lot_change_cost += constraint['cost']
                                    current_partition = partition
                                    break

            elif constraint['type'] == 'rolling_window':
                for shop_name, sequences in self.solution.items():
                    if shop_name == constraint['shop']:
                        window_count = 0
                        for i in range(len(sequences['entry'])):
                            if sequences['entry'][i] in constraint['vehicles']:
                                window_count += 1
                            if window_count > constraint['max_vehicles']:
                                rolling_window_cost += constraint['cost']
                                window_count = 0
                            if i >= constraint['window_size'] and sequences['entry'][i - constraint['window_size']] in constraint['vehicles']:
                                window_count -= 1

        # Calculate two-tone cost
        two_tone_delta = self.parser.parameters.get('two_tone_delta', 0)
        for shop_name, sequences in self.solution.items():
            if shop_name == 'paint':
                for i in range(len(sequences['entry'])):
                    if self.parser.vehicles[sequences['entry'][i]] == 'two-tone':
                        two_tone_cost += two_tone_delta

        # Total cost calculation (sum of all individual costs)
        total_cost = batch_cost + lot_change_cost + rolling_window_cost + two_tone_cost + resequencing_cost # noqa:
        return {
            "batch_cost": batch_cost,
            "lot_change_cost": lot_change_cost,
            "rolling_window_cost": rolling_window_cost,
            "two_tone_cost": two_tone_cost,
            "resequencing_cost": resequencing_cost,
            "total_cost": total_cost
        }
