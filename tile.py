import store
class Tile(object): 
    def __init__(self, img, id=0, coor=[], passable= True,
                 occup= False, tt= 's',overlays=None,
                 functions=None,adjl=None,wadjl=None,rot=0):
        self.img = img
        self.coor = coor
        self.id = id
        self.passable = passable
        self.occup = occup
        self.tt = tt
        self.overlays = [] if overlays is None else overlays
        self.functions = [] if functions is None else functions
        self.dirs = {'xam':None,'xap':None,'yam':None,
                     'yap':None,'xym':None,'xyp':None,
                     'yxm':None,'yxp':None}
        self.adjl = [] if adjl is None else adjl
        self.wadjl = [] if wadjl is None else wadjl
        self.rot = rot
    def connect(self,ol=False,delete=False):
        #ol - limits connects to overlays
        #delete - removes sprite from list
        clist = None
        if ol == True:
            clist = store.store['spo']
        else: clist = store.store['spt']
        for sp_tile in clist:
            if sp_tile.id == self.id:
                if (ol == True and sp_tile.ol == True):
                    if delete == True:
                        clist.remove(sp_tile)
                    return sp_tile
                elif ol == False: 
                    if delete == True:
                        clist.remove(sp_tile)
                    return sp_tile
    def interlace(self,g_tiles):
        for check in g_tiles:
            if (self.coor[0] == check.coor[0] and
                abs(check.coor[1]-self.coor[1]) == 1):
                if check.coor[1]-self.coor[1] == -1:
                    self.dirs['yam'] = check
                    self.adjl.append(check)
                else: 
                    self.dirs['yap'] = check
                    self.adjl.append(check)
            elif (self.coor[1] == check.coor[1] and
                  abs(check.coor[0]-self.coor[0]) == 1):
                if check.coor[0]-self.coor[0] == -1:
                    self.dirs['xam'] = check
                    self.adjl.append(check)
                else: 
                    self.dirs['xap'] = check
                    self.adjl.append(check)
            else:
                if (abs(check.coor[0]-self.coor[0]) == 1 and
                    abs(check.coor[1]-self.coor[1]) == 1):
                    if (check.coor[0]-self.coor[0] == -1 and
                            check.coor[1]-self.coor[1] == -1):
                        self.dirs['xym'] = check
                        self.adjl.append(check)
                    elif (check.coor[0]-self.coor[0] == 1 and
                            check.coor[1]-self.coor[1] == 1):
                        self.dirs['xyp'] = check
                        self.adjl.append(check)
                    elif (check.coor[0]-self.coor[0] == -1 and
                            check.coor[1]-self.coor[1] == 1):
                        self.dirs['yxm'] = check
                        self.adjl.append(check)
                    elif (check.coor[0]-self.coor[0] == 1 and
                            check.coor[1]-self.coor[1] == -1):
                        self.dirs['yxp'] = check
                        self.adjl.append(check)
