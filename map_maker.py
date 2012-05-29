import pyglet
import tile
import pickle

f_file = open("TEST_MAP", "wb", pickle.HIGHEST_PROTOCOL)
instance = tile.Map(20, 20)
pickle.dump(instance, f_file)
