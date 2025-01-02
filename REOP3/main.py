import os
import numpy as np
from pathlib import Path

from src.instance import read_instance
from src.solution import read_solution, write_solution, zero_solution, compute_cost
from src.feasible import is_feasible
from src.utils import create_solution

from algo.alea import random_solution


if __name__ == "__main__":
    # to do all the files in one go :
    data_dir = 'data'
    for file_name in os.listdir(data_dir):
        if file_name == 'tiny_sol.json':  # Skip the excluded file
            continue
        file_path = os.path.join(data_dir, file_name)
        if os.path.isfile(file_path):
            print(f"Processing {file_path}...")  # For debugging purposes

            # Replace with your processing logic :
            #current_instance = read_instance(file_path)
            # result = compute solution for current_instance
            # tiny_sol = read_solution(tiny, 'data/tiny_sol.json')  # Use the same solution for all
            # compute_cost(current_instance, current_result, True)
            # write_solution(current_instance, result)

    tiny_name = 'data/tiny.json'  # Replace with the path to your JSON file # noqa:
    tiny = read_instance(tiny_name, False)
    tiny_sol = read_solution(tiny, 'data/tiny_sol.json')
    compute_cost(tiny, tiny_sol, False)
    # write_solution(tiny, tiny_sol)

    # ## Example usage
    saved_solution = zero_solution(tiny)
    saved_cost = compute_cost(tiny, saved_solution, False)
    # print('ok')
    for _ in range(100):
        new_solution = random_solution(tiny)
        # print(new_solution)
        new_cost = compute_cost(tiny, new_solution)
        if new_cost < saved_cost :
            saved_solution = new_solution
            saved_cost = new_cost
    
    print(saved_solution, "saved_solution")
    print(saved_cost)
    compute_cost(tiny, saved_solution, True)
    print(is_feasible(tiny, saved_solution, False))
    write_solution(tiny, saved_solution)
    # test_entries = np.array([[1, 3, 2, 4, 5],[1, 3, 2, 4, 5],[1, 3, 2, 4, 5]])
    # test_sol = create_solution(tiny, test_entries)
    # write_solution(tiny, test_sol)
    # print(test_sol)
    print(is_feasible(tiny, saved_solution, True) )