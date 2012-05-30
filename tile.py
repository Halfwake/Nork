import pyglet

IMAGES = {"tile" : pyglet.image.ImageGrid(pyglet.image.load("resources/art/tile.png"), 8, 8)}
IMAGES["grass1"] = IMAGES["tile"][56]

class Tile(pyglet.sprite.Sprite):
    def __init__(self, image, blocked):
        super(Tile, self).__init__(image)
        self.blocked = blocked
TILES = {}
class GrassTile(Tile):
    def __init__(self):
        super(GrassTile, self).__init__(IMAGES["grass1"], False)
        self.hash_name = "grass"
TILES["grass"] = GrassTile


class Map(object):
    "Includes an entire map file in it, can be serialized with load_file and save_file functions."
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.content = [[TILES["grass"]() for x in range(self.width)] for y in range(self.height)]
class Camera(object):
    "Camera isntances contain a visible area and can be drawn."
    def __init__(self, a_map, width, height):
        self.a_map = a_map
        self.width = width
        self.height = height
        self.batch = pyglet.graphics.Batch()
        self.camera_grab(0, 0, self.width, self.height)
    def camera_grab(self, x, y, width, height):
        "Changes the camera's view of the map."
        final = [] #Sets the starting variable
        for row in final: #Clears the old locks batch references
            for item in row:
                item.batch = None()
        for row in range(y, y + height): #Grabs the new part of the map
            final.append(self.a_map.content[row][x:x + width])
        self.lock = final #Changes the lock
        for y,row in enumerate(self.lock): #Positions the tiles in lock and gives them a batch
            for x,item in enumerate(row):
                item.x = x * item.width
                item.y = y * item.height
                item.batch = self.batch
    def draw(self):
        self.batch.draw()
def load_file(file_name):
    "Loads map files"
    f_map = open(file_name, "rb")
    try:
        width = int(f_map.readline())
        height = int(f_map.readline())
        new_map = Map(width, height)
        x, y = 0, 0
        for line in f_map.readlines():
            if line == "\n":
                y += 1
                x = 0
            else:
                new_map.content[x][y] = TILES[line[:-1]]()
                x += 1
        return new_map
            
    finally:
        f_map.close()
def save_file(file_name, a_map):
    "Saves map files to 'file_name'"
    f_map = open(file_name, "wb")
    try:
        f_map.write(str(a_map.width) + "\n")
        f_map.write(str(a_map.height) + "\n")
        for row in a_map.content:
            for element in row:
                f_map.write(element.hash_name + "\n")
            f_map.write("\n")
    finally:
        f_map.close()
        
if __name__ == "__main__":
    a_map = Map(10,10)
    save_file("test.txt", a_map)
    test = load_file("test.txt")
    x = Camera(test, 10, 10)
    print test.height
    
