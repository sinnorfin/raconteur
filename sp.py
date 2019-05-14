import pyglet.sprite
class Sp_Tile(pyglet.sprite.Sprite):
    def __init__(self,id,ol=False,*args,**kwargs):
        pyglet.sprite.Sprite.__init__(self,*args,**kwargs)
        self.id = id
        self.ol = ol
