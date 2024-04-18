from flask import Flask, send_file, render_template_string
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import geopandas as gpd
import folium
import io
import pandas as pd
import networkx as nx
from folium.plugins import MarkerCluster


app = Flask(__name__)


@app.route("/")
def fullscreen():
    ##Load the Data
    nodes_df = pd.read_csv('nodes.csv')
    edges_df = pd.read_csv('edges.csv').reset_index()[['u', 'v', 'length']]

    # Create Graph and Initialize start and end node
    G = nx.from_pandas_edgelist(edges_df, 'u', 'v', edge_attr=True, create_using=nx.Graph())
    start_node, end_node = nodes_df['osmid'].sample(2, random_state=0)

    ##Need to implement these from stratch
    path = nx.dijkstra_path(G, start_node, end_node, weight='length')
    print(nx.shortest_path_length(G, start_node, end_node, weight='length'))

    # get data for nodes and edges along shortest path
    selected_nodes = nodes_df[nodes_df['osmid'].isin(path)]
    selected_edges = edges_df[
        (edges_df['u'].isin(selected_nodes['osmid'])) & (edges_df['v'].isin(selected_nodes['osmid']))]

    # create map
    m = folium.Map(location=[selected_nodes['y'].mean(), selected_nodes['x'].mean()], zoom_start=13)
    marker_cluster = MarkerCluster().add_to(m)

    # add the nodes to the map
    for _, row in selected_nodes.iterrows():
        if row['osmid'] in [start_node, end_node]:
            folium.Marker(
                location=[row['y'], row['x']],
                popup=f"id: {row['osmid']}, lat: {row['y']}, lon: {row['x']}",
                icon=folium.Icon(color='blue', icon='map-marker')
            ).add_to(m)
        # uncomment if want to show intermediate nodes
        """else:
            folium.Marker(
                location=[row['y'], row['x']],
                popup=f"id: {row['osmid']}, lat: {row['lat']}, lon: {row['lon']}",
                icon=folium.Icon(color='blue', icon='map-marker')
            ).add_to(m)
            """

    # add the edges to the map
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

    return m._repr_html_()


@app.route("/iframe")
def iframe():
   """Embed a map as an iframe on a page."""
   m = folium.Map()


   # set the iframe width and height
   m.get_root().width = "800px"
   m.get_root().height = "600px"
   iframe = m.get_root()._repr_html_()


   return render_template_string(
       """
           <!DOCTYPE html>
           <html>
               <head></head>
               <body>
                   <h1>Using an iframe</h1>
                   {{ iframe|safe }}
               </body>
           </html>
       """,
       iframe=iframe,
   )




@app.route("/components")
def components():
   """Extract map components and put those on a page."""
   m = folium.Map(
       width=800,
       height=600,
   )


   m.get_root().render()
   header = m.get_root().header.render()
   body_html = m.get_root().html.render()
   script = m.get_root().script.render()


   return render_template_string(
       """
           <!DOCTYPE html>
           <html>
               <head>
                   {{ header|safe }}
               </head>
               <body>
                   <h1>Using components</h1>
                   {{ body_html|safe }}
                   <script>
                       {{ script|safe }}
                   </script>
               </body>
           </html>
       """,
       header=header,
       body_html=body_html,
       script=script,
   )




if __name__ == "__main__":
   app.run(debug=True)

