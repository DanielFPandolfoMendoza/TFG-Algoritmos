import numpy as np
import route 
import time
from local_search import exchange, insertion, opt2

def localsearch(clean_routes, coordinates, demands_vector, capacity, depot_coords, max_distance, route_time):
    # Optimize using exchange
    exchange_route, exchange_time = exchange(
        clean_routes,
        coordinates,
        demands_vector,
        capacity,
        depot_coords,
        max_distance
    )

    # Optimize using insertion
    insertion_route, insertion_time = insertion(
        clean_routes,
        coordinates,
        demands_vector,
        capacity,
        depot_coords,
        max_distance
    )
    
    # Optimize using 2-opt
    opt2_route, opt2_time = opt2(
        clean_routes,
        coordinates,
        demands_vector,
        capacity,
        depot_coords,
        max_distance
    )
    
    # Compare results and choose the best
    times = {
        "original": route_time,
        "exchange": exchange_time,
        "insertion": insertion_time,
        "2-opt": opt2_time
    }
    
    best_method = min(times, key=lambda x: times[x])
    best_time = times[best_method]
    
    if best_method == "exchange":
        return exchange_route, best_time, best_method
    elif best_method == "insertion":
        return insertion_route, best_time, best_method
    elif best_method == "2-opt":
        return opt2_route, best_time, best_method
    else:
        return clean_routes, route_time, "original"

file_path = "Files/CMT12.vrp"

with open(file_path, "r") as file:
    content = file.readlines()

node_coords = []
demands = {}
depot_coords = None

reading_coords = False
reading_demands = False
reading_depot = False

capacity = None
max_distance = None 
depot_values = []

for line in content:
    line = line.strip()
    if line.startswith("CAPACITY"):
        parts = line.split(":")
        if len(parts) == 2:
            capacity = int(parts[1].strip())
        continue
    
    if line.startswith("DISTANCE"):
        parts = line.split(":")
        if len(parts) == 2:
            max_distance = float(parts[1].strip())
        continue

    if line == "NODE_COORD_SECTION":
        reading_coords = True
        continue
    elif line == "DEMAND_SECTION":
        reading_coords = False
        reading_demands = True
        continue
    elif line == "DEPOT_SECTION":
        reading_demands = False
        reading_depot = True
        continue
    elif line == "EOF":
        break

    if reading_coords:
        parts = line.split()
        node_coords.append((int(parts[0]), float(parts[1]), float(parts[2])))
    elif reading_demands:
        parts = line.split()
        demands[int(parts[0])] = int(parts[1])
    elif reading_depot:
        if line.isdigit() or (line.startswith('-') and line[1:].isdigit()):
            depot_values.append(int(line))

if len(depot_values) == 2:
    depot_coords = tuple(depot_values)

num_points = len(node_coords)
coordinates = np.zeros((num_points, 2))
demands_vector = np.zeros(num_points)

for i, (node, x, y) in enumerate(node_coords):
    coordinates[i] = [x, y]
    demands_vector[i] = demands.get(node, 0)

final_time = 0
for i in range(1,101):
    start_time = time.time()
    route_to_follow, new_route_time, final_capacity, trucks = route.define_route(
        coordinates, depot_coords, demands, capacity, max_distance
    )
    end_time = time.time() 
    if i == 1:
        route_time = new_route_time
        route_final = route_to_follow
        trucks_final = trucks
        final_time = end_time-start_time
    if route_time > new_route_time:
        route_time = new_route_time
        route_final = route_to_follow
        trucks_final = trucks
        final_time = end_time-start_time

clean_routes = []
for truck_route in route_final:
    clean_route = [(float(x), float(y)) for x, y in truck_route]
    clean_routes.append(clean_route)

# Optimize routes using all methods
rutas_optimizadas, tiempo_total_optimizado, metodo_usado = localsearch(
    clean_routes,
    coordinates,
    demands_vector,
    capacity,
    depot_coords,
    max_distance, 
    route_time
)

print("Coordinates:")
print(coordinates)
print("\nDemands:")
print(demands_vector)
print("\nDepot Coordinates:", depot_coords)
print("Maximum vehicle capacity:", capacity)
print("Maximum allowed distance per vehicle:", max_distance)
print('\nInitial routes per truck:')
for i, route in enumerate(clean_routes, 1):
    print(f"\nInitial route for truck {i}:")
    print(route)
    print(f"Length of route {i}:", len(route))
print("\nInitial total time:", route_time)
print(f"Execution time: {final_time} seconds")
print("\nRemaining capacity at the end:", final_capacity)
print("\nNumber of trucks used:", trucks_final)

print('\nOptimized routes per truck:')
for i, route in enumerate(rutas_optimizadas, 1):
    print(f"\nOptimized route for truck {i}:")
    print(route)
    print(f"Length of route {i}:", len(route))
print("\nOptimized total time:", tiempo_total_optimizado)
print(f"Method that gave best result: {metodo_usado}")


