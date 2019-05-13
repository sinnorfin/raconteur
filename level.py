import tile
import _pickle as cPickle
import random
import pyglet.window
import store
import sp
import element

class Level(pyglet.window.Window):
    def __init__(self,x=10,y=10,tset=None):
        self.x = x
        self.y = y
        self.tset = tset
        super(Level, self).__init__(self.x * store.core.ts
                                  + store.core.ts * 3,
                                    self.y * store.core.ts
                                  + store.core.ts,
                                    resizable= False)
        self.xsize = self.width
        self.xcenter = self.xsize / 2
        self.ysize = self.height
        self.ycenter = self.ysize / 2

    # def on_resize(self,width,height):
    #     store.ts
    #     store.core.ats
    #     self.xsize
    #     self.ysize
    #     if width - 50 > self.xsize or width + 50 < self.xsize:
    #         scaleto = float(width) / float(self.xsize)
    #         scaletoint = scaleto*10000
    #         scaletoint = int(scaletoint)
    #         scaletoint = float(scaletoint)/10000
    #         glscalef(scaletoint, scaletoint, scaletoint)
    #         store.ts = store.ts * scaletoint
    #         store.core.ats = store.ts/2
    #         cursor.cursor.x = cursor.cursor.x * scaletoint
    #         cursor.cursor.y = cursor.cursor.y * scaletoint
    #         #cursor.mposx = cursor.mposx * scaletoint
    #         #cursor.mposy = cursor.mposy * scaletoint
    #         self.xsize = width*scaletoint
    #         self.ysize = height*scaletoint
    #     width = self.xsize
    #     height = self.ysize

    def levelgen(self):
        if store.core.store['spt']: dellevel()
        self.levelarea = Gamearea(1,'level',
                             [[0,store.core.ts*self.x],
                             [0,store.core.ts*self.y]])
        gcoor = [0,0]
        genid = 1
        for i in range(self.x):
            store.core.add(ctile(gcoor,genid),'gt')
            genid +=1
            for i in range(self.y-1):
                gcoor= [gcoor[0],gcoor[1] + 1]
                store.core.add(ctile(gcoor,genid),'gt')
                genid += 1
            gcoor= [gcoor[0],0]
            gcoor= [gcoor[0]+1,gcoor[1]]
        for tile in store.core.store['gt']:
            tile.interlace(store.core.store['gt'])
            sp_tile = store.buildmenu.build(tile,'space',
                                           tile.coor,tile.id)
            if len(tile.adjl) != 8:
                sp_tile = store.buildmenu.build(tile,'wall',
                                               tile.coor)
class Gamearea(object):
    def __init__(self,id=None,name=None,coor=None):
        self.id = id
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
    for g_tile in iter(tocheck.dirs.values()):
        if g_tile and g_tile.passable == False:
            adjlist.append(g_tile)
    return adjlist
