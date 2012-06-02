import pyglet
import serial

IMAGES = {"tile" : pyglet.image.ImageGrid(pyglet.image.load("resources/art/tile.png"), 8, 8)}
IMAGES["grass1"] = IMAGES["tile"][56]

class Tile(pyglet.sprite.Sprite):
    def __init__(self, image, blocked):
        super(Tile, self).__init__(image)
        self.tool_tip = "A curious object."
        self.blocked = blocked
TILES = {}
class GrassTile(Tile):
    def __init__(self):
        super(GrassTile, self).__init__(IMAGES["grass1"], False)
        self.tool_tip = "Fresh grazing material"
        self.hash_name = "GrassTile"
TILES["GrassTile"] = GrassTile


class Map(object):
    "Includes an entire map file in it, can be serialized with load_file and save_file functions."
    def __init__(self, width, height, player_start = (0,0)):
        self.width = width
        self.height = height
        self.content = [[TILES["GrassTile"]() for x in range(self.width)] for y in range(self.height)]
        self.objects = {}
        self.objects["player_start"] = player_start
class Camera(object):
    "Camera instances contain a visible area and can be drawn."
    def __init__(self, a_map, width, height, x_offset, y_offset):
        self.a_map = a_map
        self.width = width
        self.height = height
        self.batch = pyglet.graphics.Batch()
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.camera_grab(0, 0, self.width, self.height)
    def move_draw(self, x, y):
        self.x_offset = x
        self.y_offset = y
    def touch_screen(self, x, y):
        for key in self.a_map.objects:
            item = self.a_map.objects[key]
            if hasattr(item, "tool_tip"):
                if item.x < x < item.x + item.width:
                    if item.y < y < item.y + item.height:
                        return item.tool_tip
                
        for row in self.a_map.content:
            for item in row:
                if item.x < x < item.x + item.width:
                    if item.y < y < item.y + item.height:
                        return item.tool_tip
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
                item.x = x * item.width + self.x_offset
                item.y = y * item.height + self.y_offset
                item.batch = self.batch
    def draw(self):
        self.batch.draw()

        
if __name__ == "__main__":
    a_map = Map(10,10)
    serial.save_file("test.txt", a_map)
    test = serial.load_file("test.txt")
    x = Camera(test, 10, 10)
    print test.height
    
