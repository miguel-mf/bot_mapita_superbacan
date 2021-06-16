import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.patches as mpatches
import seaborn as sns
import cartopy
import os
from matplotlib.image import imread
from crea_mapa import *

def mapita_superbacan(lat_sismo,lon_sismo,prof_sismo,mag_sismo,limites=(),mapa_firmado=True)
    nombre_imagen = 'mapita_superbacan.png'
    if limites:
        if limites(0) < limites(1):
            limites_mapas_y = (limites(0), limites(1))
        else:
            limites_mapas_y = (limites(1), limites(0))
        if limites(2) < limites(3):
            limites_mapas_x = (limites(2), limites(3))
        else:
            limites_mapas_x = (limites(3), limites(2))
    else:

        limites_mapas_y = [(-24, -16), (-28, -20), (-32, -24), (-36, -28),
                            (-40, -32), (-44, -36), (-48, -40), (-52, -44),
                            (-56, -48)]

        limites_mapas_x = [(-74, -65.5), (-74, -66), (-75, -68), (-76, -69.5),
                           (-77, -69.5), (-77,-70.5), (-79,-71), (-78,-71),
                           (-76,-66)]


        # Encontrar el que esté mas centrado -> que la distancia al promedio del mapa
        # sea menor
        distancias = []
        for tupla in limites_mapas_y:
            ymin, ymax = tupla
            promedio_lat = (ymin + ymax)/2
            dist_al_promedio = np.sqrt((promedio_lat - lat_sismo)**2)
            distancias.append(dist_al_promedio)

        mapa_minima_distancia = np.argmin(distancias)
        c = mapa_minima_distancia
        latmin, latmax = limites_mapas_y[c]
        lonmin, lonmax = limites_mapas_x[c]



    # Acá empieza la figura
    f = plt.figure(figsize=(8,7))
    ax0 = plt.axes(projection = ccrs.PlateCarree())
    if definir_limites=="Y":
        plotMap(ax0, lonmin, lonmax, latmin, latmax, rios=False, ciudades=False)
    else:
        plotMap(ax0, lonmin, lonmax, latmin, latmax, rios=True, ciudades=True)

    ax0.scatter(lon_sismo, lat_sismo,  marker='*', s=1000, c='tomato', zorder=20)
    props = dict(boxstyle='round', facecolor='white', alpha=0.8, zorder=10)
    texto_caja = "Profundidad: %s km \n Magnitud: %s"%(prof_sismo, mag_sismo)

    extra = 0
    extra2 = 0
    if len(prof_sismo)>=3:
        extra = -0.1 * (len(prof_sismo) - 2)
    if definir_limites=="Y":
        extra = 4
        extra2 = 4
    ax0.text(lon_sismo - 2.0 + extra, lat_sismo + 0.2 + extra2, texto_caja,
             fontsize=10, verticalalignment='top', bbox=props, zorder=20)

    # Cajita con el nombre de instagram:
    if mapa_firmado:
        props = dict(boxstyle='round', facecolor='mediumvioletred', alpha=0.6)
        ax0.text(0.04, 0.07, "@srta.replica \n María Constanza Flores",
                 transform=ax0.transAxes, fontsize=12, verticalalignment='top',
                 bbox=props)

    plt.tight_layout()
    f.savefig(nombre_imagen)

