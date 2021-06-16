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


lat_sismo = float(input("Latitud del sismo [°]: "))
lon_sismo = float(input("Longitud del sismo [°]: "))
prof_sismo = input("Profundidad del sismo [km]: ")
mag_sismo = input("Magnitud del sismo: ")

definir_limites = input("Deseas definir los límites de mapa (Y/[N]): ")
mapa_con_firma = input("Deseas que aparezca tu firma en el mapa ([Y]/N): ")
if mapa_con_firma=="Y" or mapa_con_firma=="":
    mapa_firmado = True
else:
    mapa_firmado = False
nombre_imagen = input("Nombre de la imagen para guardar [mapa.png]: ")
if nombre_imagen=="":
    nombre_imagen="mapa.png"

if definir_limites=="Y":
    while True:
        latmin = float(input("Latitud minima: "))
        latmax = float(input("Latitud maxima: "))
        lonmin = float(input("Longitud minima: "))
        lonmax = float(input("Longitud maxima: "))

        if latmin < latmax and lonmin < lonmax:
            if lat_sismo >= latmin and lat_sismo <=latmax:
                if lon_sismo >= lonmin and lon_sismo <=lonmax:
                    break
                else:
                    print("Los márgenes de longitud dejan al sismo fuera del mapa")
                    lat_sismo = float(input("Latitud del sismo [°]: "))

            else:
                print("Los márgenes de latitud dejan al sismo fuera del mapa")
                lon_sismo = float(input("Longitud del sismo [°]: "))
        else: print("Error límites máximos y minimos")

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
plt.show()
