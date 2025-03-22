import math
import numpy as np
import random  

def euclidean_distance(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def define_route(coordinates, depot, demands, capacity):
    if depot is None:
        raise ValueError("Error: el Depot no puede ser None. Verifica que las coordenadas sean válidas.")

    coordinates = [tuple(point) for point in coordinates]
    depot = tuple(depot) 

    route = [depot]
    remaining_indices = set(range(len(coordinates)))

    actual_point = depot
    time = 0
    remaining_capacity = capacity

    while remaining_indices:
        valid_indices = [i for i in remaining_indices if demands.get(i + 1, 0) <= remaining_capacity]

        if not valid_indices:
            # Si no hay puntos que podamos visitar con la capacidad restante, terminamos la ruta
            break

        next_index = random.choice(valid_indices)
        next_point = coordinates[next_index]

        remaining_capacity -= demands.get(next_index + 1, 0)
        time += euclidean_distance(actual_point, next_point)

        route.append(next_point)
        remaining_indices.remove(next_index)
        actual_point = next_point

    # Asegurarse de regresar al depot al final
    if actual_point != depot:
        time += euclidean_distance(actual_point, depot)
        route.append(depot)

    return route, time, remaining_capacity