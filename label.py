import pyglet
import controls
import store
#from pyglet.text import label
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
    playername_label = pyglet.text.Label(store.cplayer.name,
                                        'Courier_new',30,
                                        x= self.game_window.width,
                                        y = self.gamesize_y*self.tilesize+25,
                                        anchor_x = 'right',
                                        anchor_y = 'center',
                                        bt = menu_batch)
class Typein(object):
    text =''
    firstt = True
    @staticmethod
    def on_text(text):
        if Typein.firstt == True and Typein.text == 't':
            Typein.text = ''
            Typein.firstt = False
        Typein.text += text
        if Typein.firstt != True:
            Label.playername_label.text = Typein.text
        store.cplayer.name = Typein.text
    @staticmethod
    def on_key_press(symbol,modifiers):
        if symbol == key.ENTER:
            Label.playername_label.text = Typein.text
            Typein.text =''
            self.game_window.pop_handlers()
            controls.handleraltered = False
        elif symbol == key.BACKSPACE:
            Typein.text = Typein.text[:-1]
            Label.playername_label.text = Typein.text
        elif symbol:
            return True
