import numpy as np
import random as rd
from src.instance import Instance
from src.solution import Solution
from src.utils import create_solution

def random_solution(instance: Instance) -> Solution:
    #rd_sol = zero_solution(instance)
    Entries = []
    for s in range(len(instance.shops)):
        vehicle_ids = [vehicle.id for vehicle in instance.vehicles]
        rd.shuffle(vehicle_ids)
        Entries.append(vehicle_ids)
    # print(Entries, "entries")
    rd_solution = create_solution(instance, Entries)
    return rd_solution