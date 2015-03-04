import os
from lib.img2minecraft import gif_iter_frames, get_whool_colors, img_to_textures_list

from mcpi import minecraft
import urllib2, StringIO
from PIL import Image
import json


size = 20

# minecraft
mc = minecraft.Minecraft.create()
mc_x, mc_y, mc_z = mc.player.getPos()
mc_x = mc_x+20
mc_y = mc_y-size/2

# textures
whools = get_whool_colors(os.path.join(os.getcwd(), "textures/whools"))

# Gif from Giphy API : https://github.com/Giphy/GiphyAPI
API_KEY="dc6zaTOxFJmzC"
query = "pixel"

giphy_url = "http://api.giphy.com/v1/gifs/search?q="+query+"&api_key="+API_KEY

f = urllib2.urlopen(giphy_url)
medias = json.load(f)


for g, gif in enumerate(medias["data"]) :
    url = gif["images"]["fixed_height"]["url"] 
    print url
    mc.postToChat( "Sending GIF image %s tagged %s"%(url, query) )

    if g == 1 : break
    f = StringIO.StringIO(urllib2.urlopen(url).read())
    img = Image.open(f)

    for i, frame in enumerate(gif_iter_frames(img)):
        print frame.info

        # resize img
        w = frame.size[0]
        h = frame.size[1]
        r =  float(w) / h  
        h_small = size
        w_small = int(r*h_small)
        img_small = img.resize( (w_small,h_small ) )

        img_rgb = img_small.convert(mode="RGB")

        # convert img to texture
        img_whools = img_to_textures_list(img_rgb, whools)
        print "%s lines of pixels"%len(img_whools)

        for i, row in enumerate(img_whools) : 
            for j, n in enumerate(row) :
                # print n
                if n != 999 :
                    mc.setBlock(mc_x, mc_y+len(img_whools) - i, mc_z - int( len(row) / 2) + j, 35, n )
                else:
                    mc.setBlock(mc_x, mc_y+len(img_whools)-i, mc_z - int(len(row) / 2) + j, 0 )
