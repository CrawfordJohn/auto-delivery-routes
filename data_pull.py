import osmnx as ox

# Specify the location
location = "Miami, Florida"

# Load the street network
G = ox.graph_from_place(location, network_type='drive')


# Get nodes and edges
nodes, edges = ox.graph_to_gdfs(G, nodes=True, edges=True)

# Nodes are intersections and points along the streets
# Edges include distances (default is length in meters)
