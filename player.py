import store
from sp import Sp_Tile
cid = 2 
class Player(object):   
    def __init__(self, coor, img, id=0,name = 'Player',
                 inv=None):
        self.coor = coor 
        self.img = img
        self.id = id
        self.loc = store.findtile(self.coor) 
        self.name = name
        self.inv = [] if inv is None else inv
        self.itemcount = 0
        self.look = 'pchar'
        self.mrange = 5
        sp_player = Sp_Tile(x = store.ct(self.coor[0]),
                            y = store.ct(self.coor[1]), 
                            img = store.getim(self),id = self.id,
                            batch = store.player_bt)
        store.add(self,'gp')
        store.add(sp_player,'spo')
    def connect(self):
        for sp_overlay in store.store['spo']:
            if (sp_overlay.id == self.id and 
               not sp_overlay.ol):
                return sp_overlay
    def cols(self):
        collision = False
        for g_tile in store.store['gt']:
            if (g_tile.passable == False and 
                g_tile.coor == self.coor):
                    collision = True
            else:collision = False
        return collision
    def distance(self,target):
        distance = [abs(self.coor[0]-target.coor[0]),
                    abs(self.coor[1]-target.coor[1])]
        return distance
    def player_bordering(self): #searches for spaces around player
        player_bordering = []   #could be extended to find whatever around player
        up = self.coor[1] + 1
        down = self.coor[1] - 1
        right = self.coor[0] + 1
        left = self.coor[0] - 1
        for g_tile in lists.g_tiles:
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
                level.coll([ckcoll[0],ckcoll[1]]) == False): 
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
                              img = self.image['marker2'],
                              bt = debug_batch)   
                Path.wp.append(tag)
    def moveg(self):
        Path.clean_Path()
        self.checkmv(self.loc,True)        
        Path.tagged = list(set(Path.tagged))
        for tile in Path.tagged:
            tag = pyglet.sprite.Sprite(x= store.ct(tile.coor[0]),
                          y= store.ct(tile.coor[1]),
                          img = self.image['marker'],
                          bt = debug_batch)   
            Path.tags.append(tag)
        for tagged in Path.tagged:
            Path.ptagged.append(tagged)
        if ontiles([Cursor.mposx,Cursor.mposy],Path.ptagged):
            Path.clean_Path(tags=False)
            Path.goal = store.findtile(Cursor.coor)
            Control.CurrentPlayer.pathing()
    def checkmv(self,tchk,first = False,pat=False,f=None):  
        checkdirs = [tchk.dirs['xam'],tchk.dirs['xap'],
                     tchk.dirs['yam'],tchk.dirs['yap']]
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
    def moveup(self):
        if not level.coll([self.coor[1]+1,self.coor[0]]):
            self.coor[1] += 1
            self.look = 'pcharB'
            self.connect()._set_image(self.image[self.look])
            self.connect().y = store.ct(self.coor[1])
            self.loc = store.findtile(self.coor)
            Control.turn()
    def movedown(self):
        if not level.coll([self.coor[1]-1,self.coor[0]]):
            self.coor[1] -= 1
            self.look = 'pcharF'
            self.connect()._set_image(self.image[self.look])
            self.connect().y = store.ct(self.coor[1])
            self.loc = store.findtile(self.coor)
            Control.turn()
    def moveleft(self):
        if not level.coll([self.coor[1],self.coor[0]-1]):
            self.coor[0] -= 1 
            self.look = 'pcharR'
            self.connect()._set_image(self.image[self.look])
            self.connect().x = store.ct(self.coor[0])
            self.loc = store.findtile(self.coor)
            Control.turn()
    def moveright(self):
        if not level.coll([self.coor[1],self.coor[0]+1]):
            self.coor[0] += 1
            self.look = 'pchar'
            self.connect()._set_image(self.image[self.look])
            self.connect().x = store.ct(self.coor[0])
            self.loc = store.findtile(self.coor)
            Control.turn()
    def pmove(self,path,step):
        if Path.step < len(path):
            Path.node = path[step]
            Path.anim = True 
        else: 
            Path.step = 0
            self.coor[0] = Path.goal.coor[0]
            self.coor[1] = Path.goal.coor[1]
            self.loc = store.findtile(self.coor)
            self.connect().x = store.ct(self.coor[0])
            self.connect().y = store.ct(self.coor[1])
            Control.turn()
    def addplayer(self):
        g_newplayer = Player(coor=[self.coor[0]+1,
                             self.coor[1]+1],img='pchar',id=cid)
        cid +=1
