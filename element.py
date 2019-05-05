from tile import Tile
class Item(Tile):
    def __init__(self,id,x,y,img,name='',loc='',func=None):
        self.id = id
        self.x = x
        self.y = y
        self.img = img
        self.name = name
        self.loc = loc
        self.func = func
    objid = 0
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
                    SelBuild.build('wall',genloc.coor)
                else: reiter += 1
            if reiter != 0:
                Spawn.g_object(reiter,type=type)
#Spawn.g_object(3,type = 'wall')
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
            loc.connect().image=self.image['door0']
            self.closed = True
        else:
            if self.locked == False:
                loc.img = 'door1'
                loc.passable = True
                loc.connect().image=self.image['door1']
                self.closed = False
