import os
from PIL import Image
from mcpi import minecraft
import sys

def resize_img(img, _width):

    w = img.size[0]
    h = img.size[1]
    r =  h / float(w) 

    w_small = _width
    h_small = int(r*w_small)
    im_small = img.resize( (w_small,h_small ) )
    return im_small

def color_distance(rgb1,rgb2):
    '''Distance between two colors'''
    # print rgb1,rgb2
    d = (rgb1[0]-rgb2[0])**2 + (rgb1[1]-rgb2[1])**2 + (rgb1[2]-rgb2[2])**2
    # print d
    return d

class MinecraftImager():

    def __init__():
        self.mc = minecraft.Minecraft.create()
        x, y, z = mc.player.getPos()
        self.x = x+20
        self.y = y-size/2
        self.z = z
        self.textures_dir = "textures"
        self.textures = []

    def use_whools():
        whool_dir = os.path.join(self.textures_dir, "whools")

        whools = []
        fs = sorted(os.listdir(whool_dir), key = lambda k: int(k.split('_')[1].split('.')[0]))

        for f in fs :
            itmp = Image.open( os.path.join(whool_dir,f) ) 
            w = itmp.size[0]
            h = itmp.size[1]
            c =itmp.getpixel( (w/2,h/2) )
            whools.append(c)
        print "%s different whools"%len(whools)

        self.textures = whools

    def say(sentence):
        mc.postToChat( sentence )

    def img_to_textures_list(img):

        # print texture_colors
        w = img.size[0]
        h = img.size[1]

        pixels = []
        for y in range(0, h):
            col_x= []
            for x in range(0, w):
                c = img.getpixel( (x,y) )
                dists = [ color_distance(c, t) for t in self.textures ]  
                col_x.append(dists.index(min(dists)))
            pixels.append(col_x)
        return pixels


    def draw(img):

        img_textures_array = img_to_textures_list(img)

        for i, row in enumerate(img_textures_array) : 
            for j, n in enumerate(row) :
                # print n
                if n != 999 :
                    mc.setBlock(self.x, self.y+len(img_textures_array) - i, self.z - int( len(row) / 2) + j, 35, n )
                else:
                    mc.setBlock(self.x, self.y+len(img_textures_array)-i, self.z - int(len(row) / 2) + j, 0 )

