from flask import Flask, render_template, jsonify, session
import pandas as pd
import networkx as nx
import time
from dijkstra_file import dijkstra
from bf_file import bellman_ford



app = Flask(__name__)
app.secret_key = 'secret'


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

@app.route('/')
def index():
    session.clear()
    global start_node
    start_node = nodes_df.sample(1).iloc[0]

    global end_node
    end_node = None

    global init
    init = True

    return render_template("map.html")
@app.route('/api/get_start')
def init_map():
    location = {"name": int(start_node['osmid']), "lat": start_node['y'], 'lng': start_node['x']}
    return jsonify(location)
@app.route('/api/get_delivery')
def get_delivery():
    global end_node
    global init
    global start_node
    if init:
        end_node = nodes_df.sample(1).iloc[0]
        location = {"name": int(end_node['osmid']), "lat": end_node['y'], 'lng': end_node['x']}
        print(1)
        init = False
        return jsonify(location)
    else:
        start_node = end_node
        end_node = nodes_df.sample(1).iloc[0]
        location = {"name": int(end_node['osmid']), "lat": end_node['y'], 'lng': end_node['x']}
        return jsonify(location)

@app.route('/api/get_d_path')
def get_d_path():
    start_time = time.time()
    path = dijkstra(G, start_node['osmid'], end_node['osmid'])
    elapsed_time = time.time() - start_time
    distance = nx.shortest_path_length(G, start_node['osmid'], end_node['osmid'], weight = 'length') * 0.000621371
    latitude = [nodes_df[nodes_df['osmid'] == id]['y'].iloc[0] for id in path]
    longitude = [nodes_df[nodes_df['osmid'] == id]['x'].iloc[0] for id in path]
    coordinates = [{"lat": lat, "lng": lng} for lat, lng in zip(latitude, longitude)]
    return jsonify(result = coordinates, elapsed_time = elapsed_time, distance = distance)

@app.route('/api/get_b_path')
def get_b_path():
    start_time = time.time()
    path = bellman_ford(G, start_node['osmid'], end_node['osmid'])
    elapsed_time = time.time() - start_time
    distance = nx.shortest_path_length(G, start_node['osmid'], end_node['osmid'], weight='length') * 0.000621371
    latitude = [nodes_df[nodes_df['osmid'] == id]['y'].iloc[0] for id in path]
    longitude = [nodes_df[nodes_df['osmid'] == id]['x'].iloc[0] for id in path]
    coordinates = [{"lat": lat, "lng": lng} for lat, lng in zip(latitude, longitude)]
    return jsonify(result= coordinates, elapsed_time = elapsed_time, distance = distance)

if __name__ == "__main__":
    app.run(debug=True)

