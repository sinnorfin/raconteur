import tile
import pdb
import _pickle as cPickle
import random
import pyglet.window
import store
import element
import math
from pyglet.gl import *

class Level(pyglet.window.Window):
    def __init__(self,x=10,y=10,tset=None):
        self.x = x
        self.y = y
        self.tset = tset
        super(Level, self).__init__(self.x * store.ts
                                  + store.ts * 3,
                                    self.y * store.ts
                                  + store.ts,
                                    resizable = True)
        self.xsize = self.width
        self.xcenter = self.xsize / 2
        self.ysize = self.height
        self.ycenter = self.ysize / 2
        glOrtho(0, self.width, 0, self.height, -10, 10)
    def adjust_resize(self):
        if (self.xsize != self.width or self.ysize != self.height):
            scaleto = self.width / self.xsize
            print(scaleto)
            store.ts = store.ts * scaleto
            store.ats = store.ts/2
            self.xsize = self.width
            self.ysize = self.height

    def on_resize(self,width,height):
        glViewport(0,0,width,height)
        #store.ts
        #store.ats
        if (math.fabs(width - self.xsize)<50) or (math.fabs(height - self.ysize)<50):
    #         scaletoint = scaleto*10000
    #         scaletoint = int(scaletoint)
    #         scaletoint = float(scaletoint)/10000
    #         cursor.cursor.x = cursor.cursor.x * scaletoint
    #         cursor.cursor.y = cursor.cursor.y * scaletoint
    #         #cursor.mposx = cursor.mposx * scaletoint
    #         #cursor.mposy = cursor.mposy * scaletoint
            self.width = self.xsize
            self.height = self.ysize
    def levelgen(self):
        if store.store['spt']: dellevel()
        self.levelarea = Gamearea('level',
                             [[0,store.ts*self.x],
                             [0,store.ts*self.y]])
        gcoor = [0,0]
        genid = 1
        for i in range(self.x):
            store.add(ctile(gcoor,genid),'gt')
            genid +=1
            for i in range(self.y-1):
                gcoor= [gcoor[0],gcoor[1] + 1]
                store.add(ctile(gcoor,genid),'gt')
                genid += 1
            gcoor= [gcoor[0],0]
            gcoor= [gcoor[0]+1,gcoor[1]]
        for tile in store.store['gt']:
            tile.interlace(store.store['gt'])
            store.buildmenu.build(tile,'space',
                                           tile.coor)
            if len(tile.adjl) != 8:
                store.buildmenu.build(tile,'wall',tile.coor)
class Gamearea(object):
    def __init__(self,name=None,coor=None):
        self.name = name
        self.coor = coor
def adj(tile_a, tile_b):
    for dir in range(4):
        if tile_a == tile_b.dirs[dir-1]: return True
    return False
def arrange(tile,fit=True,rotonly=False):
    imp_dirs = tile.impassable_dirs()
    nb_imp_dirs = len(imp_dirs)
    if nb_imp_dirs == 0:
        tile.mod('pil',0,rotonly)
    elif nb_imp_dirs == 1:
        if 1 in imp_dirs:
            tile.mod('cap',270,rotonly)
        elif -1 in imp_dirs:
            tile.mod('cap',90,rotonly)
        elif 0 in imp_dirs:
            tile.mod('cap',0,rotonly)
        elif 2 in imp_dirs:
            tile.mod('cap',180,rotonly)
    elif nb_imp_dirs == 2:
        if (1 in imp_dirs and -1 in imp_dirs) :
            tile.mod('wall',90,rotonly)
        elif (0 in imp_dirs and 2 in imp_dirs):
            tile.mod('wall',0,rotonly)
        elif (imp_dirs != [0,2] and imp_dirs != [-1,1]):
                if imp_dirs == [0,1]:
                    tile.mod('corner',0,rotonly)
                elif imp_dirs == [-1,0]:
                    tile.mod('corner',90,rotonly)
                elif imp_dirs == [-1,2]:
                    tile.mod('corner',180,rotonly)
                else: tile.mod('corner',270,rotonly)
    elif nb_imp_dirs == 3:
        if -1 not in imp_dirs:
            tile.mod('tsect',0,rotonly)
        elif 2 not in imp_dirs:
            tile.mod('tsect',90,rotonly)
        elif 1 not in imp_dirs:
            tile.mod('tsect',180,rotonly)
        else:
            tile.mod('tsect',270,rotonly)
    elif nb_imp_dirs == 4:
        tile.mod('fourway',0,rotonly)
    if fit == True and tile is not None:
         for fittile in tile.wadjl:
             if fittile is not None:
                 fittile.wadjl = fittile.impassable_dirs()
                 arrange(fittile,False,fittile.fix_img)
