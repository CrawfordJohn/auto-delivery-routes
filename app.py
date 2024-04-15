from flask import Flask, send_file
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import io

app = Flask(__name__)


@app.route('/')
def hello_world():
    # Create a BytesIO buffer to store the plot
    buffer = io.BytesIO()

    # Create the Basemap plot
    m = Basemap(width=12000000, height=9000000, projection='lcc',
                resolution='c', lat_1=45., lat_2=55, lat_0=50, lon_0=-107.)
    # draw coastlines.
    m.drawcoastlines()
    # draw a boundary around the map, fill the background.
    m.drawmapboundary(fill_color='aqua')
    # fill continents, set lake color same as ocean color.
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
