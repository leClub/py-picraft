from instagram.client import InstagramAPI
import urllib2, StringIO
from PIL import Image
import json
from lib.img2minecraft import *

CLIENT_ID = ""
CLIENT_SECRET = ""

img_count = 5
size = 60
tag = "pattern" # "pixel"

# minecraft
mc = minecraft.Minecraft.create()
mc_x, mc_y, mc_z = mc.player.getPos()
mc_x = mc_x-20
mc_y = mc_y-size/2

# textures
whools = get_whool_colors(os.path.join(os.getcwd(), "textures/whools"))

# get data from Instagram
api = InstagramAPI(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
# popular_media = api.media_popular(count=img_count)

tagged_media = api.tag_recent_media(img_count, 1, tag)
print tagged_media

f = urllib2.urlopen(tagged_media[1])
medias = json.load(f)
    
img_urls = []
for media in medias["data"]:
    url= media["images"]['standard_resolution']["url"]
    img_urls.append(url)

# loop through images
for url in img_urls:
    print url

    # open JPG
    f = StringIO.StringIO(urllib2.urlopen(url).read())
    img = Image.open(f)

    # resize img
    img_small = resize_img(img, size)

    # convert img to texture
    img_whools = img_to_textures_list(img_small, whools)
    print "%s lines of pixels"%len(img_whools) 

    mc.postToChat( "Sending image from Instagram %s from %s"%(tag, url) )

    for i, row in enumerate(img_whools) : 
        for j, n in enumerate(row) :
            # print n
            if n != 999 :
                mc.setBlock(mc_x, mc_y+len(img_whools) - i, mc_z - int( len(row) / 2) + j, 35, n )
            else:
                mc.setBlock(mc_x, mc_y+len(img_whools)-i, mc_z - int(len(row) / 2) + j, 0 )

    mc.postToChat( "Image added !" )

