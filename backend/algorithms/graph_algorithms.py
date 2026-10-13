import heapq
from collections import deque
import time

CAMPUS_GRAPH = {
    "MAIN_GATE": {
        "ADMIN_BLOCK": 120,
        "LIBRARY": 180,
        "CAFETERIA": 220
    },
    "ADMIN_BLOCK": {
        "MAIN_GATE": 120,
        "CSE_DEPT": 90,
        "LIBRARY": 80,
        "AUDITORIUM": 150
    },
    "CSE_DEPT": {
        "ADMIN_BLOCK": 90,
        "LIBRARY": 110,
        "AUDITORIUM": 140,
        "HOSTEL_A": 200
    },
    "LIBRARY": {
        "MAIN_GATE": 180,
        "ADMIN_BLOCK": 80,
        "CSE_DEPT": 110,
        "CAFETERIA": 100,
        "HOSTEL_B": 210
    },
    "AUDITORIUM": {
        "ADMIN_BLOCK": 150,
        "CSE_DEPT": 140,
        "SPORTS_COMPLEX": 130
    },
    "CAFETERIA": {
        "MAIN_GATE": 220,
        "LIBRARY": 100,
        "SPORTS_COMPLEX": 160,
        "HOSTEL_B": 150
    },
    "SPORTS_COMPLEX": {
        "AUDITORIUM": 130,
        "CAFETERIA": 160,
        "HOSTEL_A": 170
    },
    "HOSTEL_A": {
        "CSE_DEPT": 200,
        "SPORTS_COMPLEX": 170,
        "HOSTEL_B": 120
    },
    "HOSTEL_B": {
        "LIBRARY": 210,
        "CAFETERIA": 150,
        "HOSTEL_A": 120
    }
}

LOCATION_LABELS = {
    "MAIN_GATE": "Main Entrance Gate",
    "ADMIN_BLOCK": "Administrative Block",
    "CSE_DEPT": "CSE Department & Labs",
    "LIBRARY": "Central Digital Library",
    "AUDITORIUM": "Kalam Auditorium",
    "CAFETERIA": "Campus Green Cafeteria",
    "SPORTS_COMPLEX": "Sports Complex & Gym",
    "HOSTEL_A": "Boys Hostel Block A",
    "HOSTEL_B": "Girls Hostel Block B"
}

def bfs_campus_traversal(start_node="MAIN_GATE", graph=None):
    """
    Breadth-First Search (BFS) Graph Traversal
    Time Complexity: O(V + E)
    Space Complexity: O(V)
    Finds layer-by-layer exploration of campus buildings.
    """
    if graph is None:
        graph = CAMPUS_GRAPH

    start_time = time.perf_counter()
    visited = []
    visited_set = set()
    queue = deque([(start_node, 0)]) # (node, distance_level)
    visited_set.add(start_node)
    levels = {}

    while queue:
        current, level = queue.popleft()
        visited.append({
            "node": current,
            "label": LOCATION_LABELS.get(current, current),
            "level": level
        })
        if level not in levels:
            levels[level] = []
        levels[level].append(LOCATION_LABELS.get(current, current))

        for neighbor in sorted(graph.get(current, {}).keys()):
            if neighbor not in visited_set:
                visited_set.add(neighbor)
                queue.append((neighbor, level + 1))

    elapsed_ms = (time.perf_counter() - start_time) * 1000

    return {
        "algorithm": "Breadth-First Search (BFS)",
        "start_node": start_node,
        "start_label": LOCATION_LABELS.get(start_node, start_node),
        "traversal_order": visited,
        "levels": levels,
        "total_nodes_visited": len(visited),
        "time_ms": round(elapsed_ms, 5),
        "complexity": {
            "time": "O(V + E)",
            "space": "O(V)"
        },
        "explanation": f"BFS explored all campus nodes level by level starting from {LOCATION_LABELS.get(start_node, start_node)}."
    }

def dijkstra_shortest_path(start_node="MAIN_GATE", target_node="CSE_DEPT", graph=None):
    """
    Dijkstra's Shortest Path Algorithm
    Time Complexity: O((V + E) log V) with Priority Queue (Heap)
    Space Complexity: O(V)
    Finds minimum walking distance (in meters) and optimal path between campus locations.
    """
    if graph is None:
        graph = CAMPUS_GRAPH

    start_time = time.perf_counter()
    distances = {node: float('inf') for node in graph}
    distances[start_node] = 0
    previous_nodes = {node: None for node in graph}

    # Min-Heap storing (distance, node)
    pq = [(0, start_node)]
    visited = set()
    steps_log = []

    while pq:
        current_dist, current_node = heapq.heappop(pq)

        if current_node in visited:
            continue
        visited.add(current_node)

        steps_log.append({
            "visited_node": current_node,
            "label": LOCATION_LABELS.get(current_node, current_node),
            "current_shortest_distance": current_dist
        })

        if current_node == target_node:
            break

        for neighbor, weight in graph.get(current_node, {}).items():
            if neighbor not in visited:
                new_dist = current_dist + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(pq, (new_dist, neighbor))

    # Reconstruct shortest path
    path = []
    curr = target_node
    while curr is not None:
        path.append(curr)
        curr = previous_nodes[curr]
    path.reverse()

    # Build detailed path steps
    path_details = []
    for i in range(len(path)):
        node_id = path[i]
        label = LOCATION_LABELS.get(node_id, node_id)
        dist_so_far = distances[node_id]
        leg_dist = 0
        if i > 0:
            prev_id = path[i - 1]
            leg_dist = graph[prev_id].get(node_id, 0)
        path_details.append({
            "step": i + 1,
            "location_id": node_id,
            "location_name": label,
            "leg_distance_meters": leg_dist,
            "total_distance_meters": dist_so_far
        })

    elapsed_ms = (time.perf_counter() - start_time) * 1000

    return {
        "algorithm": "Dijkstra's Shortest Path",
        "start_node": start_node,
        "target_node": target_node,
        "start_label": LOCATION_LABELS.get(start_node, start_node),
        "target_label": LOCATION_LABELS.get(target_node, target_node),
        "shortest_distance_meters": distances[target_node],
        "path": path,
        "path_details": path_details,
        "steps_log": steps_log,
        "time_ms": round(elapsed_ms, 5),
        "complexity": {
            "time": "O((V + E) log V)",
            "space": "O(V)"
        },
        "explanation": f"Optimal route from {LOCATION_LABELS.get(start_node, start_node)} to {LOCATION_LABELS.get(target_node, target_node)} is {distances[target_node]} meters."
    }
