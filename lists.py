g_tiles = []
g_players = []
sp_overlays = []
sp_tiles = []
sp_gui = []

def findtile(coor):
    for g_tile in g_tiles:
        if (g_tile.coor == coor):
            return g_tile
