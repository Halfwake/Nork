import pyglet
import main

class MenuScreen(object):
    def __init__(self, game):
        self.game = game

class MainMenuScreen(object):
    def __init__(self, game):
        self.game = game

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

class LabelButton(pyglet.text.Label):
    def __init__(self, text, font_size, x, y):
        super(LabelButton, self).__init__(text,
                                          main.GAME_FONT,
                                          font_size = font_size,
                                          x = x,
                                          y = y)
        self.command =  None
    def pos(self, x, y):
        if self.x < x < self.x + (self.font_size * len(self.text)):
            if self.y < y < self.y + (self.font_size * len(self.text)):
                return True
        return False
    def click(self, x, y):
        if self.pos(x, y): self.command()
    
        
