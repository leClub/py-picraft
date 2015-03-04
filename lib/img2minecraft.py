import os
from PIL import Image
from mcpi import minecraft
import sys

def resize_img(_file_name, _width): 
    fp = open(_file_name , "rb")
    im = Image.open(fp) 
    print(file_name, im.format, im.size, im.mode)

    w = im.size[0]
    h = im.size[1]
    r =  h / float(w) 

    w_small = _width
    h_small = int(r*w_small)
    im_small = im.resize( (w_small,h_small ) )
    return im_small

def color_distance(rgb1,rgb2):
    '''Distance between two colors'''
    # print rgb1,rgb2
    d = (rgb1[0]-rgb2[0])**2 + (rgb1[1]-rgb2[1])**2 + (rgb1[2]-rgb2[2])**2
    # print d
    return d

def get_whool_colors(whool_dir): 
    whools = []
    fs = sorted(os.listdir(whool_dir), key = lambda k: int(k.split('_')[1].split('.')[0]))
    for f in fs :
        itmp = Image.open( os.path.join(whool_dir,f) ) 
        w = itmp.size[0]
        h = itmp.size[1]
        c =itmp.getpixel( (w/2,h/2) )
        whools.append(c)
    print "%s different whools"%len(whools)
    return whools

def img_to_textures_list(img, texture_colors):
    # print texture_colors
    w = img.size[0]
    h = img.size[1]

    pixels = []
    for y in range(0, h):
        col_x= []
        for x in range(0, w):
            c = img.getpixel( (x,y) )
            dists = [ color_distance(c, t) for t in texture_colors ]  
            col_x.append(dists.index(min(dists)))
        pixels.append(col_x)
    return pixels

def send_img_to_minecraft(file_name, size): 

    # file_name = sys.argv[1]
    img = resize_img(file_name, size)

    # textures
    whools = get_whool_colors(os.path.join(os.getcwd(), "whools"))

    # convert img to texture
    img_whools = img_to_textures_list(img, whools)
    print "%s lines of pixels"%len(img_whools) 

    # minecraft
    mc = minecraft.Minecraft.create()
    mc.postToChat( "Sending image : %s"%(file_name) )

    x, y, z = mc.player.getPos()

    for i, row in enumerate(textures) : 
        for j, n in enumerate(row) :
            # print n
            if n != 999 :
                mc.setBlock(x-5, y+len(textures) - i, z - int( len(row) / 2) + j, 35, n )
            else:
                mc.setBlock(x-5, y+len(textures)-i, z - int(len(row) / 2) + j, 0 )

    mc.postToChat( "Image added !" )

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
