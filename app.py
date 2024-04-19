from flask import Flask, send_file, render_template_string, request
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import geopandas as gpd
import folium
import io
import pandas as pd
import networkx as nx
from folium.plugins import MarkerCluster
import random
from dijkstra_file import dijkstra
from bf_file import bellman_ford
import time

show_path = False

app = Flask(__name__)

# Load the Data
nodes_df = pd.read_csv('nodes.csv')
edges_df = pd.read_csv('edges.csv').reset_index()[['u', 'v', 'length']]

west, south, east, north = -80.380096,25.641690,-80.083466,25.886501
nodes_df = nodes_df[(nodes_df['y'] < north) & (nodes_df['y'] > south) & (nodes_df['x'] > west) & (nodes_df['x'] < east)]
edges_df = edges_df[edges_df['u'].isin(nodes_df['osmid']) & edges_df['v'].isin(nodes_df['osmid'])]

# Create Graph and Initialize start and end node
G = nx.from_pandas_edgelist(edges_df, 'u', 'v', edge_attr=True, create_using=nx.Graph())

start_node = nodes_df.sample(1).iloc[0]
end_node = nodes_df.sample(1).iloc[0]


@app.route("/")
def fullscreen():
    global nodes_df, edges_df, G, start_node, end_node, show_path

    m = folium.Map(location=[25.75, -80.25], zoom_start=11)

    #if (show_path):
    #    compute_path(start_node, end_node, m)

    car_icon = folium.features.CustomIcon('toy_car.png', icon_size=(50, 25))

    markers = {}  # Dictionary to hold marker objects for selected nodes



    # Create the button to re-randomize nodes and re-visualize
    button_html = """
    <div style="position: fixed; top: 10px; right: 10px; z-index: 9999; background-color: white; padding: 10px; border-radius: 5px;">
        <button onclick="setShowPath(false);">Re-Randomize Nodes</button>
    </div>
    <script>
        function setShowPath(val) {
            // Set show_path variable
            location.href = '/set_show_path?val=' + val;
            location.reload();
        }
    </script>
    """

    dijsktra_button_html = """
    <div style="position: fixed; top: 60px; right: 10px; z-index: 9999; background-color: white; padding: 10px; border-radius: 5px;">
        <button onclick="setShowPath(true);">Dijkstra</button>
    </div>
    <script>
        function setShowPath(val) {
            // Set show_path variable
            location.href = '/set_show_path?val=' + val;
            location.reload();
        }
    </script>
    """

    if (show_path == False):
        start_node = end_node
        end_node = nodes_df.sample(1).iloc[0]

    markers[start_node['osmid']] = folium.Marker(
        location=[start_node['y'], start_node['x']],
        popup=f"id: {start_node['osmid']}, lat: {start_node['y']}, lon: {start_node['x']}",
        icon=car_icon
    ).add_to(m)

    markers[end_node['osmid']] = folium.Marker(
        location=[end_node['y'], end_node['x']],
        popup=f"id: {end_node['osmid']}, lat: {end_node['y']}, lon: {end_node['x']}",
        icon=folium.Icon(color='blue', icon='map-marker')
    ).add_to(m)


    return f"{button_html}{dijsktra_button_html}{m._repr_html_()}"


@app.route("/set_show_path")
def set_show_path():
    global show_path
    val = request.args.get('val')
    show_path = val.lower() == 'true'
    return "", 204


def compute_path(start_node, end_node, m, algo = "d"):
    global G
    # Measure the time before running Dijkstra's algorithm
    start_time = time.time()

    if (algo == "d"):
        path = dijkstra(G, start_node, end_node)
    else:
        pass

    # Measure the time after running Dijkstra's algorithm
    end_time = time.time()

    # Calculate the time difference
    new_time = end_time - start_time

    selected_nodes = nodes_df[nodes_df['osmid'].isin(path)]
    selected_edges = edges_df[
        (edges_df['u'].isin(selected_nodes['osmid'])) & (edges_df['v'].isin(selected_nodes['osmid']))]

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

        # Visualize dijkstra time in the bottom right corner
        time_html = f"""
                <div style="position: fixed; bottom: 10px; right: 10px; z-index: 9999; background-color: white; padding: 10px; border-radius: 5px;">
                    Dijkstra Time: {new_time:.4f} seconds
                </div>
                """

        return time_html


if __name__ == "__main__":
    app.run(debug=True)
