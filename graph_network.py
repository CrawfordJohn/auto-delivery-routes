import networkx as nx
import pandas as pd
import folium
from folium.plugins import MarkerCluster

##Load the Data
nodes_df = pd.read_csv('nodes.csv')
edges_df = pd.read_csv('edges.csv').reset_index()[['u','v', 'length']]

#Create Graph and Initialize start and end node
G = nx.from_pandas_edgelist(edges_df, 'u', 'v', edge_attr=True, create_using=nx.Graph())
start_node, end_node = nodes_df['osmid'].sample(2, random_state=0)

##Need to implement these from stratch
path = nx.dijkstra_path(G, start_node, end_node, weight='length')
print(nx.shortest_path_length(G, start_node, end_node, weight='length'))

#get data for nodes and edges along shortest path
selected_nodes = nodes_df[nodes_df['osmid'].isin(path)]
selected_edges = edges_df[(edges_df['u'].isin(selected_nodes['osmid'])) & (edges_df['v'].isin(selected_nodes['osmid']))]

#create map
m = folium.Map(location=[selected_nodes['y'].mean(), selected_nodes['x'].mean()], zoom_start=13)
marker_cluster = MarkerCluster().add_to(m)

#add the nodes to the map
for _, row in selected_nodes.iterrows():
    if row['osmid'] in [start_node,end_node]:
        folium.Marker(
            location=[row['y'], row['x']],
            popup=f"id: {row['osmid']}, lat: {row['y']}, lon: {row['x']}",
            icon=folium.Icon(color='blue', icon='map-marker')
        ).add_to(m)
    #uncomment if want to show intermediate nodes
    """else:
        folium.Marker(
            location=[row['y'], row['x']],
            popup=f"id: {row['osmid']}, lat: {row['lat']}, lon: {row['lon']}",
            icon=folium.Icon(color='blue', icon='map-marker')
        ).add_to(m)
        """

#add the edges to the map
for _, row in selected_edges.iterrows():
    folium.PolyLine(
        locations=[(nodes_df.loc[nodes_df['osmid'] == row['u']]['y'].values[0],
                    nodes_df.loc[nodes_df['osmid'] == row['u']]['x'].values[0]),
                   (nodes_df.loc[nodes_df['osmid'] == row['v']]['y'].values[0],
                    nodes_df.loc[nodes_df['osmid'] == row['v']]['x'].values[0])],
        popup=f"start_node_id: {row['u']}, end_node_id: {row['v']}, dist: {row['length']}",
        color='red',
        weight=2,
        opacity=0.5
    ).add_to(m)

m.save('map.html')