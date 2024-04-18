from flask import Flask, send_file, render_template_string
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import geopandas as gpd
import folium
import io


app = Flask(__name__)


@app.route("/")
def fullscreen():
    # Coordinates for Florida
    lat_min = 24.396308
    lat_max = 31.001056
    lon_min = -87.634938
    lon_max = -79.974306

    # Creates a map centered around Florida
    m = folium.Map(location=[(lat_min + lat_max) / 2, (lon_min + lon_max) / 2], zoom_start=6)

    # Restricts map view to Florida
    m.fit_bounds([[lat_min, lon_min], [lat_max, lon_max]])

    # Adds a feature group for the highlighted roads
    road_layer = folium.FeatureGroup(name='Highlighted Roads')

    # Add coordinates for roads
    road_coordinates = [(27.994402, -81.760254), (27.947760, -81.733345)]

    # Add the road to the feature group as a polyline
    road_layer.add_child(folium.PolyLine(locations=road_coordinates, color='red'))

    # Add the feature group to the map
    m.add_child(road_layer)

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

