from flask import Flask, send_file, render_template_string
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import geopandas as gpd
import folium
import io
import pandas as pd


app = Flask(__name__)


@app.route("/")
def fullscreen():
    # Coordinates for Florida
    lat_min = 24.396308
    lat_max = 27.001056
    lon_min = -82.634938
    lon_max = -78.974306

    # Creates a map centered around Florida
    m = folium.Map(location=[(lat_min + lat_max) / 2, (lon_min + lon_max) / 2], zoom_start=6)

    # Restricts map view to Florida
    m.fit_bounds([[lat_min, lon_min], [lat_max, lon_max]])

    # Load nodes from CSV file
    nodes_df = pd.read_csv('nodes.csv')

    # Sample a subset of nodes (e.g., 100 nodes)
    sample_size = 100
    sampled_nodes = nodes_df.sample(n=sample_size)

    # Add each sampled node as a dot on the map
    for index, row in sampled_nodes.iterrows():
        folium.Marker(location=[row['y'], row['x']], popup=str(row['osmid'])).add_to(m)

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

