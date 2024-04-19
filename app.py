from flask import Flask, request
import folium
import pandas as pd
import networkx as nx

show_path = False

app = Flask(__name__)

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
end_node = nodes_df.sample(1).iloc[0]

@app.route("/")
def fullscreen():
    global show_path, start_node, end_node

    m = folium.Map(location=[25.75, -80.25], zoom_start=11)

    # Create Buttons
    button_html = """
    <div style="position: fixed; top: 10px; right: 10px; z-index: 9999; 
                background-color: white; padding: 10px; border-radius: 5px;">
        <button onclick="setShowPath(false);">Re-Randomize Nodes</button>
    </div>
    <div style="position: fixed; top: 60px; right: 10px; z-index: 9999; 
                background-color: white; padding: 10px; border-radius: 5px;">
        <button onclick="setShowPath(true);">Dijkstra</button>
    </div>
    <div style="position: fixed; top: 110px; right: 10px; z-index: 9999; 
                background-color: white; padding: 10px; border-radius: 5px;">
        <button onclick="setShowPath(true);">Bellman Ford</button>
    </div>
    <script>
        function setShowPath(val) {
            fetch('/set_show_path?val=' + val)
              .then(response => location.reload())
              .catch(error => console.error('Error setting show_path:', error));
        }
    </script>
    """

    # Update Nodes if show_path is False
    if not show_path:
        start_node = end_node
        end_node = nodes_df.sample(1).iloc[0]

    # Add Markers
    car_icon = folium.features.CustomIcon('toy_car.png', icon_size=(50, 25))
    markers = {
        start_node['osmid']: folium.Marker(
            location=[start_node['y'], start_node['x']],
            popup=f"id: {start_node['osmid']}, lat: {start_node['y']}, lon: {start_node['x']}",
            icon=car_icon
        ),
        end_node['osmid']: folium.Marker(
            location=[end_node['y'], end_node['x']],
            popup=f"id: {end_node['osmid']}, lat: {end_node['y']}, lon: {end_node['x']}",
            icon=folium.Icon(color='blue', icon='map-marker')
        )
    }

    for marker in markers.values():
        marker.add_to(m)

    return f"{button_html}{m._repr_html_()}"

@app.route("/set_show_path")
def set_show_path():
    global show_path
    val = request.args.get('val')
    show_path = val.lower() == 'true'
    return "", 204

if __name__ == "__main__":
    app.run(debug=True)


   # if (show_path):
    #     # Measure the time before running Dijkstra's algorithm
    #     start_time = time.time()
    #
    #     path = dijkstra(G, start_node, end_node)
    #
    #     # Measure the time after running Dijkstra's algorithm
    #     end_time = time.time()
    #
    #     # Calculate the time difference
    #     new_time = end_time - start_time
    #
    #     selected_nodes = nodes_df[nodes_df['osmid'].isin(path)]
    #     selected_edges = edges_df[
    #         (edges_df['u'].isin(selected_nodes['osmid'])) & (edges_df['v'].isin(selected_nodes['osmid']))]
    #
    #     for _, row in selected_edges.iterrows():
    #         folium.PolyLine(
    #             locations=[(nodes_df.loc[nodes_df['osmid'] == row['u']]['y'].values[0],
    #                         nodes_df.loc[nodes_df['osmid'] == row['u']]['x'].values[0]),
    #                        (nodes_df.loc[nodes_df['osmid'] == row['v']]['y'].values[0],
    #                         nodes_df.loc[nodes_df['osmid'] == row['v']]['x'].values[0])],
    #             popup=f"start_node_id: {row['u']}, end_node_id: {row['v']}, dist: {row['length']}",
    #             color='red',
    #             weight=2,
    #             opacity=0.5
    #         ).add_to(m)
    #
    #         # Visualize dijkstra time in the bottom right corner
    #         time_html = f"""
    #                     <div style="position: fixed; bottom: 10px; right: 10px; z-index: 9999; background-color: white; padding: 10px; border-radius: 5px;">
    #                         Dijkstra Time: {new_time:.4f} seconds
    #                     </div>
    #                     """
    #
