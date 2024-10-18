import numpy as np
from owslib.wcs import WebCoverageService
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.colors import to_rgba
import matplotlib.colors as mcolors
import contextily as ctx

wcs = WebCoverageService('https://service.pdok.nl/rws/ahn/wcs/v1_0?SERVICE=WCS',
                                      version='1.0.0')

def plot(x, y, normwaterstand):
    """
    Toont gebied rondom x en y. Groen ligt hoger dan waterstand en rood lager dan waterstand

    Parameters
    ----------

    x : float 
        x-coordinate 
    
    y: float
        y-coordinate

    normwaterstand: float
        waterstand
    
    Returns 
    -------
    None
        Plot van het gebied 
    """

    breedte = 600
    hoogte = 600

    bbox = (x - breedte, y - hoogte, 
            x + breedte, y + hoogte
            )
    
    resolution = 0.5
    
    raster = 'dtm_05m'
    output = wcs.getCoverage(
        identifier=raster,bbox=bbox,resx=resolution,resy=resolution,
        format='GeoTIFF',crs='EPSG:28992',interpolation='AVERAGE'
        )
    
    im = Image.open(BytesIO(output.read()))
    data = np.array(im)

    data = np.where(data > 9999, np.nan, np.where(data <= normwaterstand, 1, 2))
    
    cmap = mcolors.ListedColormap(['red', 'green'])
    bounds = [1,2,3]  
    norm = mcolors.BoundaryNorm(bounds, cmap.N)
    
    extent = [bbox[0], bbox[2], bbox[1], bbox[3]]
    
    # Plot data
    fig, ax = plt.subplots(figsize=(12, 12))
    
    im = ax.imshow(data, cmap=cmap, norm=norm, interpolation='none', extent=extent, origin='upper', alpha = 1)
    ctx.add_basemap(ax, crs='EPSG:28992', alpha = 0.6)

    facecolor_g = to_rgba('green', alpha=0.4) 
    facecolor_r = to_rgba('red', alpha=0.4) 
    
    # Labels for legend 
    legend_elements = [
        Patch(facecolor= facecolor_g, edgecolor= 'black', label=f'>NAP +{normwaterstand} m'),
        Patch(facecolor= facecolor_r, edgecolor= 'black',  label=f'<NAP +{normwaterstand} m'),
        ]

    ax.legend(handles=legend_elements, loc='upper left', title='Legenda')
    ax.set_title('Hoogtekaart (AHN4)')
    ax.set_xlabel('X-coördinaat')
    ax.set_ylabel('Y-coördinaat')
    
    plt.show()








