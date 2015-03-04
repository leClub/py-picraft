from image_to_minecraft import gif_iter_frames

import urllib2, StringIO
from PIL import Image
import json

# Gif from Giphy API : https://github.com/Giphy/GiphyAPI
API_KEY="dc6zaTOxFJmzC"
Q = "funny+cat"

giphy_url = "http://api.giphy.com/v1/gifs/search?q="+Q+"&api_key="+API_KEY

f = urllib2.urlopen(giphy_url)
medias = json.load(f)

for gif in medias["data"] :
    url = gif["images"]["fixed_height"]["url"] 
    
    f = StringIO.StringIO(urllib2.urlopen(url).read())
    img = Image.open(f)

    for i, frame in enumerate(gif_iter_frames(img)):
        print frame.info
        # frame.save('test%d.png' % i,**frame.info)
