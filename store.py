import os
import pyglet
#rcm - right click menu
#core - storage object for core variables
class Store(object):
    def __init__(self):
        lists = ['gt','gp','spt','spo','spg']
        self.store = {}
        self.image = {}
        for name in lists:
            self.store[name]= []
        for (file) in (os.listdir('res')):
            self.image[file.split('.')[0]] = pyglet.resource.image(file)
            #creates pyglet images in image dictionary
            if file.split('_')[0] != 'c':
                # centers images not beginning with 'c'
                center_tile(self.image[file.split('.')[0]])
        self.ts = self.image['space'].width
        self.ats = self.ts/2
        self.inturn = 0
        self.cplayer = ''
    def add(self,what,where):
        self.store[where].append(what)
    def remove(self,what,where):
        pass
    def empty(self,what):
        self.store[what] = []
    def ct(self,num):
        tiled = (num*self.ts)+self.ats
        return tiled
    def findtile(self,coor):
        for g_tile in self.store['gt']:
            if (g_tile.coor == coor):
                return g_tile
    def getim(self,obj):
        return self.image[obj.img]
def prange(loc):
    range = core.cplayer.distance(loc)
    # range[0] = distance in absolute units on x axis [1] = y axis
    return range
def center_tile(im): # puts anchor to image center
    im.anchor_x = im.width / 2
    im.anchor_y = im.height / 2
def getol(funct):
    for ol in rcm[1].clickloc.overlays:
        if ol.func == funct:
            return ol
def delol(g_tile,ol):
    #Deletes overlay from a certain tile
    ol.connect(True,delete=True).delete()
    g_tile.overlays.remove(ol)
    if len(g_tile.overlays) == 0:
        g_tile.occup = False
