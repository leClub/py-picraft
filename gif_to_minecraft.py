import os
import json
import urllib2, StringIO

from PIL import Image
from mcpi import minecraft

from lib.img2minecraft import get_whool_colors, img_to_textures_list, resize_img

size = 20 # width in minecraft

#  Giphy API
API_KEY="dc6zaTOxFJmzC"
query = "pixel"

# minecraft


# textures
whools = get_whool_colors(os.path.join(os.getcwd(), "textures/whools"))

# Get GIF from API
giphy_url = "http://api.giphy.com/v1/gifs/search?q="+query+"&api_key="+API_KEY
f = urllib2.urlopen(giphy_url)
medias = json.load(f)

for g, gif in enumerate(medias["data"]) :
    url = gif["images"]["fixed_height"]["url"] 
    print url

    mc.postToChat( "Sending GIF image %s tagged %s"%(url, query) )

    if g == 1 : break # limit to one

    # open image stream
    f = StringIO.StringIO(urllib2.urlopen(url).read())
    img = Image.open(f)

    # extract each frames
    for i, frame in enumerate(gif_iter_frames(img)):
        print frame.info

        # format image
        img_small = resize_img(img, size)
        img_rgb = img_small.convert(mode="RGB")

        # convert img to textures array
        img_whools = img_to_textures_list(img_rgb, whools)
        print "%s lines of pixels"%len(img_whools)

        # draw on minecraft
        draw_in_minecraft()

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
