import os
from PIL import Image
from lib.img2minecraft import MinecraftImager

img_dir = "out"

# minecraft
mi = MinecraftImager() 
mi.use_whools() # select textures

# center map
mi.x = 0
mi.y  = -54 # 
mi.z = 0

# clean stage
# mi.clear()

size = 196

# US map
img = Image.open(os.path.join(img_dir, "map.png"))

# mi.draw(img.convert(mode="RGB"))
mi.say( "Creating US Map")
mi.draw(img, size, flat=True)


def draw_population(year):
        mi.say( "Year %s"%year)
        filename = "us_pop"+year+".png"
        img_year = Image.open(os.path.join(img_dir, filename))
        mi.draw_bar(img_year, size=size)

# draw bars
# imgs = sorted(os.listdir(img_dir))
# for img in imgs :
#     if img != "map.png":
#         year = img[6:-4]
#         if year == "1900":
#             mi.say( "Year %s"%year)
#             img_year = Image.open(os.path.join(img_dir, img))
#             mi.draw_bar(img_year, size=size)

