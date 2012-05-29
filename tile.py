import pyglet

IMAGES = {"tile" : pyglet.image.ImageGrid(pyglet.image.load("resources/art/tile.png"), 8, 8)}
IMAGES["grass1"] = IMAGES["tile"][56]


class Tile(pyglet.sprite.Sprite):
    def __init__(self, image, blocked):
        super(Tile, self).__init__(image)
        self.blocked = blocked

class GrassTile(Tile):
    def __init__(self):
        super(GrassTile, self).__init__(IMAGES["grass1"], False)

class Map(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.content = [[GrassTile() for x in range(self.width)] for y in range(self.height)]
    def camera_grab(self, x, y, width, height):
        final = []
        for row in range(y, height):
            final.append(self.content[row][x:width])
        return final
class Camera(object):
    def __init__(self, a_map, width, height):
        self.a_map = a_map
        self.width = width
        self.height = height
        self.lock = self.a_map.camera_grab(0, 0, self.width, self.height)
    def camera_grab(self, x, y, width, height):
        self.lock = self.a_map.camera_grab(x, y, width, height)
    def draw(self, x, y):
        sprite = self.lock[0][0]
        for y,row in enumerate(self.lock):
            for x,tile in enumerate(row):
                tile.x = x
                tile.y = y
                tile.draw()
def load_file():
    pass
def save_file():
    pass
if __name__ == "__main__":
    pass
    
