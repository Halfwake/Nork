import pyglet
import tile
import serial

IMAGES = {"npc" : pyglet.image.ImageGrid(pyglet.image.load("resources/art/npc.png"), 8, 8)}
IMAGES["player"] = IMAGES["npc"][56]
IMAGES["corinth"] = IMAGES["npc"][59]
SOUNDS = {}
CAMERA_WIDTH = 10
CAMERA_HEIGHT = 10
class GameScreen(object):
    def __init__(self, save_file = None):
        self.save_file = save_file
        if save_file:
            self.load_save(save_file)
        else:
            self.player = Player()
            self.map = serial.load_file("resources/map/default_map")
            self.camera = tile.Camera(self.map, CAMERA_WIDTH, CAMERA_HEIGHT)
            self.lambdas = []
            self.keys = []
            self.update_start()
    def update_start(self):
        "Starts all clock schedule functions."
        self.lambdas.append((lambda dt : self.player.move(dt, self.keys), 0.05))
        for lamb in self.lambdas:
            pyglet.clock.schedule_interval(lamb[0], lamb[1])
    def update_end(self):
        "Ends all clock schedule functions. Should be used for end of mode."
        for lamb in self.lambdas: pyglet.clock.unschedule(lamb[0])
    def on_draw(self):
        self.camera.draw()
        self.player.draw()
    def on_key_press(self, symbol, modifiers):
        self.keys.append(symbol)
    def on_key_release(self, symbol, modifiers):
        self.keys.pop(self.keys.index(symbol))
    def on_mouse_press(self, x, y, symbol, modifiers):
        pass #Add tooltip stuff here
    def load_save(self, save_file):
        pass

class Interpolation(object):
    "Returns a list of changes in movement."
    def interpolate(self, distance, increments, movement = "linear"):
        if movement == "linear":
            final = [float(distance) / float(increments) for i in range(1, increments + 1)]
            return final
            
            
class Collide(object):
    "All classes that inherit from Collide and Sprite can see if they collide with another sprite"
    def collide(self, other):
        #For clarity
        self_center_x = self.x + (self.width / 2)
        self_center_y = self.y + (self.height / 2)
        other_center_x = other.x + (other.x / 2)
        other_center_y = other.y + (other.y / 2)
        
        if other.x < self_center_x < other.x + other.width:
            if other.y < self_center_y < other.y + other.height:
                return True
        if self.x < other_center_x < self.x + self.width:
            if self.y < other_center_y < self.y + self.height:
                return True
        return False

class Player(pyglet.sprite.Sprite, Collide, Interpolation):
    def __init__(self):
        super(Player, self).__init__(IMAGES["player"])
        self.speed = 10 #Pixels moved per second
    def change_place(self, amount, axis):
        "Because lambdas are gimped pieces of shit, fuck you guido."
        if axis == "x":
            self.x += amount
        elif axis == "y":
            self.y += amount
    def move(self, dt, keys):
        "Moves the character."
        increments = 20 #amount of frames for movement
        if pyglet.window.key.UP in keys:
            for movement in self.interpolate(self.speed, increments):
                pyglet.clock.schedule_once(lambda dt : self.change_place(movement + movement * dt, "y"), 1 / increments)
        if pyglet.window.key.DOWN in keys:
            for movement in self.interpolate(-1 * (self.speed), increments):
                pyglet.clock.schedule_once(lambda dt : self.change_place(movement + movement * dt, "y"), 1 / increments)
        if pyglet.window.key.RIGHT in keys:
            for movement in self.interpolate(self.speed, increments):
                pyglet.clock.schedule_once(lambda dt : self.change_place(movement + movement * dt, "x"), 1 / increments)
        if pyglet.window.key.LEFT in keys:
            for movement in self.interpolate(-1 * (self.speed), increments):
                pyglet.clock.schedule_once(lambda dt : self.change_place(movement + movement * dt, "x"), 1 / increments)
                
    

