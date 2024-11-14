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
                # Example placeholder calculation for batch size constraint
                min_vehicles = constraint.get('min_vehicles', 0)
                max_vehicles = constraint.get('max_vehicles', 0)
                batch_cost += cost * (max_vehicles - min_vehicles)

            elif constraint['type'] == 'lot_change':
                # Example placeholder calculation for lot change constraint
                lot_change_cost += cost  # Directly add cost for demonstration

            elif constraint['type'] == 'rolling_window':
                # Example placeholder calculation for rolling window constraint
                max_vehicles = constraint.get('max_vehicles', 0)
                window_size = constraint.get('window_size', 0)
                rolling_window_cost += cost * (window_size - max_vehicles)

            elif constraint['type'] == 'two_tone':
                # Example placeholder calculation for two-tone constraint
                two_tone_cost += cost

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
