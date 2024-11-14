import json
# import parser
import copy


def swap(sequence, i, j):
    sequence[i], sequence[j] = sequence[j], sequence[i]


def computeExitPaint(entry, vehicles, delta):
    permutation = copy.deepcopy(entry)
    # liste_2T = [False, False, False, True, True, False, False, True, True, False] # noqa:
    # permutation_exemple1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for j in range(len(permutation)):
        i = len(permutation) - j - 1

        if vehicles[permutation[i]] == "two-tone":
            if i == len(permutation) - 1:
                swap(permutation, i, i-1)

            elif i == len(permutation) - 2:
                swap(permutation, i, i+1)

            elif i > len(permutation) - delta:
                swap(permutation, i, -1)
                swap(permutation, i, i+1)

            else:
                swap(permutation, i, i+2)
                swap(permutation, i, i+1)
    return permutation


class Solution:
    def __init__(self, called_parser):
        self.solution = {}
        self.parser = called_parser

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
                "exit": computeExitPaint(entry_sequence, self.parser.get_vehicles(), self.parser.get_parameters()['two_tone_delta'])
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
        # two_tone_cost = 0
        resequencing_cost = self.parser.get_parameters()['resequencing_cost']

        for constraint in self.parser.constraints:
            match constraint['type']:
                case "batch_size":
                    batch_cost = self.batchCost(constraint)

                case "lot_change":
                    lot_change_cost = self.lotChangeCost(constraint) # noqa:

                case "rolling_window":
                    rolling_window_cost = self.rollingCost(constraint) # noqa:

        # Calculate resequencing cost
        c = self.parser.parameters.get('resequencing_cost', 0)
        resequencing_delays = 0
        for s in range(len(self.solution) - 1):
            shop_s = self.solution[f'shop_{s}']
            shop_s_plus_1 = self.solution[f'shop_{s + 1}']
            for v in shop_s['exit']:
                t_v_minus_1_s = shop_s['exit'].index(v) + 1
                t_v_minus_1_s_plus_1 = shop_s_plus_1['entry'].index(v) + 1
                delay = t_v_minus_1_s_plus_1 - t_v_minus_1_s - self.parser.shops[f'shop_{s}']['resequencing_lag']
                if delay > 0:
                    resequencing_delays += delay
        resequencing_cost = c * resequencing_delays

        # Total cost calculation (sum of all individual costs)
        total_cost = batch_cost + lot_change_cost + rolling_window_cost + resequencing_cost # + two_tone_cost # noqa:
        return {
            "batch_cost": batch_cost,
            "lot_change_cost": lot_change_cost,
            "rolling_window_cost": rolling_window_cost,
            # "two_tone_cost": two_tone_cost,
            "resequencing_cost": resequencing_cost,
            "total_cost": total_cost
        }

    def batchCost(self, constraint):
        batch_cost = 0
        for shop_name, sequences in self.solution.items():
            if shop_name == constraint['shop']:
                batch_count = 0
                for vehicle in sequences['entry']:
                    if vehicle in constraint['vehicles']:
                        batch_count += 1
                        if batch_count > constraint['max_vehicles']:
                            batch_cost += constraint['cost']
                            batch_count = 0
        return batch_cost

    def lotChangeCost(self, constraint):
        lot_change_cost = 0
        for shop_name, sequences in self.solution.items():
            if shop_name == constraint['shop']:
                current_partition = None
                for vehicle in sequences['entry']:
                    for partition in constraint['partition']:
                        if vehicle in partition:
                            if current_partition is not None and current_partition != partition: # noqa:
                                lot_change_cost += constraint['cost']
                                current_partition = partition
                                break
        return lot_change_cost

    def rollingCost(self, constraint):
        rolling_window_cost = 0
        for shop_name, sequences in self.solution.items():
            if shop_name == constraint['shop']:
                window_count = 0
                for i in range(len(sequences['entry'])):
                    if sequences['entry'][i] in constraint['vehicles']:
                        window_count += 1
                    if window_count > constraint['max_vehicles']:
                        rolling_window_cost += constraint['cost']
                        window_count = 0
                    if i >= constraint['window_size'] and sequences['entry'][i - constraint['window_size']] in constraint['vehicles']: # noqa:
                        window_count -= 1
        return rolling_window_cost
