import heapq

def dijkstra(graph, start, end, weight='length'):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    predecessor = {}
    priority_queue = [(0, start)]

    while priority_queue:
        curr_dist, curr_node = heapq.heappop(priority_queue)

        # Break loop if the end node
        if curr_node == end:
            break

        # Explore neighbors
        for neighbor, data in graph[curr_node].items():
            neighbor_dist = curr_dist + data.get(weight, float('inf'))

            # Update dist
            if neighbor_dist < distances[neighbor]:
                distances[neighbor] = neighbor_dist
                predecessor[neighbor] = curr_node
                heapq.heappush(priority_queue, (neighbor_dist, neighbor))

    # Reconstruct the shortest path
    shortest_path = []
    node = end
    while node != start:
        shortest_path.insert(0, node)
        node = predecessor[node]
    shortest_path.insert(0, start)

    return shortest_path