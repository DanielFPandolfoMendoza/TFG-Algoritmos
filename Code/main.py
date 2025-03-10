import numpy as np

# Leer el archivo y extraer datos
file_path = "/mnt/data/CMT1.vrp"
with open(file_path, "r") as file:
    content = file.readlines()

node_coords = []
demands = {}
deport = None

reading_coords = False
reading_demands = False
reading_depot = False

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
        depot = int(line) if line.isdigit() else depot

# Convertir listas a arrays de NumPy
num_puntos = len(node_coords)
coordenadas = np.zeros((num_puntos, 2))
vector_demandas = np.zeros(num_puntos)

for i, (node, x, y) in enumerate(node_coords):
    coordenadas[i] = [x, y]
    vector_demandas[i] = demands.get(node, 0)

# Mostrar resultados
print("Coordenadas:")
print(coordenadas)
print("\nDemandas:")
print(vector_demandas)
