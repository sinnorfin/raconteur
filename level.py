import lists
import cPickle
class Level:
    def __init__(self,ts,x=10,y=10,tset=None):
        self.x = x
        self.y = y
        self.ts = ts
        self.ats = self.ts / 2
        self.tset = tset
        self.levelgen(self.ts,self.x,self.y)    
    def levelgen(ts,gsx,gsy): 
        if lists.sp_tiles: dellevel()
        self.levelarea = Gamearea(1,'level',
                             [[0,ts*gsx],
                             [0,ts*gsy]])
        gcoor = [0,0]
        genid = 1
        for i in range(gsx):
            self.ctile(gcoor,genid)
            genid +=1   
            for i in range(gsy-1):
                gcoor= [gcoor[0],gcoor[1] + 1]
                self.ctile(gcoor,genid)
                genid += 1
            gcoor= [gcoor[0],0]
            gcoor= [gcoor[0]+1,gcoor[1]]
        for tile in lists.g_tiles:
            self.interlace(tile)
            SelBuild.build('space',tile.coor,tile.id)  
            if len(tile.adjl) != 8:
                SelBuild.build('wall',tile.coor)
    def ct(self,num):
        tiled = (num*self.ts)+self.ats
        return tiled
    def savelevel():
        savelev = open('saved_level','wb')
        cPickle.dump(lists.g_tiles, savelev)
        cPickle.dump(lists.g_players, savelev)
        savelev.close()     
    def loadlevel(): 
        dellevel()
        for sp_overlay in lists.sp_overlays:
            sp_overlay.delete()
        del lists.sp_overlays[:]
        del lists.g_players[:]
        loadlev = open('saved_level','rb')
        lists.g_tiles = cPickle.load(loadlev)
        lists.g_players = cPickle.load(loadlev)
        for g_tile in lists.g_tiles:
            sp_tile = Sp_Tile(x=clevel.ct(g_tile.coor[0]), y=clevel.ct(g_tile.coor[1]), 
                              img=getim(g_tile),
                              bt= map_batch,id=g_tile.id)
            sp_tile._set_rotation(g_tile.rot)
            lists.sp_tiles.append(sp_tile)
            if g_tile.overlays:
                for ol in g_tile.overlays:
                    sp_overlay = Sp_Tile(x=clevel.ct(ol.x),y=clevel.ct(ol.y),
                                         img=getim(ol),
                                         bt=item_batch,id=ol.id,
                                         ol=True) 
                    lists.sp_overlays.append(sp_overlay)      
        for g_player in lists.g_players:
            sp_overlay = Sp_Tile(x=clevel.ct(g_player.coor[0]),
                                 y=clevel.ct(g_player.coor[1]),
                                 img = getim(g_player),
                                 id= g_player.id,
                                 bt = player_batch)
            lists.sp_overlays.append(sp_overlay)   
        loadlev.close()
        Control.turn()
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
def adjlists(tocheck):
    adjlists = []
    for g_tile in tocheck.dirs.itervalues():
        if g_tile and g_tile.passable == False:
            adjlists.append(g_tile)
    for g_tile in tocheck.dirs.itervalues():
        if g_tile and g_tile.passable == False: 
            adjlists.append(g_tile)
    return adjlists
