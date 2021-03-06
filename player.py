import store
import tile
import math
import controls
import level
import pyglet.sprite
from pyglet.window import mouse
from pyglet.window import key

class Player(tile.Gameobject):
    def __init__(self, coor, img,name = 'Player',
                 inv=None):
        super(Player, self).__init__(img)
        self.coor = coor
        self.loc = store.findtile(self.coor)
        self.name = name
        self.inv = [] if inv is None else inv
        self.itemcount = 0
        self.faces = ['pcharF','pchar','pcharB','pcharR']
        self.look = 'pchar'
        self.mrange = 5
        self.sp = pyglet.sprite.Sprite(x = store.ct(self.coor[0]),
                            y = store.ct(self.coor[1]),
                            img = store.getim(self),
                            batch = store.player_bt)
        store.add(self,'gp')
        store.add(self.sp,'spo')
    def build(self,buildmenu):
        if not self.cols():
            if buildmenu.c[1] == 1:
               buildmenu.overlay(store.findtile(self.coor),
                                buildmenu.blist[buildmenu.c[0]][0],
                                self.coor)
            else:
                buildmenu.build(store.findtile(self.coor),
                                buildmenu.blist[buildmenu.c[0]][0],
                                self.coor)
            controls.turn()
    def updateols(self):
        for item in self.inv:
            item.sp.x = self.sp.x
            item.sp.y = self.sp.y
    def updateitems(self):
        for item in self.inv:
            item.x = self.coor[0]
            item.y = self.coor[1]
            item.loc = self.loc
    def cols(self):
        for g_tile in store.store['gt']:
            if (g_tile.passable == False and
                g_tile.coor == self.coor):
                    return True
        return False
    def distance(self,target):
        distance = [abs(self.coor[0]-target.coor[0]),
                    abs(self.coor[1]-target.coor[1])]
        return distance
    def player_bordering(self):
        player_bordering = []
        up = self.coor[1] + 1
        down = self.coor[1] - 1
        right = self.coor[0] + 1
        left = self.coor[0] - 1
        for g_tile in store.store['gt']:
            add = False
            if (g_tile.coor[1] == up and
                g_tile.coor[0] == right):
                    add = True
                    ckcoll = [up,right]
            elif (g_tile.coor[1] == down and
                  g_tile.coor[0] == left):
                    add = True
                    ckcoll = [down,left]
            elif (g_tile.coor[1] == up and
                  g_tile.coor[0] == left):
                    add = True
                    ckcoll = [up,left]
            elif (g_tile.coor[1] == down and
                  g_tile.coor[0] == right):
                    add = True
                    ckcoll = [down,right]
            elif (g_tile.coor[1] == up and
                  g_tile.coor[0] == self.coor[0]):
                    add = True
                    ckcoll = [up,self.coor[0]]
            elif (g_tile.coor[1] == down and
                  g_tile.coor[0] == self.coor[0]):
                    add = True
                    ckcoll = [down,self.coor[0]]
            elif (g_tile.coor[1] == self.coor[1] and
                  g_tile.coor[0] == right):
                    add = True
                    ckcoll = [self.coor[1],right]
            elif (g_tile.coor[1] == self.coor[1] and
                  g_tile.coor[0] == left):
                    add = True
                    ckcoll = [self.coor[1],left]
            if (add == True and
                not self.cols([ckcoll[0],ckcoll[1]])):
                    player_bordering.append(g_tile)
        return player_bordering
    def pathing(self):
        self.checkmv(self.loc,True,pat=True)
        Path.tagged = list(set(Path.tagged))
        if Path.pl:
            mincost = Path.pl[0].cost
            costlist=[]
            for path in Path.pl:
                costlist.append(path.cost)
            Path.cpath = Path.pl[costlist.index(min(costlist))]
            for node in Path.cpath.nodes:
                tag = pyglet.sprite.Sprite(x= store.ct(node.coor[0]),
                              y= store.ct(node.coor[1]),
                              img = store.image ['marker2'],
                              batch = store.debug_bt)
                Path.wp.append(tag)
    def moveg(self):
        Path.clean_Path()
        self.checkmv(self.loc,True)
        Path.tagged = list(set(Path.tagged))
        for tile in Path.tagged:
            tag = pyglet.sprite.Sprite(x= store.ct(tile.coor[0]),
                          y= store.ct(tile.coor[1]),
                          img = store.image ['marker'],
                          batch = store.debug_bt)
            Path.tags.append(tag)
        for tagged in Path.tagged:
            Path.ptagged.append(tagged)
        if level.ontiles([store.cursor.mposx,store.cursor.mposy],Path.ptagged):
            Path.clean_Path(tags=False)
            Path.goal = store.findtile(store.cursor.coor)
            store.cplayer.pathing()
    def checkmv(self,tchk,first = False,pat=False,f=None):
        checkdirs = [tchk.dirs[-1],tchk.dirs[1],
                     tchk.dirs[0],tchk.dirs[2]]
        if f: checkdirs.pop(checkdirs.index(f))
        if first == True:
            st_cost = Path.cost
            st_tagged = len(Path.tagged)
            for ccheck in checkdirs:
                Path.cost = st_cost
                for i in range(len(Path.tagged)-st_tagged):
                    if pat==True:Path.tagged.pop()
                if pat == True:
                    self.checkmv(ccheck,pat=True,
                                 f=tchk)
                else:
                    self.checkmv(ccheck,f=tchk)
        if (first == False and tchk.passable == True and
            Path.cost + 1 <= self.mrange):
            Path.cost += 1
            Path.tagged.append(tchk)
            st_cost = Path.cost
            st_tagged = len(Path.tagged)
            if pat == True and tchk.coor == Path.goal.coor:
                p = Path(Path.cost,[])
                for node in Path.tagged: p.nodes.append(node)
                Path.pl.append(p)
            if Path.cost != self.mrange:
                for ccheck in checkdirs:
                    Path.cost = st_cost
                    for i in range(len(Path.tagged)-st_tagged):
                        if pat == True:Path.tagged.pop()
                    if pat == True:
                        self.checkmv(ccheck,pat=True,
                                     f=tchk)
                    else:
                        self.checkmv(ccheck,f=tchk)
    def moveone(self,coor,dir,fixcoor):
        if not self.coll(coor+dir):
            self.coor[coor] += dir
            self.look = self.faces[coor+dir]
            self.sp.image=store.image [self.look]
            if coor == 0:
                self.sp.x = store.ct(self.coor[0])
            else: self.sp.y = store.ct(self.coor[1])
            self.loc = store.findtile(self.coor)
            controls.turn()
            self.updateols()
            self.updateitems()
    def coll(self,direc):
        if not (self.loc.dirs[direc].passable):
            return True
        return False
    def pmove(self,path,step):
        if Path.step < len(path):
            Path.node = path[step]
            Path.anim = True
        else:
            Path.step = 0
            self.coor[0] = Path.goal.coor[0]
            self.coor[1] = Path.goal.coor[1]
            self.loc = store.findtile(self.coor)
            self.sp.x = store.ct(self.coor[0])
            self.sp.y = store.ct(self.coor[1])
            controls.turn()
    def addplayer(self):
        g_newplayer = Player(coor=[self.coor[0]+1,
                             self.coor[1]+1],img='pchar')
        store.cid +=1
    def cloak(self):
        if not self.cols():
            if self.img == 'pchar':
                self.sp.image= store.image['pchar_1b']
                self.img = 'pchar_1b'
            else:
                self.sp.image= store.image['pchar']
                self.img = 'pchar'
            controls.turn()
    def hasitem_name(self,name):
        for item in self.inv:
            if item.name == name:
                return True
        return False
