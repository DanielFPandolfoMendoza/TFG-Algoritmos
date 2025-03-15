import math
import numpy as np

def euclidean_distance(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def define_route(coordinates, depot):
    if depot is None:
        raise ValueError("Error: el Depot no puede ser None. Verifica que las coordenadas sean válidas.")

    # Convertir las coordenadas a tuplas para evitar problemas con sets
    coordinates = [tuple(point) for point in coordinates]
    depot = tuple(depot)  # Convertimos el depot en una tupla

    route = [depot]  # Comienza en el depósito
    remaining_points = set(coordinates)  # Puntos a visitar

    actual_point = depot

    time = 0

    while remaining_points:
        next_point = min(remaining_points, key=lambda p: euclidean_distance(actual_point, p))
        time = time +  euclidean_distance(actual_point, next_point)
        route.append(next_point)
        remaining_points.remove(next_point)
        actual_point = next_point

    return route, time