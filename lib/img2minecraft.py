import os
import sys
from PIL import Image
from mcpi import minecraft
import mcpi.block as block



def color_distance(rgb1,rgb2):
    '''Distance between two colors'''
    # print rgb1,rgb2
    d = (rgb1[0]-rgb2[0])**2 + (rgb1[1]-rgb2[1])**2 + (rgb1[2]-rgb2[2])**2
    # print d
    return d

class MinecraftImager():

    def __init__(self):
        self.mc = minecraft.Minecraft.create()
        x, y, z = self.mc.player.getPos()
        self.cx = x
        self.cy = y
        self.cz = z
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


    def resize_img(self, img, size):
            w = img.size[0]
            h = img.size[1]
            r =  h / float(w) 

            w_small = size
            h_small = int(r*w_small)
            img_small = img.resize( (w_small,h_small ) ) 
            return img_small

    def process_img(self, img, size):

        img_small = self.resize_img(img, size)

        # print texture_colors
        w = img_small.size[0]
        h = img_small.size[1]

        pixels = []
        for y in range(1, h):
            col_x= []
            for x in range(1, w):
                c = img_small.getpixel( (x,y) )
                # print c
                dists = [ color_distance(c, t) for t in self.textures ]
                col_x.append(dists.index(min(dists)))
            pixels.append(col_x)
        return pixels

    def clear(self):
        """Clear eveything on stage"""
        self.mi.say("Cleaning stage")

        self.mc.setBlocks(-128,-54,-128,128,64,128,0)

        # sand ground
        bid = block.SANDSTONE.id
        self.mc.setBlocks(-128,-54,-128,128,-64,128,bid)

    def draw_bar(self, img, size=20):

        """Draw relief from grayscale image"""
        img_small = self.resize_img(img, size)
        print img_small

        # print texture_colors
        w = img_small.size[0]
        h = img_small.size[1]

        for yimg in range(1, h):
            for ximg in range(1, w):

                c = img_small.getpixel( (ximg,yimg) )
                if c != (255, 255, 255, 255) : 
                    scale =  int(( float(c[0])/255 ) * 30 )
                    for i in range( -53, -53 + scale):
                        self.mc.setBlock(self.cx - w/2 +ximg, i, self.cz - h/2 + yimg, 35, 1 )

    def draw(self, img, size=40, flat=False):
        """Draw an image"""

        pixels = self.process_img(img, size)
        h = len(pixels)
        for yimg, row in enumerate(pixels) :
            for ximg, n in enumerate(row) :
                w = len(row)
                if flat:
                    self.mc.setBlock(self.cx - w/2 +ximg, -54, self.cz - h/2 + yimg, 35, n )
                else :
                    self.mc.setBlock(self.cx + 10,  self.cy - w/2 +yimg, self.cz - h/2 + yimg, 35, n )

        print  "Image added (x:%s y:%s z:%s) !"%(self.cx, self.cy,self.cz)

        self.say( "Image added (x:%s y:%s z:%s) !"%(self.cx, self.cy,self.cz) )