class SelBuild(object):
    def __init__(self):
        self.c = [0,False]
        self.blist = [['wall',0],['door0',0],['door1',0],['key',1]]
        self.label = pyglet.text.Label(self.blist[0][0],
                'Courier_new',30, x= store.clevel.xcenter,
                y = store.clevel.y * store.ts + 25,
                anchor_x = 'center', anchor_y = 'center')
    def next(self):
        self.label.delete()
        buildnum = len(self.blist)
        self.c[0] +=1
        if self.c[0] == buildnum:
            self.c[0] = 0
        self.c[1] = self.blist[self.c[0]][1]
        self.label = pyglet.text.Label(
                                        self.blist[self.c[0]][0],
                                        'Courier_new',30,
                                        x= store.clevel.xcenter,
                                        y = store.clevel.y *
                                        store.ts+25,
                                        anchor_x = 'center',
                                        anchor_y = 'center')
    def build(self,buildloc,type,gcoor,inid=0):
        scoor = [store.ct(gcoor[0]),
                 store.ct(gcoor[1])]
        if type != 'space' and buildloc.occup == True:
            type = 'none'
        if type == 'space':
            buildloc.sp=pyglet.sprite.Sprite(x= scoor[0],
                      y= scoor[1],
                      img = store.image['space'],
                      batch = store.map_bt)
            store.add(buildloc.sp,'spt')
        if type == 'wall':
            var_wall = ['wall','wall_v1']
            buildloc.occup = True
            buildloc.passable = False
            buildloc.img = var_wall[random.randint(0,
                                    len(var_wall)-1)]
            buildloc.sp.image =store.image[buildloc.img]
            buildloc.wadjl = buildloc.impassable_dirs(True)
            arrange(buildloc)
        if type == 'door0':
            buildloc.occup = True
            buildloc.passable = False
            buildloc.functions.append(element.Door())
            buildloc.img = 'door0'
            buildloc.sp.image=store.image['door0']
            buildloc.fix_img = True
            buildloc.wadjl = buildloc.impassable_dirs(True)
            arrange(buildloc,rotonly=True)
        if type == 'door1':
            buildloc.occup = True
            buildloc.passable = True
            buildloc.functions.append(element.Door())
            buildloc.img = 'door1'
            buildloc.sp.image=store.image['door1']
            buildloc.fix_img = True
            buildloc.wadjl = buildloc.impassable_dirs(True)
            arrange(buildloc,rotonly=True)
    @staticmethod
    def overlay(overloc,type,coor,inid=0):
        overloc = store.findtile(coor)
        lay = True
        for ol in overloc.overlays:
            if ol.name == type:
                lay = False
                store.delol(overloc,ol)
        if lay == True:
            if overloc.occup == True:
                type = 'none'
            overloc.occup = True
            if type == 'key':
                key = element.Item(x=coor[0], y=coor[1],
                           img='key',name='key',
                           loc=overloc,func='item_p')
                overloc.overlays.append(key)
                key.sp = pyglet.sprite.Sprite(x=store.ct(key.x),
                                        y=store.ct(key.y),
                                        img=store.getim(key),
                                        batch=store.item_bt)
                store.store['spo'].append(key.sp)
class Spawn(object):
    reiterlist = []
    @staticmethod
    def g_object(num,type = ''):
        reiter = 0
        if type == 'wall':
            genloclist = []
            for genloc in store.store['gt']:
                if genloc.occup == False:
                    genloclist.append(genloc)
            limit = len(genloclist)
            if num > limit: num = limit
            for i in range(num):
                genloc = genloclist[random.randint(0,len(genloclist)-1)]
                if genloc.occup == False :
                    store.buildmenu.build(genloc,'wall',genloc.coor)
                else: reiter += 1
            if reiter != 0:
                Spawn.g_object(reiter,type=type)
def ctile(gcoor,genid):
    var_space = ['space','space_v1','space','space_v2','space_v3']
    g_gen = tile.Tile(img=var_space[random.randint(0,
                   len(var_space)-1)],
                   coor=gcoor,occup=False)
    return g_gen
def ontiles(m_coor,tiles):
    for tile in tiles:
        if (m_coor[0] >= store.ct(tile.coor[0])-store.ats and
            m_coor[0] <= store.ct(tile.coor[0])+store.ats and
            m_coor[1] >= store.ct(tile.coor[1])-store.ats and
            m_coor[1] <= store.ct(tile.coor[1])+store.ats):
            return True
def standon(tocheck, against):
    return (against.coor[0] == tocheck.x and
            against.coor[1] == tocheck.y)
def savelevel():
    savelev = open('saved_level','wb')
    saved_tiles = store.store['gt']
    cPickle.dump(saved_tiles,savelev)
    for player in store.store['gp']:
        cPickle.dump(player,savelev)
    savelev.close()
def loadlevel():
    dellevel()
    for sp_overlay in store.store['spo']:
        sp_overlay.delete()
    del store.store['spo'][:]
    del store.store['gp'][:]
    loadlev = open('saved_level','rb')
    store.store['gt'] = cPickle.load(loadlev)
    store.store['gp'] = cPickle.load(loadlev)
    for g_tile in store.store['gt']:
        sp_tile = pyglet.sprite.Sprite(x=store.ct(g_tile.coor[0]),
                          y=store.ct(g_tile.coor[1]), img=getim(g_tile),
                          bt= store.map_batch)
        sp_tile.rotation=g_tile.rot
        store.store['spt'].append(sp_tile)
        if g_tile.overlays:
            for ol in g_tile.overlays:
                sp_overlay = pyglet.sprite.Sprite(x=store.ct(ol.x),y=store.ct(ol.y),
                                     img=getim(ol),
                                     bt=store.item_batch)
                store.store['spo'].append(sp_overlay)
    for g_player in store.store['gp']:
        sp_overlay = pyglet.sprite.Sprite(x=store.ct(g_player.coor[0]),
                             y=store.ct(g_player.coor[1]),
                             img = getim(g_player),
                             bt = store.player_batch)
        store.store['spo'].append(sp_overlay)
    loadlev.close()
def dellevel(delol=False):
    if delol == True:
        store.store['spo'][:] = [ol for ol in
                               store.store['spo'] if not
                               store.det_ol(ol)]
    for sp_tile in store.store['spt']:
        sp_tile.delete()
    del store.store['spt'][:]
    del store.store['gt'][:]
