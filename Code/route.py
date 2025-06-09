import math
import random

def calculate_angle(origin, point):
    return math.atan2(point[1] - origin[1], point[0] - origin[0])

def euclidean_distance(p1, p2):
    return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)

def define_route(coordinates, depot, demands, capacity, max_distance):
    if depot is None:
        raise ValueError("Error: el Depot no puede ser None. Verifica que las coordenadas sean válidas.")
    
    # Convertir las coordenadas a tuplas
    coordinates = [tuple(point) for point in coordinates]
    depot = tuple(depot)

    client_indices = [i for i, point in enumerate(coordinates) if point != depot]
    clients_with_angles = [
        (i, calculate_angle(depot, coordinates[i]))
        for i in client_indices
    ]
    # Ordenar por -ángulo (mayor a menor) para barrido horario
    clients_with_angles.sort(key=lambda x: -x[1])
    ordered_indices = [x[0] for x in clients_with_angles]

    remaining_indices = set(ordered_indices)

    # Variables para almacenar la ruta, la distancia total y la cantidad de camiones usados
    route = [depot]
    total_distance = 0
    trucks = 1

    # Variables del camión actual
    current_capacity = capacity
    current_distance = max_distance  # Distancia restante disponible para el camión actual
    current_point = depot

    while remaining_indices:
        valid_indices = []
        # Buscar clientes alcanzables desde la posición actual
        for i in remaining_indices:
            demand = demands.get(i + 1, 0)
            dist_to_customer = euclidean_distance(current_point, coordinates[i])
            dist_back_to_depot = euclidean_distance(coordinates[i], depot)
            # Se evalúa la posibilidad de atender al cliente con los recursos actuales
            if demand <= current_capacity and (dist_to_customer + dist_back_to_depot) <= current_distance:
                valid_indices.append(i)

        if valid_indices:
            # Se selecciona aleatoriamente un cliente alcanzable
            next_index = random.choice(valid_indices)
            next_point = coordinates[next_index]
            dist_to_next = euclidean_distance(current_point, next_point)
            # Avanzar al cliente
            total_distance += dist_to_next
            current_distance -= dist_to_next  # Se consume la distancia
            current_capacity -= demands.get(next_index + 1, 0)
            route.append(next_point)
            remaining_indices.remove(next_index)
            current_point = next_point

            # Si se atendieron todos los clientes, regresar al depot
            if not remaining_indices:
                if current_point != depot:
                    dist_to_depot = euclidean_distance(current_point, depot)
                    total_distance += dist_to_depot
                    current_distance -= dist_to_depot
                    route.append(depot)
                break

        else:
            # No hay clientes alcanzables desde la posición actual con los recursos actuales.
            # Si no estamos en el depot, el camión regresa para recargar su capacidad.
            if current_point != depot:
                dist_to_depot = euclidean_distance(current_point, depot)
                total_distance += dist_to_depot
                current_distance -= dist_to_depot
                route.append(depot)
                current_point = depot
                # Se recarga la capacidad; la distancia restante no se reinicia.
                current_capacity = capacity

            # Desde el depot, se verifica si existe al menos un nodo alcanzable con la distancia restante del camión actual.
            reachable = False
            for i in remaining_indices:
                round_trip = euclidean_distance(depot, coordinates[i]) + euclidean_distance(coordinates[i], depot)
                if round_trip <= current_distance:
                    reachable = True
                    break

            if reachable:
                # El problema era solo de capacidad; se sigue con el mismo camión.
                route.append(depot)
                continue
            else:
                # Si ningún nodo es alcanzable con la distancia restante, se suma un nuevo camión.
                trucks += 1
                # Se reinician ambos recursos para el nuevo camión.
                current_capacity = capacity
                current_distance = max_distance
                # Como ya estamos en depot, se marca el reinicio en la ruta.
                route.append(depot)
                current_point = depot
                continue

    return route, total_distance, current_capacity, trucks
