import os
from ..lib.img2minecraft import MinecraftImager

# minecraft
mi = MinecraftImager() 
mi.use_whools() # select textures

img_dir = "out"

# US map
img = Image.open(os.path.join(img_dir, "map.png"))

# mi.draw(img.convert(mode="RGB"))
mi.say( "Creating US Map")
mi.draw(img)


# file_name = "Electronic_circuit.jpg"



