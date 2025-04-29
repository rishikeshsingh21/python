def dfs(graph, start, destination, path=None, visited=None):
    if path is None:
        path = [start]
    if visited is None:
        visited = set()

    if start == destination:
        print(f"Destination '{destination}' found!")
        print("Path:", " -> ".join(path))
        return True

    visited.add(start)

    for neighbor in graph[start]:
        if neighbor not in visited:
            if dfs(graph, neighbor, destination, path + [neighbor], visited):
                return True

    return False

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

found = dfs(graph, start_node, destination_node)

if not found:
    print(f"Destination '{destination_node}' not found in the graph.")
