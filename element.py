from tile import Tile
import store
import random
class Item(Tile):
    def __init__(self,id,x,y,img,name='',loc='',func=None,sp=None):
        super(Tile, self).__init__(img,id,sp)
        self.x = x
        self.y = y
        self.name = name
        self.loc = loc
        self.func = func
    objid = 0

class Door(object):
    def __init__(self,func='door',loc=0,
                 closed= False,locked = False):
        self.func = func
        self.loc = loc
        self.closed = closed
        self.locked = locked
    def use(self,loc):
        if self.closed == False:
            loc.img = 'door0'
            loc.passable = False
            loc.sp.image=store.image['door0']
            self.closed = True
        else:
            if self.locked == False:
                loc.img = 'door1'
                loc.passable = True
                loc.sp.image=store.image['door1']
                self.closed = False
def lock():
    getfunc('door').locked = True
def unlock():
    getfunc('door').locked = False
def pickup():
    store.cplayer.inv.append(store.getol('item_p'))
    #store.delol(store.rcm[1].clickloc,store.getol('item_p'))
def getfunc(funct):
    for func in store.rcm[1].clickloc.functions:
        if func.func == funct:
            return func
