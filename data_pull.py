import osmnx as ox

#Define bounding box (Greater Miami Area)
west, south, east, north = -80.634155,25.219851,-79.826660,26.902477

G = ox.graph_from_bbox(north, south, east, west, network_type='drive')
fig, ax = ox.plot_graph(G)

nodes, edges = ox.graph_to_gdfs(G, nodes=True, edges=True)

#nodes[["y", "x", "street_count", "geometry"]].to_csv("nodes.csv")
#edges[["osmid", "length", "geometry"]].to_csv("edges.csv")