import math
import random

def calculate_angle(origin, point):
    return math.atan2(point[1] - origin[1], point[0] - origin[0])

def euclidean_distance(p1, p2):
    return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)

def build_rcl_by_angles(candidates, alpha):
    if not candidates:
        return []
    
    normalized_candidates = []
    for idx, angle in candidates:
        norm_angle = angle if angle >= 0 else angle + 2 * math.pi
        normalized_candidates.append((idx, norm_angle))
    
    angles = [angle for _, angle in normalized_candidates]
    s_max = max(angles)
    s_min = min(angles)
    
    threshold = s_max - alpha * (s_max - s_min)
    rcl = [candidate for candidate in normalized_candidates if candidate[1] >= threshold]
    
    return rcl

def define_grasp_route(coordinates, depot, demands, capacity, max_distance, alpha=0.75):
    if depot is None:
        raise ValueError("Error: el Depot no puede ser None. Verifica que las coordenadas sean válidas.")
    
    coordinates = [tuple(point) for point in coordinates]
    depot = tuple(depot)

    client_indices = [i for i, point in enumerate(coordinates) if point != depot]
    clients_with_angles = [
        (i, calculate_angle(depot, coordinates[i]))
        for i in client_indices
    ]

    ordered_indices = []
    remaining_clients = clients_with_angles.copy()
    
    while remaining_clients:
        rcl = build_rcl_by_angles(remaining_clients, alpha)
        if not rcl:
            break
        
        selected = random.choice(rcl)
        ordered_indices.append(selected[0])
        remaining_clients.remove((selected[0], calculate_angle(depot, coordinates[selected[0]])))

    remaining_indices = ordered_indices.copy()

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
                break

        else:
            if current_point != depot:
                dist_to_depot = euclidean_distance(current_point, depot)
                total_distance += dist_to_depot
                current_distance -= dist_to_depot
                current_route.append(depot)
                current_point = depot
                current_capacity = capacity

            reachable = False
            for i in remaining_indices:
                round_trip = euclidean_distance(depot, coordinates[i]) + euclidean_distance(coordinates[i], depot)
                if round_trip <= current_distance:
                    reachable = True
                    break

            if reachable:
                continue
            else:
                all_routes.append(current_route)
                trucks += 1
                current_capacity = capacity
                current_distance = max_distance
                current_route = [depot]
                current_point = depot
                continue

    all_routes.append(current_route)
    return all_routes, total_distance, current_capacity, trucks
