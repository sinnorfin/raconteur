import store
waypoint = False
cplayer = ''
sp_topath = ''
goal = ''
goalwp = ''
obstacles = []
distances = []
xlist = []
ylist = []
handleraltered = False
inturn = 0     
def turn():
    self.inturn += 1
    playnum = len(lists.g_players)
    if inturn == playnum:
        inturn = 0
    cplayer = lists.g_players[inturn]
    Label.create(cplayer.name, 
                  Label.playername_label)
def pushhandlers(Class):
    if handleraltered == True:
        self.game_window.pop_handlers()
        handleraltered = False
    self.game_window.push_handlers(Class)
    handleraltered = True
class Play(object):
    @store.clevel.event
    def on_key_press(self,symbol,modifiers):
        if symbol == key.UP:
            cplayer.moveup()          
        elif symbol == key.DOWN:
            cplayer.movedown()
        elif symbol == key.LEFT:
            cplayer.moveleft()
        elif symbol == key.RIGHT:
            cplayer.moveright()
        elif symbol == key.SPACE:
            if not cplayer.cols():
                if cplayer.img == 'pchar':
                    cplayer.connect()._set_image(
                                       self.image['pchar_1b'])
                    cplayer.img = 'pchar_1b'
                else: 
                    cplayer.connect()._set_image(
                                       self.image['pchar'])
                    cplayer.img = 'pchar'
                self.turn()
        elif symbol == key.B:
            if not cplayer.cols():
                if SelBuild.c[1] == 1:
                    SelBuild.overlay(SelBuild.buildlist[
                                     SelBuild.c[0]][0],
                            cplayer.coor,
                            findtile(cplayer))
                    self.turn()
                else:
                    SelBuild.build(SelBuild.buildlist[
                                        SelBuild.c[0]][0],
                            cplayer.coor,
                            findtile(cplayer))
                    self.turn()
        elif symbol == key.P:
            cplayer.addplayer()
        elif symbol == key.DELETE:
            dellevel(delol=True)
            game.newlevel()
        elif symbol == key.R:
            dellevel(delol=True)
            game.newlevel()
            Spawn.g_object(8,type = 'wall')
        elif symbol == key.S:
            clevel.savelevel()
        elif symbol == key.L:
            clevel.loadlevel()
        elif symbol == key.Q:
            SelBuild.next()
        elif symbol == key.O:
            print len(cplayer.player_bordering())
        elif symbol == key.T:
            pushhandlers(Typein)
            Typein.firstt = True
        elif symbol == key.M:
            pushhandlers(Path)
            cplayer.moveg()
    @store.clevel.event
    def on_mouse_motion(self,x,y,dx,dy):
        if (x+self.anctile > Cursor.mposx + self.tilesize or
            x+self.anctile < Cursor.mposx or 
            y+self.anctile > Cursor.mposy + self.tilesize or 
            y+self.anctile < Cursor.mposy ):
            if inarea([x,y],level.levelarea):
                Cursor.xcoor = math.floor(x/self.tilesize)
                Cursor.ycoor = math.floor(y/self.tilesize)
                Cursor.cursor = pyglet.sprite.Sprite( 
                             x =clevel.ct(Cursor.xcoor),
                             y =clevel.ct(Cursor.ycoor),
                             img = self.image['cursor'])          
                Cursor.mposx = Cursor.cursor.x 
                Cursor.mposy = Cursor.cursor.y 
                Cursor.coor = [Cursor.xcoor, Cursor.ycoor]
                Cursor.onarea = 'l'
            else: Cursor.onarea = 'o'
    @store.clevel.event
    def on_mouse_press(self,x,y,button,modifiers): 
        clickloc = findtile(Cursor.coor)
        if button == mouse.LEFT:
            if (Gui.rcm[0] and inarea(Cursor.coor,
                level.levelarea)): 
                Gui.rcm[1].click([x,y])
            elif (not Gui.rcm[0] and inarea(Cursor.coor,
                level.levelarea)):
                for func in clickloc.functions:
                    if (func.func == 'door' and
                        level.adj(cplayer,
                                      clickloc)):
                            func.use(clickloc)
            #elif lists.g_tiles:
                #for g_tile in lists.g_tiles:
                    #if Cursor.coor == g_tile.coor: 
                        #if not level.standon(
                            #cplayer, g_tile):
                                #pathto(
                                    #cplayer,g_tile)
        elif button == mouse.RIGHT:
            if inarea([x,y],level.levelarea):
                print 'MENNU'
                if Gui.rcm[0]:
                   Gui.killrcm() 
                rcm = Gui([x,y],'rcm',clickloc)
                Gui.rcm.append(rcm)
            else: print 'NOMENU'
        elif button == mouse.MIDDLE:
            print len(clickloc.functions)
