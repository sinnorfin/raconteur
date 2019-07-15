import os
import pyglet

def add(what,where):
    store[where].append(what)
def remove(what,where):
    pass
def empty(what):
    store[what] = []
def ct(num):
    tiled = (num*ts)+ats
    return tiled
def findtile(coor):
    for g_tile in store['gt']:
        if (g_tile.coor == coor):
            return g_tile
def getim(obj):
    return image[obj.img]
def center_tile(im): # puts anchor to image center
    im.anchor_x = im.width / 2
    im.anchor_y = im.height / 2
def getol(funct):
    for ol in rcm[1].clickloc.overlays:
        if ol.func == funct:
            return ol
def delol(g_tile,ol):
    #Deletes overlay from a certain tile
    ol.sp.delete()
    g_tile.overlays.remove(ol)
    if len(g_tile.overlays) == 0:
        g_tile.occup = False
def det_ol(sp_tile):
    if sp_tile.ol:
        sp_tile.delete()
        return True

lists = ['gt','gp','spt','spo','spg']
store = {}
image = {}
pyglet.resource.path = ['res']
pyglet.resource.reindex()
for name in lists:
    store[name]= []
for (file) in (os.listdir('res')):
    image[file.split('.')[0]] = pyglet.resource.image(file)
    #creates pyglet images in image dictionary
    if file.split('_')[0] != 'c':
        # centers images not beginning with 'c'
        center_tile(image[file.split('.')[0]])
ts = image['space'].width
ats = ts/2
inturn = 0
