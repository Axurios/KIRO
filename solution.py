import json
# import parser
# import copy
import numpy as np


def swap(sequence, i, j):
    sequence[i], sequence[j] = sequence[j], sequence[i]


def paint_order(L, vehicles, delta):
    L_entry = L
    index_entry = [i for i in range(len(L_entry))]
    index_exit = []
    L_exit = []
    two_tone_temp = []
    two_tone_temp_time = np.array([])
    two_tone_temp_index = []

    # Convert dictionary items to a list
    vehicles_items = list(vehicles.items())

    for i in range(len(L_entry)):
        if len(two_tone_temp_time) > 0:
            for k in range(len(two_tone_temp_time)):
                if two_tone_temp_time[0] >= delta-1:

                    L_exit.append(two_tone_temp[0])
                    index_exit.append(two_tone_temp_index[0])
                    two_tone_temp = two_tone_temp[1:]
                    two_tone_temp_time = two_tone_temp_time[1:]
                    two_tone_temp_index = two_tone_temp_index[1:]

        # Access the i-th element
        key, value = vehicles_items[i]
        if value == "two-tone":
            two_tone_temp.append(L_entry[i])
            two_tone_temp_time = np.append(two_tone_temp_time, 0)
            two_tone_temp_index.append(index_entry[i])

        else:
            L_exit.append(L_entry[i])
            index_exit.append(index_entry[i])
            two_tone_temp_time += 1

    L_exit = L_exit+two_tone_temp
    index_exit = index_exit+two_tone_temp_index
    return L_entry, L_exit, index_exit


def computeExitPaint(entry, vehicles, delta):
    """
    Given an entry sequence and vehicles dictionary, computes the exit sequence 
    with two-tone vehicles shifted backward by delta.

    :param entry: list of vehicle IDs at the entrance
    :param vehicles: dict mapping vehicle IDs to vehicle types (e.g., 'two-tone')
    :param delta: int, number of positions to move two-tone vehicles backward
    :return: list representing the exit sequence
    """
    # Initial permutation (copy of entry sequence)
    permutation = entry.copy()

    # Determine the exit sequence
    two_tone_indices = [i for i, v in enumerate(permutation) if vehicles.get(v) == "two-tone"]

    # Rearrange each two-tone vehicle backward by delta
    for idx in two_tone_indices:
        # Determine the maximum possible backward shift for this position
        shift_amount = min(delta, idx)

        # Shift the two-tone vehicle backward by swapping positions
        for shift in range(shift_amount):
            swap(permutation, idx - shift, idx - shift - 1)

    # Return the modified sequence for the paint shop, or unchanged for others
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
            print("delta", self.parser.get_parameters())
            Lentry, Lexit, Lindex = paint_order(entry_sequence, self.parser.get_vehicles(), self.parser.get_parameters()['two_tone_delta'])
            self.solution[shop_name] = {
                "entry": entry_sequence,
                "exit": Lexit  #computeExitPaint(entry_sequence, self.parser.get_vehicles(), self.parser.get_parameters()['two_tone_delta'])
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
        c_resequencing = self.parser.get_parameters()['resequencing_cost']

        for constraint in self.parser.constraints:
            match constraint['type']:
                case "batch_size":
                    batch_cost = self.batchCost(constraint)

                case "lot_change":
                    lot_change_cost = self.lotChangeCost(constraint) # noqa:

                case "rolling_window":
                    rolling_window_cost = self.rollingCost(constraint) # noqa:

        

        # Total cost calculation (sum of all individual costs)
        total_cost = batch_cost + lot_change_cost + rolling_window_cost #+ resequencing_cost # + two_tone_cost # noqa:
        return {
            "batch_cost": batch_cost,
            "lot_change_cost": lot_change_cost,
            "rolling_window_cost": rolling_window_cost,
            # "two_tone_cost": two_tone_cost,
            #"resequencing_cost": resequencing_cost,
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