def arrange(toarrange,fit=True):
    toarrange.connect().rotation = 0
    toarrange.rot = 0
    xac = 0
    yac = 0
    if (toarrange.dirs['xam'] and
        toarrange.dirs['xam'].passable == False):
        xac= xac+1
    if (toarrange.dirs['xap'] and
        toarrange.dirs['xap'].passable == False):
        xac= xac+1
    if (toarrange.dirs['yam'] and
        toarrange.dirs['yam'].passable == False):
        yac= yac+1
    if (toarrange.dirs['yap'] and
        toarrange.dirs['yap'].passable == False):
        yac= yac+1
    if xac == 0 and yac == 0:
        toarrange.connect().image = store.core.image['pil']
        toarrange.img = 'pil'
        toarrange.tt = 's'
    elif xac == 1 and yac == 0:
        if (toarrange.dirs['xap'] and
            toarrange.dirs['xap'].passable == False):
            toarrange.connect().image=store.core.image['cap']
            toarrange.connect().rotation=270
            toarrange.img = 'cap'
            toarrange.tt = 'xm_c'
            toarrange.rot = 270
        elif (toarrange.dirs['xam'] and
            toarrange.dirs['xam'].passable == False):
            toarrange.connect().image=store.core.image['cap']
            toarrange.connect().rotation=90
            toarrange.img = 'cap'
            toarrange.tt = 'xp_c'
            toarrange.rot = 90
    elif xac == 2 and yac == 0 :
        toarrange.connect().rotation=90
        toarrange.tt = 'x'
        toarrange.connect().image=store.core.image['wall']
        toarrange.img = 'wall'
        toarrange.rot = 90
    elif xac != 0 and yac != 0:
        if xac+yac == 2:
            toarrange.connect().image=store.core.image['corner']
            toarrange.img = 'corner'
            if ((toarrange.dirs['xap'] and
                toarrange.dirs['yam']) and
                (toarrange.dirs['xap'].passable == False and
                toarrange.dirs['yam'].passable == False)):
                toarrange.connect().rotation=0
                toarrange.tt = 'cse'
                toarrange.rot = 0
            elif ((toarrange.dirs['xam'] and
                toarrange.dirs['yam']) and
                (toarrange.dirs['xam'].passable == False and
                toarrange.dirs['yam'].passable == False)):
                toarrange.connect().rotation=90
                toarrange.tt = 'csw'
                toarrange.rot = 90
            elif ((toarrange.dirs['xam'] and
                toarrange.dirs['yap']) and
                (toarrange.dirs['xam'].passable == False and
                toarrange.dirs['yap'].passable == False)):
                toarrange.connect().rotation=180
                toarrange.tt = 'cnw'
                toarrange.rot = 180
            else:
                toarrange.connect().rotation=270
                toarrange.tt = 'cne'
                toarrange.rot = 270
        elif xac+yac == 3:
            toarrange.connect().image=store.core.image['tsect']
            toarrange.img = 'tsect'
            if (not toarrange.dirs['xam'] or
                toarrange.dirs['xam'].passable == True):
                toarrange.connect().rotation=0
                toarrange.tt = 'tw'
                toarrange.rot = 0
            elif (not toarrange.dirs['yap'] or
                toarrange.dirs['yap'].passable == True):
                toarrange.connect().rotation=90
                toarrange.tt = 'tn'
                toarrange.rot = 90
            elif (not toarrange.dirs['xap'] or
                toarrange.dirs['xap'].passable == True):
                toarrange.connect().rotation=180
                toarrange.tt = 'te'
                toarrange.rot = 180
            else:
                toarrange.connect().rotation=270
                toarrange.tt = 'ts'
                toarrange.rot = 270
        else:
            toarrange.connect().image=store.core.image['fourway']
            toarrange.img = 'fourway'
            toarrange.tt = 'fw'
    else:
        if (yac == 1 and toarrange.dirs['yam'] and
            toarrange.dirs['yam'].passable == False):
            toarrange.connect().image=store.core.image['cap']
            toarrange.connect().rotation=0
            toarrange.img = 'cap'
            toarrange.tt = 'xp_c'
            toarrange.rot = 0
        elif (yac == 1 and toarrange.dirs['yap'] and
            toarrange.dirs['yap'].passable == False):
            toarrange.connect().image=store.core.image['cap']
            toarrange.connect().rotation=180
            toarrange.img = 'cap'
            toarrange.tt = 'xm_c'
            toarrange.rot = 180
        else:
            toarrange.tt = 'y'
            toarrange.connect().image=store.core.image['wall']
            toarrange.img = 'wall'
    if fit == True:
        fitnext(toarrange.wadjl)
class SelBuild(object):
    def __init__(self):
        self.c = [0,False]
        self.blist = [['wall',0],['door0',0],['door1',0],['key',1]]
        self.label = pyglet.text.Label(self.blist[0][0],
                'Courier_new',30, x= store.clevel.xcenter,
                y = store.clevel.y * store.core.ts + 25,
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
                                        store.core.ts+25,
                                        anchor_x = 'center',
                                        anchor_y = 'center')
    def build(self,buildloc,type,gcoor,inid=0):
        #sp_built = None
        scoor = [store.core.ct(gcoor[0]),
                 store.core.ct(gcoor[1])]
        if type != 'space' and buildloc.occup == True:
            type = 'none'
        if type == 'space':
            sp_built = sp.Sp_Tile(x= scoor[0],
                      y= scoor[1],
                      img = store.core.image['space'],
                      batch = store.map_bt ,id= inid)
            store.core.add(sp_built,'spt')
        if type == 'wall':
            var_wall = ['wall','wall_v1']
            buildloc.occup = True
            buildloc.passable = False
            buildloc.img = var_wall[random.randint(0,
                                    len(var_wall)-1)]
            buildloc.connect().image =store.core.image[buildloc.img]
            buildloc.wadjl = adjlist(buildloc)
            arrange(buildloc)
        if type == 'door0':
            buildloc.occup = True
            buildloc.passable = False
            door = element.Door(loc=buildloc,closed=True)
            buildloc.functions.append(door)
            buildloc.img = 'door0'
            buildloc.connect().image=store.core.image['door0']
            buildloc.wadjl = adjlist(buildloc)
            arrange(buildloc)
        if type == 'door1':
            buildloc.occup = True
            buildloc.passable = True
            door = element.Door(loc=buildloc)
            buildloc.functions.append(door)
            buildloc.img = 'door1'
            buildloc.connect().image=store.core.image['door1']
            buildloc.wadjl = adjlist(buildloc)
            arrange(buildloc)
    @staticmethod
    def overlay(overloc,type,coor,inid=0):
        overloc = store.core.findtile(coor)
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
                key = element.Item(id=element.Item.objid, x=coor[0], y=coor[1],
                           img='key',name='key',
                           loc=overloc,func='item_p')
                overloc.overlays.append(key)
                sp_overlay = sp.Sp_Tile(x=store.core.ct(key.x),
                                        y=store.core.ct(key.y),
                                        img=store.core.getim(key),
                                        batch=store.item_bt,id=key.id,
                                        ol=True)
                store.core.store['spo'].append(sp_overlay)
                element.Item.objid += 1
