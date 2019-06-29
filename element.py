from tile import Tile
import store
import random
class Item(Tile):
    def __init__(self,x,y,img,name='',loc='',func=None,sp=None):
        super(Tile, self).__init__(img,sp)
        self.x = x
        self.y = y
        self.name = name
        self.loc = loc
        self.func = func
        self.buttons = [['c_pickup',self.pickup]]
    def pickup(self):
        store.cplayer.loc.overlays[:] = [x for x in store.cplayer.loc.overlays
        if x is not self]
        store.cplayer.inv.append(self)
        self.buttons[0]=(['c_drop',self.drop])
    def drop(self):
        store.cplayer.loc.overlays.append(self)
        store.cplayer.inv.remove(self)
        self.buttons[0]=(['c_pickup',self.pickup])
class Door(object):
    def __init__(self,locked = False):
        self.locked = locked
        self.buttons =[['c_lock',self.lock]]
        # [0] button image, [1] function, baseclass?
    def lock(self):
        if store.cplayer.hasitem_name('key'):
            self.locked = True
            self.buttons[0] = ['c_unl',self.unlock]
    def unlock(self):
        if store.cplayer.hasitem_name('key'):
            self.locked = False
            self.buttons[0] = ['c_lock',self.lock]
    def use(self,loc):
        if loc.passable:
            loc.img = 'door0'
            loc.passable = False
            loc.sp.image=store.image['door0']
        else:
            if not self.locked:
                loc.img = 'door1'
                loc.passable = True
                loc.sp.image=store.image['door1']
