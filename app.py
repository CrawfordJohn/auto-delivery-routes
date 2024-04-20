from flask import Flask, request, render_template, jsonify
import folium
import pandas as pd
import networkx as nx
import time
from dijkstra_file import dijkstra
from bf_file import bellman_ford



app = Flask(__name__)
init = True

# Load Data
nodes_df = pd.read_csv('nodes.csv')
edges_df = pd.read_csv('edges.csv').reset_index()[['u', 'v', 'length']]

# Filter Data
west, south, east, north = -80.380096, 25.641690, -80.083466, 25.886501
nodes_df = nodes_df[(nodes_df['y'] < north) & (nodes_df['y'] > south) &
                         (nodes_df['x'] > west) & (nodes_df['x'] < east)]
edges_df = edges_df[edges_df['u'].isin(nodes_df['osmid']) &
                         edges_df['v'].isin(nodes_df['osmid'])]

# Create Graph and Initialize Nodes
G = nx.from_pandas_edgelist(edges_df, 'u', 'v', edge_attr=True, create_using=nx.Graph())
start_node = nodes_df.sample(1).iloc[0]


@app.route('/')
def index():
    return render_template("map.html")
@app.route('/api/get_start')
def init_map():
    location = {"name": int(start_node['osmid']), "lat": start_node['y'], 'lng': start_node['x']}
    return jsonify(location)
@app.route('/api/get_delivery')
def get_delivery():
    global end_node
    global init
    if init:
        end_node = nodes_df.sample(1).iloc[0]
        location = {"name": int(end_node['osmid']), "lat": end_node['y'], 'lng': end_node['x']}
        init = False
        return jsonify(location)
    else:
        global start_node
        start_node = end_node
        end_node = nodes_df.sample(1).iloc[0]
        location = {"name": int(end_node['osmid']), "lat": end_node['y'], 'lng': end_node['x']}
        return jsonify(location)

@app.route('/api/get_d_path')
def get_d_path():
    path = dijkstra(G, start_node['osmid'], end_node['osmid'])
    latitude = [nodes_df[nodes_df['osmid'] == id]['y'].iloc[0] for id in path]
    longitude = [nodes_df[nodes_df['osmid'] == id]['x'].iloc[0] for id in path]
    coordinates = [{"lat": lat, "lng": lng} for lat, lng in zip(latitude, longitude)]
    return jsonify(coordinates)

@app.route('/api/get_b_path')
def get_b_path():
    path = bellman_ford(G, start_node['osmid'], end_node['osmid'])
    latitude = [nodes_df[nodes_df['osmid'] == id]['y'].iloc[0] for id in path]
    longitude = [nodes_df[nodes_df['osmid'] == id]['x'].iloc[0] for id in path]
    coordinates = [{"lat": lat, "lng": lng} for lat, lng in zip(latitude, longitude)]
    return jsonify(coordinates)
if __name__ == "__main__":
    app.run(debug=True)

