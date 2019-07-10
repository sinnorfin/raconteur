import store
class Gameobject(object):
    def __init__(self,img='',sp=None):
        self.img = img
        self.sp = sp
class Tile(Gameobject):
    def __init__(self, img, coor=[], passable= True,
                 occup= False,sp = None, overlays=None,
                 functions=None,adjl=None,wadjl=None,
                 fix_img = False):
        super(Tile, self).__init__(img,sp)
        self.coor = coor
        self.passable = passable
        self.occup = occup
        self.overlays = [] if overlays is None else overlays
        self.functions = [] if functions is None else functions
        self.dirs = {-1 :None,1 :None,0 :None,
                     2: None,'xym':None,'xyp':None,
                     'yxm':None,'yxp':None}
        self.adjl = [] if adjl is None else adjl
        self.wadjl = [] if wadjl is None else wadjl
        self.fix_img = fix_img
    def mod(self,img='',ang=0,rotonly=False):
        if not rotonly: self.sp.image=store.image[img]
        self.sp.rotation=ang
    def connect(self,ol=False,delete=False):
        #ol - limits connects to overlays
        #delete - removes sprite from list
        clist = None
        if ol == True:
            clist = store.store['spo']
        else: clist = store.store['spt']
        if (ol == True and self.sp.ol == True):
            if delete == True:
                clist.remove(self.sp)
            return sp_tile
        elif ol == False:
            if delete == True:
                clist.remove(self.sp)
            return self.sp
    def valid_dirs(self):
        valid = []
        for c in range(4):
            if (self.dirs[c-1]):
                valid.append(c-1)
        return valid
    def impassable_dirs(self):
        dirs = self.valid_dirs()
        impassable = []
        for dir in dirs:
            if self.dirs[dir].passable == False:
                impassable.append(dir)
        return impassable
    def interlace(self,g_tiles):
        for check in g_tiles:
            if (self.coor[0] == check.coor[0] and
                abs(check.coor[1]-self.coor[1]) == 1):
                if check.coor[1]-self.coor[1] == -1:
                    self.dirs[0] = check
                    self.adjl.append(check)
                else:
                    self.dirs[2] = check
                    self.adjl.append(check)
            elif (self.coor[1] == check.coor[1] and
                  abs(check.coor[0]-self.coor[0]) == 1):
                if check.coor[0]-self.coor[0] == -1:
                    self.dirs[-1] = check
                    self.adjl.append(check)
                else:
                    self.dirs[1] = check
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
