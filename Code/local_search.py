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

def combined_optimization(routes, coordinates, demands_vector, capacity, depot_coords, max_distance, route_time):
    
    all_methods = [
        exchange,
        insertion,
        opt2
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
    
    # Final verification of the best solution
    final_time = calculate_total_time(current_routes)
    if abs(final_time - best_total_time) > 0.01:
        best_total_time = final_time
    
    return current_routes, best_total_time


