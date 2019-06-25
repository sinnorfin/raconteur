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
    objid = 0

class Door(object):
    def __init__(self,buttons=[],locked = False):
        self.buttons = buttons
        # [0] button image, [1] function, baseclass?
        self.locked = locked
        self.buttons.append(['c_lock',self.lock])
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
def pickup():
    item = store.getol('item_p')
    store.cplayer.loc.overlays[:] = [x for x in store.cplayer.loc.overlays
    if x is not item]
    store.cplayer.inv.append(item)
def drop():
    store.cplayer.loc.overlays.append(
                store.cplayer.inv[-1])
    store.cplayer.inv.pop()
