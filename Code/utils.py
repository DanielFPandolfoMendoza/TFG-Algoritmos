import math

def calculate_distance(point1, point2):
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

def calculate_route_time(route):
    total_time = 0
    for i in range(len(route) - 1):
        total_time += calculate_distance(route[i], route[i + 1])
    return total_time

def calculate_total_time(routes):
    return sum(calculate_route_time(route) for route in routes)

def verify_distance_load(route, coordinates, demands_vector, capacity, depot_coords, max_distance):
    current_load = 0
    accumulated_distance = 0
    new_route = [route[0]]
    
    for i in range(1, len(route)):
        point = route[i]
        
        # Skip if this point is the depot and we just came from the depot
        if point == depot_coords and new_route[-1] == depot_coords:
            continue
            
        point_demand = 0
        for j, coord in enumerate(coordinates):
            if abs(coord[0] - point[0]) == 0 and abs(coord[1] - point[1]) == 0:
                point_demand = demands_vector[j]
                break
        
        # 1. Check if there's enough distance to go to the point and return to depot
        dist_to_point = calculate_distance(new_route[-1], point)
        dist_to_depot = calculate_distance(point, depot_coords)
        needed_distance = dist_to_point + dist_to_depot
        
        if accumulated_distance + needed_distance > max_distance:
            return None, False
        
        # 2. Check if there's enough load
        if current_load + point_demand > capacity:
            if new_route[-1] != depot_coords:
                new_route.append(depot_coords)
                accumulated_distance += calculate_distance(new_route[-2], depot_coords)
            current_load = 0
            dist_to_point = calculate_distance(depot_coords, point)
            dist_to_depot = calculate_distance(point, depot_coords)
            needed_distance = dist_to_point + dist_to_depot
            
            # 3. Check if with remaining distance can reach the point
            if accumulated_distance + needed_distance > max_distance:
                return None, False
        
        new_route.append(point)
        current_load += point_demand
        accumulated_distance += dist_to_point
    
    return new_route, True