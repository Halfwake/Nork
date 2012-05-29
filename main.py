import pyglet
import game
import menu
import credit

class Game(pyglet.window.Window):
    def __init__(self, width, height):
        super(Game, self).__init__(width, height)
        pyglet.clock.set_fps_limit(30)
        self.fps_display = pyglet.clock.ClockDisplay(color = (200.0, 200.0, 200.5, 200.0))
        self.mainmenu_screen = menu.MainMenuScreen()
        self.game_screen = game.GameScreen()
        self.menu_screen = menu.MenuScreen()
        self.credit_screen = credit.CreditScreen()
    def on_draw(self):
        self.clear()
        self.fps_display.draw()
if __name__ == "__main__":
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    root = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
    pyglet.app.run()
