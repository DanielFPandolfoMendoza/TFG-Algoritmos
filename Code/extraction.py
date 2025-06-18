import numpy as np
import route 
import time

file_path = "Files/CMT1.vrp"

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


clean_route = [(float(x), float(y)) for x, y in route_final]

# Mostrar resultados
print("Coordenadas:")
print(coordinates)
print("\nDemandas:")
print(demands_vector)
print("\nCoordenadas del Depot:", depot_coords)
print("Capacidad máxima del vehículo:", capacity)
print("Distancia máxima permitida por vehículo:", max_distance)
print('\nRuta')
print(clean_route)
print("Largo de la ruta:", len(clean_route))
print("\nTiempo total:", route_time)
print(f"Tiempo de ejecución: {final_time} segundos")
print("\nCapacidad restante al final:", final_capacity)
print("\nCantidad de camiones utilizados:", trucks_final)
