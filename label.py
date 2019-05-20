import pyglet
import controls
import store
from pyglet.window import key

def create(label):
    store.playername_label = pyglet.text.Label(label,
                                    'Courier_new',30,
                                    x= store.clevel.width,
                                    y = store.clevel.ysize*
                                    store.core.ts+25,
                                    anchor_x = 'right',
                                    anchor_y = 'center',
                                    batch = store.menu_bt)
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
            store.playername_label.text = Typein.text
        store.core.cplayer.name = Typein.text
    @staticmethod
    def on_key_press(symbol,modifiers):
        if symbol == key.ENTER:
            store.playername_label.text = Typein.text
            Typein.text =''
            store.clevel.pop_handlers()
            controls.handleraltered = False
        elif symbol == key.BACKSPACE:
            Typein.text = Typein.text[:-1]
            store.playername_label.text = Typein.text
        elif symbol:
            return True
