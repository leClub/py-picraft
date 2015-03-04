import json
from PIL import Image
import urllib2, StringIO

from instagram.client import InstagramAPI
from lib.img2minecraft import MinecraftImager

INSTAGRAM_CLIENT_ID = ""
INSTAGRAM_CLIENT_SECRET = ""

size = 60
img_count = 5 # number of images
tag = "pattern" # "pixel"

# minecraft
mi = MinecraftImager(20)
mi.use_whools() # select textures

# get data from Instagram
api = InstagramAPI(client_id=INSTAGRAM_CLIENT_ID, client_secret=INSTAGRAM_CLIENT_SECRET)
# popular_media = api.media_popular(count=img_count)
tagged_media = api.tag_recent_media(img_count, 1, tag)

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

    mi.draw(img)

    mi.say( "Sending image from Instagram %s from %s"%(tag, url) )