def arrange(toarrange,fit=True):
    toarrange.connect()._set_rotation(0)
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
        toarrange.connect()._set_image(self.image['pil'])
        toarrange.img = 'pil'
        toarrange.tt = 's'
    elif xac == 1 and yac == 0:
        if (toarrange.dirs['xap'] and
            toarrange.dirs['xap'].passable == False):
            toarrange.connect()._set_image(self.image['cap'])
            toarrange.connect()._set_rotation(270)
            toarrange.img = 'cap'
            toarrange.tt = 'xm_c'
            toarrange.rot = 270
        elif (toarrange.dirs['xam'] and 
            toarrange.dirs['xam'].passable == False):
            toarrange.connect()._set_image(self.image['cap'])
            toarrange.connect()._set_rotation(90)
            toarrange.img = 'cap'
            toarrange.tt = 'xp_c'
            toarrange.rot = 90
    elif xac == 2 and yac == 0 :
        toarrange.connect()._set_rotation(90)
        toarrange.tt = 'x'
        toarrange.connect()._set_image(self.image['wall'])
        toarrange.img = 'wall'
        toarrange.rot = 90
    elif xac != 0 and yac != 0:
        if xac+yac == 2:
            toarrange.connect()._set_image(self.image['corner'])
            toarrange.img = 'corner'
            if ((toarrange.dirs['xap'] and 
                toarrange.dirs['yam']) and
                (toarrange.dirs['xap'].passable == False and
                toarrange.dirs['yam'].passable == False)):
                toarrange.connect()._set_rotation(0)
                toarrange.tt = 'cse'
                toarrange.rot = 0
            elif ((toarrange.dirs['xam'] and 
                toarrange.dirs['yam']) and
                (toarrange.dirs['xam'].passable == False and
                toarrange.dirs['yam'].passable == False)):
                toarrange.connect()._set_rotation(90)
                toarrange.tt = 'csw'
                toarrange.rot = 90
            elif ((toarrange.dirs['xam'] and 
                toarrange.dirs['yap']) and
                (toarrange.dirs['xam'].passable == False and
                toarrange.dirs['yap'].passable == False)):
                toarrange.connect()._set_rotation(180)
                toarrange.tt = 'cnw'
                toarrange.rot = 180
            else:   
                toarrange.connect()._set_rotation(270)
                toarrange.tt = 'cne'
                toarrange.rot = 270
        elif xac+yac == 3:
            toarrange.connect()._set_image(self.image['tsect'])
            toarrange.img = 'tsect'
            if (not toarrange.dirs['xam'] or
                toarrange.dirs['xam'].passable == True):
                toarrange.connect()._set_rotation(0)
                toarrange.tt = 'tw'
                toarrange.rot = 0
            elif (not toarrange.dirs['yap'] or
                toarrange.dirs['yap'].passable == True):
                toarrange.connect()._set_rotation(90)
                toarrange.tt = 'tn'
                toarrange.rot = 90
            elif (not toarrange.dirs['xap'] or
                toarrange.dirs['xap'].passable == True):
                toarrange.connect()._set_rotation(180)
                toarrange.tt = 'te'
                toarrange.rot = 180
            else: 
                toarrange.connect()._set_rotation(270)
                toarrange.tt = 'ts'
                toarrange.rot = 270
        else:
            toarrange.connect()._set_image(self.image['fourway'])
            toarrange.img = 'fourway'
            toarrange.tt = 'fw'
    else: 
        if (yac == 1 and toarrange.dirs['yam'] and 
            toarrange.dirs['yam'].passable == False):
            toarrange.connect()._set_image(self.image['cap'])
            toarrange.connect()._set_rotation(0)
            toarrange.img = 'cap'
            toarrange.tt = 'xp_c'
            toarrange.rot = 0
        elif (yac == 1 and toarrange.dirs['yap'] and 
            toarrange.dirs['yap'].passable == False):
            toarrange.connect()._set_image(self.image['cap'])
            toarrange.connect()._set_rotation(180)
            toarrange.img = 'cap'
            toarrange.tt = 'xm_c'
            toarrange.rot = 180
        else:
            toarrange.tt = 'y'
            toarrange.connect()._set_image(self.image['wall'])
            toarrange.img = 'wall'
    if fit == True:
        self.fitnext(toarrange.wadjl)
def coll(direc):
    collision = False
    for g_tile in lists.g_tiles:
        if (g_tile.passable == False and
            g_tile.coor[1] == direc[0] and g_tile.coor[0] == direc[1]):
                collision = True
                return collision
    return collision
def fitnext(tile):
    for i in tile:
        i.wadjl = self.adjlists(i)
        self.arrange(i,False)
def ctile(gcoor,genid):
    var_space = ['space','space_v1','space','space_v2','space_v3']
    g_gen = Tile(img=var_space[random.randint(0,
                   len(var_space)-1)],
                   id=genid,coor=gcoor,occup=False)  
    lists.g_tiles.append(g_gen)
def interlace(tile):
    for check in lists.g_tiles:
        if (tile.coor[0] == check.coor[0] and
            abs(check.coor[1]-tile.coor[1]) == 1):
            if check.coor[1]-tile.coor[1] == -1:
                tile.dirs['yam'] = check
                tile.adjl.append(check)
            else: 
                tile.dirs['yap'] = check
                tile.adjl.append(check)
        elif (tile.coor[1] == check.coor[1] and
              abs(check.coor[0]-tile.coor[0]) == 1):
            if check.coor[0]-tile.coor[0] == -1:
                tile.dirs['xam'] = check
                tile.adjl.append(check)
            else: 
                tile.dirs['xap'] = check
                tile.adjl.append(check)
        else:
            if (abs(check.coor[0]-tile.coor[0]) == 1 and
                abs(check.coor[1]-tile.coor[1]) == 1):
                if (check.coor[0]-tile.coor[0] == -1 and
                        check.coor[1]-tile.coor[1] == -1):
                    tile.dirs['xym'] = check
                    tile.adjl.append(check)
                elif (check.coor[0]-tile.coor[0] == 1 and
                        check.coor[1]-tile.coor[1] == 1):
                    tile.dirs['xyp'] = check
                    tile.adjl.append(check)
                elif (check.coor[0]-tile.coor[0] == -1 and
                        check.coor[1]-tile.coor[1] == 1):
                    tile.dirs['yxm'] = check
                    tile.adjl.append(check)
                elif (check.coor[0]-tile.coor[0] == 1 and
                        check.coor[1]-tile.coor[1] == -1):
                    tile.dirs['yxp'] = check
                    tile.adjl.append(check)
def standon(tocheck, against):
    if (against.coor[0] == tocheck.x and 
        against.coor[1] == tocheck.y) :
        standon = True
    else: standon = False
    return standon
