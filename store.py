import os
import pyglet
import level
import gui
pyglet.resource.path = ['res']
pyglet.resource.reindex()

map_bt = pyglet.graphics.Batch()
item_bt = pyglet.graphics.Batch()
player_bt = pyglet.graphics.Batch()
menu_bt = pyglet.graphics.Batch()
debug_bt = pyglet.graphics.Batch()
image = {}
store = {}
listname = ['gt','gp','spt','spo','spg']

def create():
    for name in listname:
        store[name]= []
def add(what,where):
    store[where].append(what)
def remove(what,where):
    pass
def empty(what):
    store[what] = []
def load_images():
    for (file) in (os.listdir('res')):
        image[file.split('.')[0]] = pyglet.resource.image(file)
        #creates pyglet images in image dictionary
        if file.split('_')[0] != 'c':
            # centers images not beginning with 'c'
            center_tile(image[file.split('.')[0]])
def center_tile(im): # puts anchor to image center
    im.anchor_x = im.width / 2
    im.anchor_y = im.height / 2
def getim(obj):
    return image[obj.img]
def findtile(coor):
    for g_tile in store['gt']:
        if (g_tile.coor == coor):
            return g_tile
def ct(num):
    tiled = (num*ts)+ats
    return tiled

load_images()
create()
ts = image['space'].width
ats = ts/2
clevel = level.Level()
clevel.levelgen()
cursor = gui.Cursor()
