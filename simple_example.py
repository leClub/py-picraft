from lib.img2minecraft import MinecraftImager
from PIL import Image

size = 20 # width in minecraft

file_name = "Electronic_circuit.jpg"
img = Image.open(file_name)

mi = MinecraftImager(60)
mi.use_whools()

mi.say("drawing %s !"%file_name)

mi.draw(img)