def coll(direc):
    collision = False
    for g_tile in store.core.store['gt']:
        if (g_tile.passable == False and
            g_tile.coor[1] == direc[0] and g_tile.coor[0] == direc[1]):
                collision = True
                return collision
    return collision
def fitnext(tile):
    for i in tile:
        i.wadjl = adjlist(i)
        arrange(i,False)
def ctile(gcoor,genid):
    var_space = ['space','space_v1','space','space_v2','space_v3']
    g_gen = tile.Tile(img=var_space[random.randint(0,
                   len(var_space)-1)],
                   id=genid,coor=gcoor,occup=False)
    return g_gen
def ontiles(m_coor,tiles):
    for tile in tiles:
        if (m_coor[0] >= store.core.ct(tile.coor[0])-store.core.ats and
            m_coor[0] <= store.core.ct(tile.coor[0])+store.core.ats and
            m_coor[1] >= store.core.ct(tile.coor[1])-store.core.ats and
            m_coor[1] <= store.core.ct(tile.coor[1])+store.core.ats):
            return True
def standon(tocheck, against):
    if (against.coor[0] == tocheck.x and
        against.coor[1] == tocheck.y) :
        standon = True
    else: standon = False
    return standon
def savelevel():
    savelev = open('saved_level','wb')
    cPickle.dump(store.core.store['gt'], savelev)
    cPickle.dump(store.core.store['gp'], savelev)
    savelev.close()
def loadlevel():
    dellevel()
    for sp_overlay in store.core.store['spo']:
        sp_overlay.delete()
    del store.core.store['spo'][:]
    del store.core.store['gp'][:]
    loadlev = open('saved_level','rb')
    store.core.store['gt'] = cPickle.load(loadlev)
    store.core.store['gp'] = cPickle.load(loadlev)
    for g_tile in store.core.store['gt']:
        sp_tile = Sp_Tile(x=store.core.ct(g_tile.coor[0]), y=store.core.ct(g_tile.coor[1]),
                          img=getim(g_tile),
                          bt= store.map_batch,id=g_tile.id)
        sp_tile.rotation=g_tile.rot
        store.core.store['spt'].append(sp_tile)
        if g_tile.overlays:
            for ol in g_tile.overlays:
                sp_overlay = Sp_Tile(x=store.core.ct(ol.x),y=store.core.ct(ol.y),
                                     img=getim(ol),
                                     bt=store.item_batch,id=ol.id,
                                     ol=True)
                store.core.store['spo'].append(sp_overlay)
    for g_player in store.core.store['gp']:
        sp_overlay = Sp_Tile(x=store.core.ct(g_player.coor[0]),
                             y=store.core.ct(g_player.coor[1]),
                             img = getim(g_player),
                             id= g_player.id,
                             bt = store.player_batch)
        store.core.store['spo'].append(sp_overlay)
    loadlev.close()
def dellevel(delol=False):
    if delol == True:
        store.core.store['spo'][:] = [ol for ol in
                               core.store['spo'] if not
                               det_ol(ol)]
    for sp_tile in store.core.store['spt']:
        sp_tile.delete()
    del store.core.store['spt'][:]
    del store.core.store['gt'][:]
