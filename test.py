from collections import deque

def bfs(graph, start, destination):
    visited = set()
    queue = deque([(start, [start])])  # queue stores (current_node, path_to_node)

    while queue:
        node, path = queue.popleft()

        if node == destination:
            print(f"Destination '{destination}' found!")
            print("Path:", " -> ".join(path))
            return

        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))

    print(f"Destination '{destination}' not found in the graph.")

# Example graph
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

start_node = 'A'
destination_node = input("Enter destination node: ").strip()

bfs(graph, start_node, destination_node)
