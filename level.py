import tile
import pdb
import _pickle as cPickle
import random
import pyglet.window
import store
import element

class Level(pyglet.window.Window):
    def __init__(self,x=10,y=10,tset=None):
        self.x = x
        self.y = y
        self.tset = tset
        super(Level, self).__init__(self.x * store.ts
                                  + store.ts * 3,
                                    self.y * store.ts
                                  + store.ts,
                                    resizable= False)
        self.xsize = self.width
        self.xcenter = self.xsize / 2
        self.ysize = self.height
        self.ycenter = self.ysize / 2

    # def on_resize(self,width,height):
    #     store.ts
    #     store.ats
    #     self.xsize
    #     self.ysize
    #     if width - 50 > self.xsize or width + 50 < self.xsize:
    #         scaleto = float(width) / float(self.xsize)
    #         scaletoint = scaleto*10000
    #         scaletoint = int(scaletoint)
    #         scaletoint = float(scaletoint)/10000
    #         glscalef(scaletoint, scaletoint, scaletoint)
    #         store.ts = store.ts * scaletoint
    #         store.ats = store.ts/2
    #         cursor.cursor.x = cursor.cursor.x * scaletoint
    #         cursor.cursor.y = cursor.cursor.y * scaletoint
    #         #cursor.mposx = cursor.mposx * scaletoint
    #         #cursor.mposy = cursor.mposy * scaletoint
    #         self.xsize = width*scaletoint
    #         self.ysize = height*scaletoint
    #     width = self.xsize
    #     height = self.ysize

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
def adj(tocheck, against):
    if (against.coor[0] == tocheck.coor[0] + 1 and
        against.coor[1] == tocheck.coor[1] or
        against.coor[0] == tocheck.coor[0] - 1 and
        against.coor[1] == tocheck.coor[1] or
        against.coor[1] == tocheck.coor[1] + 1 and
        against.coor[0] == tocheck.coor[0] or
        against.coor[1] == tocheck.coor[1] - 1 and
        against.coor[0] == tocheck.coor[0]) :
        adj = True
    else: adj = False
    return adj
def adjlist(tocheck):
    adjlist = []
    for g_tile in iter(tocheck.dirs.values()):
        if g_tile and g_tile.passable == False:
            adjlist.append(g_tile)
    return adjlist
def valid_dirs(tile):
    valid = []
    for c in range(4):
        if (tile.dirs[c-1] is not None):
            valid.append(c-1)
    return valid
def impassable_dirs(tile):
    dirs = valid_dirs(tile)
    impassable = []
    for dir in dirs:
        if tile.dirs[dir].passable == False:
            impassable.append(dir)
    return impassable
def arrange(toarrange,fit=True):
    imp_dirs = impassable_dirs(toarrange)
    nb_imp_dirs = len(imp_dirs)
    if nb_imp_dirs == 0:
        toarrange.sp.image = store.image['pil']
        toarrange.img = 'pil'
        toarrange.tt = 's'
    elif nb_imp_dirs == 1:
        if 1 in imp_dirs:
            toarrange.sp.image=store.image['cap']
            toarrange.sp.rotation=270
            toarrange.img = 'cap'
            toarrange.tt = 'xm_c'
            toarrange.rot = 270
        elif -1 in imp_dirs:
            toarrange.sp.image=store.image['cap']
            toarrange.sp.rotation=90
            toarrange.img = 'cap'
            toarrange.tt = 'xp_c'
            toarrange.rot = 90
        elif 0 in imp_dirs:
            toarrange.sp.image=store.image['cap']
            toarrange.sp.rotation=0
            toarrange.img = 'cap'
            toarrange.tt = 'xp_c'
            toarrange.rot = 0
        elif 2 in imp_dirs:
            toarrange.sp.image=store.image['cap']
            toarrange.sp.rotation=180
            toarrange.img = 'cap'
            toarrange.tt = 'xm_c'
            toarrange.rot = 180
    elif nb_imp_dirs == 2:
        if (1 in imp_dirs and -1 in imp_dirs) :
            toarrange.sp.rotation=90
            toarrange.tt = 'x'
            toarrange.sp.image=store.image['wall']
            toarrange.img = 'wall'
            toarrange.rot = 90
        elif (0 in imp_dirs and 2 in imp_dirs):
            toarrange.tt = 'y'
            toarrange.sp.image=store.image['wall']
            toarrange.img = 'wall'
        elif (imp_dirs != [0,2] and imp_dirs != [-1,1]):
                toarrange.sp.image=store.image['corner']
                toarrange.img = 'corner'
                if imp_dirs == [0,1]:
                    toarrange.sp.rotation=0
                    toarrange.tt = 'cse'
                    toarrange.rot = 0
                elif imp_dirs == [-1,0]:
                    toarrange.sp.rotation=90
                    toarrange.tt = 'csw'
                    toarrange.rot = 90
                elif imp_dirs == [-1,2]:
                    toarrange.sp.rotation=180
                    toarrange.tt = 'cnw'
                    toarrange.rot = 180
                else:
                    toarrange.sp.rotation=270
                    toarrange.tt = 'cne'
                    toarrange.rot = 270
    elif nb_imp_dirs == 3:
        toarrange.sp.image=store.image['tsect']
        toarrange.img = 'tsect'
        if -1 not in imp_dirs:
            toarrange.sp.rotation=0
            toarrange.tt = 'tw'
            toarrange.rot = 0
        elif 2 not in imp_dirs:
            toarrange.sp.rotation=90
            toarrange.tt = 'tn'
            toarrange.rot = 90
        elif 1 not in imp_dirs:
            toarrange.sp.rotation=180
            toarrange.tt = 'te'
            toarrange.rot = 180
        else:
            toarrange.sp.rotation=270
            toarrange.tt = 'ts'
            toarrange.rot = 270
    elif nb_imp_dirs == 4:
        toarrange.sp.image=store.image['fourway']
        toarrange.img = 'fourway'
        toarrange.tt = 'fw'
    if fit == True:
        fitnext(toarrange.wadjl)
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
        #sp_built = None
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
            buildloc.wadjl = adjlist(buildloc)
            arrange(buildloc)
        if type == 'door0':
            buildloc.occup = True
            buildloc.passable = False
            buildloc.functions.append(element.Door())
            buildloc.img = 'door0'
            buildloc.sp.image=store.image['door0']
            buildloc.wadjl = adjlist(buildloc)
            arrange(buildloc)
        if type == 'door1':
            buildloc.occup = True
            buildloc.passable = True
            buildloc.functions.append(element.Door())
            buildloc.img = 'door1'
            buildloc.sp.image=store.image['door1']
            buildloc.wadjl = adjlist(buildloc)
            arrange(buildloc)
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
                element.Item.objid += 1
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
#Spawn.g_object(3,type = 'wall')
def fitnext(tile):
    for i in tile:
        i.wadjl = adjlist(i)
        arrange(i,False)
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
    if (against.coor[0] == tocheck.x and
        against.coor[1] == tocheck.y) :
        standon = True
    else: standon = False
    return standon
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
