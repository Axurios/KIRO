import json
# import parser
from constraint import compute_exit


def compose_permutations(sigma, tau):
    # Initialize the result list for the composition
    composition = [0] * len(sigma)
    for i in range(len(sigma)):
        # Apply tau first, then apply sigma
        composition[i] = sigma[tau[i] - 1]  # Convert to 0-based index
    return composition


def inverse_permutation(sigma):
    # Initialize a list for the inverse permutation
    inverse = [0] * len(sigma)
    # For each element in sigma, put the index in the corresponding place in the inverse
    for i in range(len(sigma)):
        inverse[sigma[i] - 1] = i + 1  # Convert to 1-based index
    return inverse


def swap(sequence, i, j):
    sequence[i], sequence[j] = sequence[j], sequence[i]


# def computeExitPaint(entry, vehicles, delta):
#     # Create a copy of the entry list to avoid modifying it while iterating
#     result = entry[:]

#     # Iterate through the entry list from the end to the start (reverse)
#     for i in range(len(entry) - 1, -1, -1):
#         vehicle_id = entry[i]

#         # If the vehicle is 'two-tone', attempt to move it up (increase its position)
#         if vehicles[vehicle_id] == 'two-tone':
#             # Calculate the maximum allowed shift (delta - 1)
#             max_shift = delta - 1

#             # Try to move the vehicle up by max_shift positions
#             current_pos = i
#             new_pos = current_pos + max_shift

#             # Ensure that we don't go out of bounds
#             if new_pos >= len(entry):
#                 new_pos = len(entry) - 1

#             # Move the vehicle up by swapping it with vehicles ahead of it
#             while new_pos > current_pos:
#                 # Check if the vehicle at the new position is not 'two-tone'
#                 if vehicles[result[new_pos]] != 'two-tone':
#                     # Swap the two vehicles
#                     result[current_pos], result[new_pos] = result[new_pos], result[current_pos]
#                     current_pos = new_pos
#                 else:
#                     # If it's a two-tone vehicle, stop and leave the current position unchanged
#                     break

#     return result

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
            print(entry_sequence)
            print(self.parser.get_vehicles())
            self.solution[shop_name] = {
                "entry": entry_sequence,
                "exit": compute_exit(entry=entry_sequence, vehicles=self.parser.get_vehicles(), delta=self.parser.get_parameters()['two_tone_delta'])
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

        # Calculate resequencing cost
        resequencing_delays = 0
        # for shop_name, sequences in self.solution.items():
        shop_names = list(self.solution.keys())
        for s in range(len(shop_names) - 1):
            shop_s = self.solution[shop_names[s]]
            shop_s_plus_1 = self.solution[shop_names[s + 1]]
            for v in shop_s['exit']:
                t_v_minus_1_s = shop_s['exit'].index(v) + 1
                t_v_minus_1_s_plus_1 = shop_s_plus_1['entry'].index(v) + 1
                # print("ok" , self.parser.shops[shop_names[s]])
                delay = t_v_minus_1_s_plus_1 - t_v_minus_1_s - self.parser.shops[shop_names[s]]
                if delay > 0:
                    resequencing_delays += delay
        resequencing_cost = resequencing_delays * c_resequencing

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
