class Label(object):
    @staticmethod
    def create(label,clean):
        clean.delete()
        Label.playername_label = pyglet.text.Label(label, 
                                        'Courier_new',30,
                                        x= self.game_window.width,
                                        y = self.gamesize_y*self.tilesize+25,
                                        anchor_x = 'right',
                                        anchor_y = 'center',
                                        bt = menu_batch)
    playername_label = pyglet.text.Label(control.cplayer.name, 
                                        'Courier_new',30,
                                        x= self.game_window.width,
                                        y = self.gamesize_y*self.tilesize+25,
                                        anchor_x = 'right',
                                        anchor_y = 'center', 
                                        bt = menu_batch)
