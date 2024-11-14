from parser import dataParser

if __name__ == "__main__":
    print("ok")
    # Example usage
    filename = 'Instances/tiny.json'  # Replace with the path to your JSON file
    parser = dataParser(filename)

    # Access parsed data
    print("Shops:", parser.get_shops())
    print("Parameters:", parser.get_parameters())
    print("Vehicles:", parser.get_vehicles())
    print("Constraints:", parser.get_constraints())

    # Calculate costs
    costs = parser.compute_costs()
    print("Batch Size Cost:", costs['batch_cost'])
    print("Lot Change Cost:", costs['lot_change_cost'])
    print("Rolling Window Cost:", costs['rolling_window_cost'])
    print("Total Cost:", costs['total_cost'])


def swap(sequence, i, j):
    sequence[i], sequence[j] = sequence[j], sequence[i]
