#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

from lib.img2minecraft import MinecraftImager

# minecraft
mi = MinecraftImager() 
mi.use_whools() # select textures

mi.say( "Creating US Map")

# mi.draw(img.convert(mode="RGB"))

# create US map
fig = plt.figure(figsize=(2.56, 2.56), dpi=100, frameon = False)
ax = plt.axes()

# Lambert Conformal map of USA lower 48 states
M = Basemap(llcrnrlon=-119, llcrnrlat=22, urcrnrlon=-64, urcrnrlat=49, projection='lcc', lat_1=33, lat_2=45, lon_0=-95, resolution='c', area_thresh=10000)

# draw lakes and land
M.drawmapboundary(fill_color='blue')
M.fillcontinents(color='green',lake_color='blue')

# save map
plt.savefig('out/map.png',bbox_inches='tight', pad_inches=0, dpi = 100)






# clear figure
fig.clf() 


# Load data
pop_file = 'data/US_states_pop.json'
states = json.load(open(pop_file, 'r'))

del  states["name"=="US United States"] # remove US 

years =["pop1900","pop1910","pop1920","pop1930","pop1940","pop1960","pop1950","pop1970","pop1980","pop1990"]

lngs = [ state["geo"]["properties"]["lng"]  for state in states ]
lats = [ state["geo"]["properties"]["lat"] for state in states ]

# make years
for year in years :
    pop = [ state[year] / 100000  for state in states ]

    # normalize colors in grayscale 
    colors = [ str( float(p) / ( max(pop) ) )  for p in pop ]

    # unique sizes
    sizes = [ 1 for p in pop ]

    # print lngs
    scat = M.scatter(lngs, lats, c=colors, latlon=True, s=sizes, linewidths=0)

    # plt.savefig('out/us_'+year+'.png',bbox_inches='tight', pad_inches=0, dpi = 100)
