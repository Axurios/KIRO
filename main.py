from parser import dataParser
from solution import Solution
from itertools import permutations


def calculate_cost_after_permutation(parser, sequence):
    # Create a temporary parser object with the new sequence
    temp_parser = dataParser(parser.filename)
    temp_parser.vehicles = {i: temp_parser.vehicles[i] for i in sequence}
    costs = temp_parser.compute_costs()
    return costs['total_cost']


def find_optimal_permutation(parser):
    vehicles = list(parser.get_vehicles().keys())
    min_cost = float('inf')
    optimal_sequence = None

    for perm in permutations(vehicles):
        cost = calculate_cost_after_permutation(parser, perm)
        if cost < min_cost:
            min_cost = cost
            optimal_sequence = perm

    return optimal_sequence, min_cost


if __name__ == "__main__":
    print("ok")
    # Example usage
    filename = 'Instances/tiny.json'  # Replace with the path to your JSON file # noqa:
    parser = dataParser(filename)

    # Access parsed data
    # print("Shops:", parser.get_shops())
    # print("Parameters:", parser.get_parameters())
    print("Vehicles:", parser.get_vehicles())
    # print("Constraints:", parser.get_constraints())

    # # Calculate costs
    # costs = parser.compute_costs()
    # print("Batch Size Cost:", costs['batch_cost'])
    # print("Lot Change Cost:", costs['lot_change_cost'])
    # print("Rolling Window Cost:", costs['rolling_window_cost'])
    # print("Total Cost:", costs['total_cost'])

    # Example usage
    solution = Solution()
    # Add sequences for each shop (using example data from the prompt)
    solution.add_shop_sequence("body", [1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
    solution.add_shop_sequence("paint", [1, 2, 3, 4, 5], [1, 2, 4, 3, 5])
    solution.add_shop_sequence("assembly", [1, 2, 4, 3, 5], [1, 2, 4, 3, 5])

    # Find optimal permutation
    optimal_sequence, min_cost = find_optimal_permutation(parser)
    print("Optimal Sequence:", optimal_sequence)
    print("Minimum Cost:", min_cost)

    # Print solution as JSON
    print("Solution JSON:")
    print(solution.to_json())

    # Optionally save solution to a file
    solution.save_to_file("solution.json")


def swap(sequence, i, j):
    sequence[i], sequence[j] = sequence[j], sequence[i]
