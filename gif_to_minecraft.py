import os
import json
import urllib2, StringIO

from PIL import Image
from lib.img2minecraft import MinecraftImager

size = 20 # image width 
API_KEY="dc6zaTOxFJmzC" #  Giphy API
query = "pixel"

# minecraft
mi = MinecraftImager(20) 
mi.use_whools() # select textures

# get GIF from API
giphy_url = "http://api.giphy.com/v1/gifs/search?q="+query+"&api_key="+API_KEY
f = urllib2.urlopen(giphy_url)
medias = json.load(f)

# function to iterate over images in GIF file
def gif_iter_frames(im):
    try:
        i= 0
        while 1:
            im.seek(i)
            imframe = im.copy()
            if i == 0: 
                palette = imframe.getpalette()
            else:
                imframe.putpalette(palette)
            yield imframe
            i += 1
    except EOFError:
        pass

for g, gif in enumerate(medias["data"]) :
    url = gif["images"]["fixed_height"]["url"] 
    print url

    mi.say( "Sending GIF image %s tagged %s"%(url, query) )
    if g == 1 : break # limit to one

    # open image stream
    f = StringIO.StringIO(urllib2.urlopen(url).read())
    img = Image.open(f)

    # extract each frames
    for i, frame in enumerate(gif_iter_frames(img)):
        print frame.info

        # draw on minecraft
        mi.draw(img.convert(mode="RGB"))
