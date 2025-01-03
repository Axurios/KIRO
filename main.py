from parser import dataParser
from solution import Solution
from itertools import permutations
import numpy as np



def calculate_cost_after_permutation(parser, sequence):
    # Create a temporary parser object with the new sequence
    temp_sol = Solution(parser)
    # parser.vehicles = {i: temp_sol.parser.vehicles[i] for i in sequence}
    costs = temp_sol.compute_costs()
    return costs['total_cost']


def find_optimal_permutation(parser):
    vehicles = list(parser.get_vehicles().keys())
    min_cost = float('inf')
    optimal_sequence = None
    i = 0
    for perm in permutations(vehicles):
        print("Attempt n°", i)
        cost = calculate_cost_after_permutation(parser, perm)
        if cost < min_cost:
            min_cost = cost
            optimal_sequence = perm
            print(f"New optimal sequence found: {optimal_sequence} with cost {min_cost}") # noqa :
        i += 1
        if i >= 1000 :
            break

    return optimal_sequence, min_cost


if __name__ == "__main__":
    print("ok")
    # Example usage
    filename = 'Instances/tiny.json'  # Replace with the path to your JSON file # noqa:
    parser = dataParser(filename)

    # Access parsed data
    # print("Shops:", parser.get_shops())
    #  print("Parameters:", parser.get_parameters()['two_tone_delta'])
    #print("Vehicles:", parser.get_vehicles())
    # print("Constraints:", parser.get_constraints())

    # Calculate costs
    # costs = parser.compute_costs()
    # print("Batch Size Cost:", costs['batch_cost'])
    # print("Lot Change Cost:", costs['lot_change_cost'])
    # print("Rolling Window Cost:", costs['rolling_window_cost'])
    # print("Total Cost:", costs['total_cost'])
    
    # Example usage
    solution = Solution(parser)
    # Add sequences for each shop (using example data from the prompt)
    identity = (np.arange(1, 1+len(parser.get_vehicles()))).tolist()
    # print(identity)
    # print(identity54)
    solution.add_shop_entry("body", identity)
    solution.add_shop_entry("paint", identity)
    solution.add_shop_entry("assembly", identity)

    # print(solution.solution)

    # print(solution.compute_costs())

    # Find optimal permutation
    # optimal_sequence, min_cost = find_optimal_permutation(parser)
    # print("Optimal Sequence:", optimal_sequence)
    # print("Minimum Cost:", min_cost)

    # Print solution as JSON
    # print("Solution JSON:")
    # print(solution.to_json())
    # print("Solution JSON:")
    # print(solution.to_json())

    # Optionally save solution to a file
    # print("viable solution ? ", solution.isViable())
    solution.save_to_file("solution.json")
