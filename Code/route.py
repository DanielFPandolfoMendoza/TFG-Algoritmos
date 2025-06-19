import math
import random

def calculate_angle(origin, point):
    return math.atan2(point[1] - origin[1], point[0] - origin[0])

def euclidean_distance(p1, p2):
    return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)

def define_route(coordinates, depot, demands, capacity, max_distance):
    if depot is None:
        raise ValueError("Error: el Depot no puede ser None. Verifica que las coordenadas sean válidas.")
    
    coordinates = [tuple(point) for point in coordinates]
    depot = tuple(depot)

    client_indices = [i for i, point in enumerate(coordinates) if point != depot]
    clients_with_angles = [
        (i, calculate_angle(depot, coordinates[i]))
        for i in client_indices
    ]
    clients_with_angles.sort(key=lambda x: -x[1])
    ordered_indices = [x[0] for x in clients_with_angles]

    remaining_indices = set(ordered_indices)

    all_routes = []
    current_route = [depot]
    total_distance = 0
    trucks = 1

    current_capacity = capacity
    current_distance = max_distance
    current_point = depot

    while remaining_indices:
        valid_indices = []
        for i in remaining_indices:
            demand = demands.get(i + 1, 0)
            dist_to_customer = euclidean_distance(current_point, coordinates[i])
            dist_back_to_depot = euclidean_distance(coordinates[i], depot)
            if demand <= current_capacity and (dist_to_customer + dist_back_to_depot) <= current_distance:
                valid_indices.append(i)

        if valid_indices:
            next_index = valid_indices[0]   
            next_point = coordinates[next_index]
            dist_to_next = euclidean_distance(current_point, next_point)
            total_distance += dist_to_next
            current_distance -= dist_to_next
            current_capacity -= demands.get(next_index + 1, 0)
            current_route.append(next_point)
            remaining_indices.remove(next_index)
            current_point = next_point

            if not remaining_indices:
                if current_point != depot:
                    dist_to_depot = euclidean_distance(current_point, depot)
                    total_distance += dist_to_depot
                    current_distance -= dist_to_depot
                current_route.append(depot)
                all_routes.append(current_route)
                break

        else:
            if current_point != depot:
                dist_to_depot = euclidean_distance(current_point, depot)
                total_distance += dist_to_depot
                current_distance -= dist_to_depot
                current_route.append(depot)
                all_routes.append(current_route)
                current_point = depot
                current_capacity = capacity
                current_route = [depot]

            reachable = False
            for i in remaining_indices:
                round_trip = euclidean_distance(depot, coordinates[i]) + euclidean_distance(coordinates[i], depot)
                if round_trip <= current_distance:
                    reachable = True
                    break

            if reachable:
                continue
            else:
                trucks += 1
                current_capacity = capacity
                current_distance = max_distance
                current_route = [depot]
                current_point = depot
                continue

    return all_routes, total_distance, current_capacity, trucks
