class Messenger(object):
    games = []
    gamescreens = []
    toolbars = []
    def switch_mode(new_mode):
        for game in games:
            game.mode = game.modes[new_mode]