class Path(object):
    cost = 0
    tagged = []
    ptagged = []
    tags = []
    wp = []
    goal = None
    pl = []
    cpath = None
    anim = False
    step = 0
    @staticmethod
    def clean_Path(tags=True):
        Path.cost = 0
        Path.tagged[:] = []
        Path.pl[:] = []
        if Path.wp:
            for wp in Path.wp:
                wp.delete
        del Path.wp[:]
        if tags == True:
            for tag in Path.tags:
                tag.delete()
            del Path.tags[:]
    @staticmethod
    def on_key_press(symbol,modifiers):
        if symbol == key.ESCAPE:
            store.clevel.pop_handlers()
            store.handleraltered = False
            Path.clean_Path()
            del Path.ptagged[:]
            return True
    @staticmethod
    def on_mouse_motion(x,y,dx,dy):
        if (x+store.ats > store.cursor.mposx + store.ts or
            x+store.ats < store.cursor.mposx or
            y+store.ats > store.cursor.mposy + store.ts or
            y+store.ats < store.cursor.mposy ):
            if level.ontiles([x,y],Path.ptagged):
                store.cursor.xcoor = math.floor(x/store.ts)
                store.cursor.ycoor = math.floor(y/store.ts)
                store.cursor.cursor = pyglet.sprite.Sprite(
                             x =store.ct(store.cursor.xcoor),
                             y =store.ct(store.cursor.ycoor),
                             img = store.image['cursor'])
                store.cursor.mposx = x
                store.cursor.mposy = y
                store.cursor.coor = [store.cursor.xcoor, store.cursor.ycoor]
                store.cursor.onarea = 'm'
                Path.clean_Path(tags=False)
                Path.goal = store.findtile(store.cursor.coor)
                store.cplayer.pathing()
        return True
    @staticmethod
    def on_mouse_press(x,y,button,modifiers):
        if button == mouse.LEFT:
            if level.ontiles([x,y],Path.ptagged):
                Path.clean_Path()
                Path.goal = store.findtile(store.cursor.coor)
                store.cplayer.pathing()
                store.cplayer.pmove(Path.cpath.nodes,
                                            Path.step)
                del Path.ptagged[:]
                Path.clean_Path()
                store.clevel.pop_handlers()
                store.handleraltered = False
            return True
    def __init__(self,cost,nodes):
        self.cost = cost
        self.nodes = nodes
