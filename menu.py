import pyglet

class MenuScreen(object):
    pass

class MainMenuScreen(object):
    pass

class Button(pyglet.sprite.Sprite):
    def __init__(self, x, y, image, command):
        super(Button, self).__init__(image)
        self.x = x
        self.y = y
        self.command = command
    def pos(self, x, y):
        if self.x < x < self.x + self.width:
            if self.y < y < self.y + self.height:
                return True
        return False
    def click(self, x, y):
        if self.pos(x, y): self.command()
        
