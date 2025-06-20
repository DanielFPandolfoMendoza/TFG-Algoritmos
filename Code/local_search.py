import math

def calculate_distance(point1, point2):
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

def calculate_route_time(route):
    total_time = 0
    for i in range(len(route) - 1):
        total_time += calculate_distance(route[i], route[i + 1])
    return total_time

def verify_distance_load(route, coordinates, demands_vector, capacity, depot_coords, max_distance):
    current_load = 0
    accumulated_distance = 0
    new_route = [route[0]]
    
    for i in range(1, len(route)):
        point = route[i]
        
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
            # If not enough distance, route cannot be completed
            return None, False
        
        # 2. Check if there's enough load
        if current_load + point_demand > capacity:
            new_route.append(depot_coords)
            current_load = 0
            dist_to_point = calculate_distance(depot_coords, point)
            dist_to_depot = calculate_distance(point, depot_coords)
            needed_distance = dist_to_point + dist_to_depot
            
            # 3. Check if with remaining distance can reach the point
            if accumulated_distance + needed_distance > max_distance:
                # If not enough distance after reloading, route cannot be completed
                return None, False
        
        new_route.append(point)
        current_load += point_demand
        accumulated_distance += dist_to_point
    
    return new_route, True

def exchange(routes, coordinates, demands_vector, capacity, depot_coords, max_distance):
    optimized_routes = []
    total_time = 0
    
    for route in routes:
        if route[0] != depot_coords: 
            route.insert(0, depot_coords)
        if route[-1] != depot_coords:
            route.append(depot_coords)
            
        best_route = route.copy()
        best_time = calculate_route_time(best_route)
        
        for i in range(1, len(route) - 1):
            for j in range(i + 1, len(route) - 1):
                new_route = route.copy()
                new_route[i], new_route[j] = new_route[j], new_route[i]
                
                # Verify load and distance
                new_route, valid = verify_distance_load(new_route, coordinates, demands_vector, capacity, depot_coords, max_distance)
                if valid:
                    new_time = calculate_route_time(new_route)
                    
                    if new_time < best_time:
                        best_route = new_route
                        best_time = new_time
        
        optimized_routes.append(best_route)
        total_time += best_time
    
    return optimized_routes, total_time

def insertion(routes, coordinates, demands_vector, capacity, depot_coords, max_distance):
    optimized_routes = []
    total_time = 0
    
    for route in routes:
        if route[0] != depot_coords:
            route.insert(0, depot_coords)
        if route[-1] != depot_coords:
            route.append(depot_coords)
            
        best_route = route.copy()
        best_time = calculate_route_time(best_route)
        
        for i in range(1, len(route) - 1):
            point = route[i]
            for j in range(1, len(route)):
                if i != j:
                    new_route = route.copy()
                    new_route.remove(point)
                    new_route.insert(j, point)
                    
                    # Verify load and distance
                    new_route, valid = verify_distance_load(new_route, coordinates, demands_vector, capacity, depot_coords, max_distance)
                    if valid:
                        new_time = calculate_route_time(new_route)
                        
                        if new_time < best_time:
                            best_route = new_route
                            best_time = new_time
        
        optimized_routes.append(best_route)
        total_time += best_time
    
    return optimized_routes, total_time

def opt2(routes, coordinates, demands_vector, capacity, depot_coords, max_distance):
    optimized_routes = []
    total_time = 0
    
    for route in routes:
        if route[0] != depot_coords:
            route.insert(0, depot_coords)
        if route[-1] != depot_coords:
            route.append(depot_coords)
            
        best_route = route.copy()
        best_time = calculate_route_time(best_route)
        
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route) - 1):
                new_route = route.copy()
                segment = new_route[i:j+1]
                segment.reverse()
                new_route[i:j+1] = segment
                
                # Verify load and distance
                new_route, valid = verify_distance_load(new_route, coordinates, demands_vector, capacity, depot_coords, max_distance)
                if valid:
                    new_time = calculate_route_time(new_route)
                    
                    if new_time < best_time:
                        best_route = new_route
                        best_time = new_time
        
        optimized_routes.append(best_route)
        total_time += best_time
    
    return optimized_routes, total_time

    



