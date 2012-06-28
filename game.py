import pyglet
import thread
import tile
import serial
import toolbar
import menu
import messenger

IMAGES = {"npc" : pyglet.image.ImageGrid(pyglet.image.load("resources/art/npc.png"), 8, 8)}
IMAGES["player"] = IMAGES["npc"][56]
IMAGES["baldo"] = IMAGES["npc"][57]
IMAGES["binky"] = IMAGES["npc"][58]
IMAGES["corinth"] = IMAGES["npc"][59]
IMAGES["toolbar"] = pyglet.image.load("resources/art/toolbar.png")

SOUNDS = {}
CAMERA_WIDTH = 25
CAMERA_HEIGHT = 15
class GameScreen(object):
    def __init__(self, game, save_file = None):
        messenger.Messenger.gamescreens.append(self)
        self.game = game
        self.save_file = save_file
        self.map = serial.load_file("resources/map/default_map")
        self.map.objects["player"] = Player(self.map.objects["player_start"][0],
                                            self.map.objects["player_start"][1],
                                            self)
        self.toolbar = toolbar.Toolbar()
        self.map.objects["npcs"].append(Corinth(100,100,self)) #testing NPC
        self.camera = tile.Camera(self.map, CAMERA_WIDTH, CAMERA_HEIGHT, 0, 128)
        self.lambdas = []
        self.keys = []
        self.update_start()
        if save_file:
            self.load_save(save_file)
    def update_start(self):
        "Starts all clock schedule functions."
        self.lambdas.append((lambda dt : self.map.objects["player"].move(dt, self.keys), 0.05))
        self.lambdas.append((lambda dt : self.map.objects["player"].interact(dt, self.keys), 0.05))
        for lamb in self.lambdas:
            pyglet.clock.schedule_interval(lamb[0], lamb[1])
    def update_end(self):
        "Ends all clock schedule functions. Should be used for end of mode."
        for lamb in self.lambdas: pyglet.clock.unschedule(lamb[0])
    def on_draw(self):
        self.toolbar.on_draw()
        self.camera.draw()
        for key in self.map.objects:
            if hasattr(self.map.objects[key], "draw"):
                self.map.objects[key].draw()
        for npc in self.map.objects["npcs"]:
            npc.draw()
        self.toolbar.on_draw()
    def on_key_press(self, symbol, modifiers):
        self.keys.append(symbol)
    def on_key_release(self, symbol, modifiers):
        self.keys.pop(self.keys.index(symbol))
    def on_mouse_press(self, x, y, symbol, modifiers):
        print self.camera.touch_screen(x, y)#needs work here
        self.toolbar.on_mouse_press(x, y, symbol, modifiers)
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
    def __init__(self, x, y, game):
        super(Player, self).__init__(IMAGES["player"])
        self.game = game
        self.x = x
        self.y = y
        self.speed = 10 #Pixels moved per second
        self.tool_tip = "Your glorious avatar!"
    def change_place(self, amount, axis):
        "Because lambdas are gimped pieces of shit, fuck you guido."
        if axis == "x":
            self.x += amount
        elif axis == "y":
            self.y += amount
    def interact(self, dt, keys):
        if pyglet.window.key.SPACE in keys:
            for key in self.game.map.objects:
                obj = self.game.map.objects[key]
                if key == "npcs":
                    for npc in obj:
                        if npc.proxim(self.game.map.objects["player"],15):
                            npc.talk(self.game.toolbar)
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

        
    

class TalkBack(object):
    def __init__(self, response_dict):
        self.response_dict = response_dict
        self.background = IMAGES["toolbar"]
        self.options = []
        self.create_options()
        self.reply = None
        self.npc = None
    def create_options(self):
        interval = len(self.response_dict)
        for cntr, key in enumerate(self.response_dict): #key is text
            response = self.response_dict[key]
            new_label = menu.LabelButton(key,
                                         128 / interval,
                                         64,
                                         128 / interval * cntr)
            new_label.command = lambda : self.change_reply(response)
            self.options.append(new_label)
    def change_reply(self, change):
        if change == {}:
            self.game.toolbar.mode = self.game.toolbar.last_mode
        else:
            self.npc.talk_obj = change 
            self.npc.talk(self.game.toolbar, self.talk_obj)
    def on_mouse_press(self, x, y, symbol, modifiers):
        for option in self.options:
            option.click(x, y) 
    def on_draw(self):
        self.background.blit(0,0)
        for option in self.options: option.draw()
            
class Npc(pyglet.sprite.Sprite, Collide, Interpolation):
    def __init__(self, x, y, image, game, talk_obj = None, tool_tip = None):
        super(Npc, self).__init__(image)
        self.x = x
        self.y = y
        self.game = game
        self.talk_obj = talk_obj    
        self.talk_obj.npc = self
        self.tool_tip = tool_tip
    def proxim(self, other, distance):
        if abs(self.x - other.x) <= distance and abs(self.y - other.y) <= distance:
            return True
        return False
    def talk(self, toolbar, prompt = TalkBack({"Hello!" : TalkBack({"World" : {}})})):
            prompt = prompt or self.talk_obj #can't put a self.field in default arguments
            self.talk_obj.npc = self
            self.game.toolbar.mode = self.talk_obj
          
        
                
    
class Corinth(Npc):
    def __init__(self, x, y, game, talk = None):
        super(Corinth, self).__init__(image = IMAGES["corinth"],
                                      talk_obj = TalkBack({"Hello!" : TalkBack({"World" : {}})}),
                                      tool_tip = "Pretty, but dim. Pretty dim.",
                                      x = x,
                                      y = y,
                      game = game)

