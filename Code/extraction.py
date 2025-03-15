import numpy as np
import route 

# We open and read the file form where we are taking the information
file_path = "Files/CMT1.vrp"
with open(file_path, "r") as file:
    content = file.readlines()

node_coords = []
demands = {}
deport_coords = None 

reading_coords = False
reading_demands = False
reading_depot = False

depot_values = []

for line in content:
    line = line.strip()
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

# We check that we have taken the tuple of the depot point
if len(depot_values) == 2:
    depot_coords = tuple(depot_values)

# We convert the list to an array
num_points = len(node_coords)
coordinates = np.zeros((num_points, 2))
demands_vector = np.zeros(num_points)

for i, (node, x, y) in enumerate(node_coords):
    coordinates[i] = [x, y]
    demands_vector[i] = demands.get(node, 0)

route_to_follow, time = route.define_route(coordinates, depot_values)
clean_route = [(float(x), float(y)) for x, y in route_to_follow]

# Show results
print("Coordenadas:")
print(coordinates)
print("\nDemandas:")
print(demands_vector)
print("\nCoordenadas del Depot:", depot_coords)
print('\nRuta')
print(clean_route)
print("\nTiempo")
print(time)