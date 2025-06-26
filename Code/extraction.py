import numpy as np
import time
from route import define_route
from local_search import combined_optimization
from utils import calculate_route_time

def localsearch(clean_routes, coordinates, demands_vector, capacity, depot_coords, max_distance, route_time):
    optimized_routes, optimized_time = combined_optimization(
        clean_routes,
        coordinates,
        demands_vector,
        capacity,
        depot_coords,
        max_distance,
        route_time
    )
    
    return optimized_routes, optimized_time

#region problem instances

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

#endregion

#region sweeping algorithm

final_time = 0
for i in range(1,101):
    start_time = time.time()
    route_to_follow, new_route_time, final_capacity, trucks = define_route(
        coordinates, depot_coords, demands, capacity, max_distance
    )
    end_time = time.time() 
    if i == 1 or route_time > new_route_time:
        route_time = new_route_time
        route_final = route_to_follow
        trucks_final = trucks
        final_time = end_time-start_time

clean_routes = []
for truck_route in route_final:
    clean_route = [(float(x), float(y)) for x, y in truck_route]
    clean_routes.append(clean_route)

total_initial_distance = 0
print("\nValidating initial routes:")
print("-------------------------")
for i, route in enumerate(clean_routes, 1):
    distance = calculate_route_time(route)
    print(f"Route {i} distance: {distance:.2f}")
    total_initial_distance += distance
print(f"Total initial distance: {total_initial_distance:.2f}")
print(f"Reported initial distance: {route_time:.2f}")
if abs(total_initial_distance - route_time) > 0.01:
    print("WARNING: Initial distance calculation mismatch!")

#endregion

#region local optimization

# Optimize routes using all methods
rutas_optimizadas, tiempo_total_optimizado = localsearch(
    clean_routes,
    coordinates,
    demands_vector,
    capacity,
    depot_coords,
    max_distance, 
    route_time
)

# Validate final optimized routes
total_optimized_distance = 0
print("\nValidating final optimized routes:")
print("--------------------------------")
for i, route in enumerate(rutas_optimizadas, 1):
    distance = calculate_route_time(route)
    print(f"Route {i} distance: {distance:.2f}")
    total_optimized_distance += distance
print(f"Total optimized distance: {total_optimized_distance:.2f}")
print(f"Reported optimized distance: {tiempo_total_optimizado:.2f}")
if abs(total_optimized_distance - tiempo_total_optimizado) > 0.01:
    print("WARNING: Optimized distance calculation mismatch!")

print("\nOptimized Solution:")
print(f"Number of trucks used: {len(rutas_optimizadas)}")
print(f"Total time: {tiempo_total_optimizado:.2f}")
print(f"Improvement: {((route_time - tiempo_total_optimizado) / route_time) * 100:.2f}%")
print("\nOptimized routes per truck:")
for i, route in enumerate(rutas_optimizadas, 1):
    print(f"\nTruck {i} route ({len(route)} points):")
    print(route)

#endregion