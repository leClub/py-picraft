import os
from PIL import Image
from mcpi import minecraft
import sys


def color_distance(rgb1,rgb2):
    '''Distance between two colors'''
    # print rgb1,rgb2
    d = (rgb1[0]-rgb2[0])**2 + (rgb1[1]-rgb2[1])**2 + (rgb1[2]-rgb2[2])**2
    # print d
    return d

class MinecraftImager():

    def __init__(self, size):
        self.mc = minecraft.Minecraft.create()
        x, y, z = self.mc.player.getPos()
        self.x = x+20
        self.y = y-size/2
        self.z = z
        self.size = size
        self.textures_dir = "textures"
        self.textures = []

    def use_whools(self):
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

    def say(self, sentence):
        self.mc.postToChat( sentence )

    def process_img(self, img):

        w = img.size[0]
        h = img.size[1]
        r =  h / float(w) 

        w_small = self.size
        h_small = int(r*w_small)
        img_small = img.resize( (w_small,h_small ) )


        # print texture_colors
        w = img_small.size[0]
        h = img_small.size[1]

        pixels = []
        for y in range(0, h):
            col_x= []
            for x in range(0, w):
                c = img_small.getpixel( (x,y) )
                dists = [ color_distance(c, t) for t in self.textures ]  
                col_x.append(dists.index(min(dists)))
            pixels.append(col_x)
        return pixels


    def draw(self,img):

        img_textures_array = self.process_img(img)
        print img_textures_array

        for i, row in enumerate(img_textures_array) : 
            for j, n in enumerate(row) :
                # print n
                if n != 999 :
                    self.mc.setBlock(self.x, self.y+len(img_textures_array) - i, self.z - int( len(row) / 2) + j, 35, n )
                else:
                    self.mc.setBlock(self.x, self.y+len(img_textures_array)-i, self.z - int(len(row) / 2) + j, 0 )

        self.say( "Image added !" )
