from utils import calculate_route_time, verify_distance_load, calculate_total_time

#region simple methods

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

#endregion

#region multiple methods

def exchange_multiple(routes, coordinates, demands_vector, capacity, depot_coords, max_distance):
    best_solution = None
    best_total_time = sum(calculate_route_time(route) for route in routes)
    
    for i in range(len(routes)):
        for j in range(i + 1, len(routes)):
            for point_i in range(1, len(routes[i]) - 1):
                for point_j in range(1, len(routes[j]) - 1):
                    new_route_i = routes[i].copy()
                    new_route_j = routes[j].copy()
                    
                    new_route_i[point_i], new_route_j[point_j] = new_route_j[point_j], new_route_i[point_i]
                    
                    new_route_i, valid_i = verify_distance_load(new_route_i, coordinates, demands_vector, capacity, depot_coords, max_distance)
                    new_route_j, valid_j = verify_distance_load(new_route_j, coordinates, demands_vector, capacity, depot_coords, max_distance)
                    
                    if valid_i and valid_j:
                        new_solution = routes.copy()
                        new_solution[i] = new_route_i
                        new_solution[j] = new_route_j
                        total_time = sum(calculate_route_time(r) for r in new_solution)
                        
                        if total_time < best_total_time:
                            best_total_time = total_time
                            best_solution = new_solution
    
    return best_solution if best_solution else routes, best_total_time


def insertion_multiple(routes, coordinates, demands_vector, capacity, depot_coords, max_distance):
    best_solution = None
    best_total_time = sum(calculate_route_time(route) for route in routes)
    
    for i in range(len(routes)):
        for j in range(len(routes)):
            if i == j:
                continue
                
            for point_pos in range(1, len(routes[i]) - 1):
                point_to_insert = routes[i][point_pos]
                
                new_route_i = routes[i].copy()
                new_route_j = routes[j].copy()
                
                new_route_i.pop(point_pos)
                
                for insert_pos in range(1, len(new_route_j)):
                    current_route_j = new_route_j.copy()
                    current_route_j.insert(insert_pos, point_to_insert)
                    
                    # Verify load and distance for both routes
                    new_route_i_verified, valid_i = verify_distance_load(new_route_i, coordinates, demands_vector, capacity, depot_coords, max_distance)
                    new_route_j_verified, valid_j = verify_distance_load(current_route_j, coordinates, demands_vector, capacity, depot_coords, max_distance)
                    
                    if valid_i and valid_j:
                        new_solution = routes.copy()
                        new_solution[i] = new_route_i_verified
                        new_solution[j] = new_route_j_verified
                        total_time = sum(calculate_route_time(r) for r in new_solution)
                        
                        if total_time < best_total_time:
                            best_total_time = total_time
                            best_solution = new_solution
    
    return best_solution if best_solution else routes, best_total_time

#endregion

def combined_optimization(routes, coordinates, demands_vector, capacity, depot_coords, max_distance, route_time):
    
    all_methods = [
        exchange,
        insertion,
        opt2,
        exchange_multiple,
        insertion_multiple
    ]
    
    current_routes = routes.copy()
    best_total_time = route_time
    improvement_found = True
    
    # Continue while we find improvements in a cycle
    while improvement_found:
        improvement_found = False
        
        # Try each method in sequence
        for method in all_methods:
            optimized_routes, total_time = method(current_routes.copy(), coordinates, demands_vector, capacity, depot_coords, max_distance)
            
            actual_time = calculate_total_time(optimized_routes)

            if abs(actual_time - total_time) > 0.01:
                total_time = actual_time

            if total_time < best_total_time:
                current_routes = optimized_routes
                best_total_time = total_time
                improvement_found = True
                print(f"Found improvement: {best_total_time}")
                break
    
    # Final verification of the best solution
    final_time = calculate_total_time(current_routes)
    if abs(final_time - best_total_time) > 0.01:
        best_total_time = final_time
    
    # Filter out routes that only contain the depot point
    filtered_routes = [route for route in current_routes if len(route) > 2 or (len(route) == 2 and route[0] != route[1])]
    
    return filtered_routes, best_total_time


