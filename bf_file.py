def bellman_ford(graph, start, end, weight='length'):
    #initialize distances and predecessors
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    predecessor = {}
    updated = True

    #keep updating shortest distances until no updates occur
    for _ in range(len(graph) - 1):
        if not updated:
            break
        updated = False
        for curr_node in graph:
            for neighbor, data in graph[curr_node].items():
                neighbor_dist = distances[curr_node] + data.get(weight, float('inf'))
                if neighbor_dist < distances[neighbor]:
                    distances[neighbor] = neighbor_dist
                    predecessor[neighbor] = curr_node
                    updated = True

    #reconstruct the shortest path
    shortest_path = []
    node = end
    while node != start:
        shortest_path.insert(0, node)
        node = predecessor[node]
    shortest_path.insert(0, start)

    return shortest_path