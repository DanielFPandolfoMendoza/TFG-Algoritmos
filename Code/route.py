import math
import random

def euclidean_distance(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def define_route(coordinates, depot, demands, capacity, max_distance):
    if depot is None:
        raise ValueError("Error: el Depot no puede ser None. Verifica que las coordenadas sean válidas.")

    coordinates = [tuple(point) for point in coordinates]
    depot = tuple(depot)

    route = [depot]
    remaining_indices = set(range(len(coordinates)))

    actual_point = depot
    total_distance = 0
    trucks = 1
    remaining_capacity = capacity
    remaining_distance = max_distance

    while remaining_indices:
        valid_indices = []
        for i in remaining_indices:
            demand = demands.get(i + 1, 0)
            dist_to_customer = euclidean_distance(actual_point, coordinates[i])
            dist_back_to_depot = euclidean_distance(coordinates[i], depot)
            projected_distance = dist_to_customer + dist_back_to_depot

            if demand <= remaining_capacity and projected_distance <= remaining_distance:
                valid_indices.append(i)

        if not valid_indices:
            if actual_point != depot:
                dist_to_depot = euclidean_distance(actual_point, depot)
                total_distance += dist_to_depot
                route.append(depot)
            remaining_capacity = capacity
            remaining_distance = max_distance
            actual_point = depot
            route.append(depot)
            continue

        next_index = random.choice(valid_indices)
        next_point = coordinates[next_index]

        dist_to_next = euclidean_distance(actual_point, next_point)
        dist_back_to_depot = euclidean_distance(next_point, depot)

        remaining_capacity -= demands.get(next_index + 1, 0)
        total_distance += dist_to_next
        remaining_distance -= dist_to_next

        route.append(next_point)
        remaining_indices.remove(next_index)
        actual_point = next_point

        if remaining_distance < dist_back_to_depot:
            total_distance += dist_back_to_depot
            route.append(depot)
            remaining_capacity = capacity
            remaining_distance = max_distance
            actual_point = depot

    if actual_point != depot:
        dist_to_depot = euclidean_distance(actual_point, depot)
        total_distance += dist_to_depot
        route.append(depot)

    return route, total_distance, remaining_capacity, trucks
