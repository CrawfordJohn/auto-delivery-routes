from flask import Flask, send_file
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

@app.route('/')
def hello_world():
    # Create a BytesIO buffer to store the plot
    buffer = io.BytesIO()

    # Create a larger figure
    plt.figure(figsize=(12, 9))  # Adjust the size as needed

    # Create the Basemap plot focused on Florida
    m = Basemap(llcrnrlon=-87.634896, llcrnrlat=24.396308,
                urcrnrlon=-79.974306, urcrnrlat=31.000888,
                resolution='i', projection='merc', lat_0=28.5, lon_0=-82.5)
    # Draw coastlines.
    m.drawcoastlines()
    # Draw a boundary around the map, fill the background.
    m.drawmapboundary(fill_color='aqua')
    # Fill continents, set lake color same as ocean color.
    m.fillcontinents(color='coral', lake_color='aqua')

    # Save the plot to the buffer
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Clear the plot to avoid memory leaks
    plt.clf()
    plt.close()

    # Return the image file
    return send_file(buffer, mimetype='image/png')

if __name__ == '__main__':
    app.run()
