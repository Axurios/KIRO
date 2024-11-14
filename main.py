from parser import dataParser
from solution import Solution

if __name__ == "__main__":
    print("ok")
    # Example usage
    filename = 'Instances/small_1.json'  # Replace with the path to your JSON file # noqa:
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

    # Print solution as JSON
    print("Solution JSON:")
    print(solution.to_json())

    # Optionally save solution to a file
    solution.save_to_file("solution.json")


def swap(sequence, i, j):
    sequence[i], sequence[j] = sequence[j], sequence[i]
