import copy
def compute_exit(vehicles, entry, delta):
    # Create a copy of entry to work on, as we don't want to modify the original list
    exit_list = copy.deepcopy(entry)
    print(exit_list, "aaaaaa")
    
    # Start from the end of the list and move backwards
    for i in range(len(exit_list) - 1, -1, -1):
        vehicle_num = exit_list[i]
        if vehicles[vehicle_num] == 'two-tone':  # If the vehicle is two-tone
            # Try to move forward within the allowed delta
            moves = 0
            j = i
            while moves < delta and j < len(exit_list) - 1:
                # Check the vehicle in front of the current position
                next_vehicle = exit_list[j + 1]
                # Stop if the next vehicle is also 'two-tone'
                if vehicles[next_vehicle] == 'two-tone':
                    break
                # Swap positions
                exit_list[j], exit_list[j + 1] = exit_list[j + 1], exit_list[j]
                # Move forward
                j += 1
                moves += 1

    return exit_list



# Define the vehicles and entry permutation
vehicles = {
    1: 'regular', 2: 'regular', 3: 'two-tone', 4: 'regular', 5: 'regular', 6: 'two-tone',
    7: 'regular', 8: 'two-tone', 9: 'regular', 10: 'regular', 11: 'regular', 12: 'regular',
    13: 'two-tone', 14: 'two-tone', 15: 'regular', 16: 'regular', 17: 'two-tone', 18: 'two-tone',
    19: 'regular', 20: 'regular', 21: 'regular', 22: 'regular', 23: 'regular', 24: 'two-tone',
    25: 'two-tone', 26: 'two-tone', 27: 'regular', 28: 'regular', 29: 'two-tone', 30: 'regular',
    31: 'two-tone', 32: 'two-tone', 33: 'two-tone', 34: 'regular', 35: 'regular', 36: 'regular',
    37: 'two-tone', 38: 'regular', 39: 'regular', 40: 'regular', 41: 'two-tone', 42: 'regular',
    43: 'regular', 44: 'regular', 45: 'two-tone', 46: 'two-tone', 47: 'regular', 48: 'regular',
    49: 'two-tone', 50: 'regular', 51: 'two-tone', 52: 'two-tone', 53: 'two-tone', 54: 'two-tone'
}

entry = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
         25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46,
         47, 48, 49, 50, 51, 52, 53, 54]

delta = 2  # The number of positions we want to move two-tone vehicles up

# Example usage with delta = 2 (or any desired value)
exit_result = compute_exit(vehicles, entry, delta=2)
print(exit_result)
