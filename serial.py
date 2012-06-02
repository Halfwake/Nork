import tile
import json

def load_file(file_name):
    "Loads map files"
    f_map = open(file_name, "rb")
    try:
        loaded_file = json.load(f_map)
        new_map = tile.Map(loaded_file["width"], loaded_file["height"])
        new_map.content = map(lambda row : map(lambda item : tile.TILES[item](), row),loaded_file["content"])
        new_map.objects = loaded_file["objects"]
    finally:
        f_map.close()
    return new_map
            
def save_file(file_name, a_map):
    "Saves map files to 'file_name'"
    f_map = open(file_name, "wb")
    try:
        data_list = {}
        data_list["width"] = a_map.width
        data_list["height"] = a_map.height

        a_tiles = []
        for row in a_map.content:
            new_row = []
            for a_tile in row:
                new_row.append(a_tile.hash_name)
            a_tiles.append(new_row)
        data_list["content"] = a_tiles
        data_list["objects"] = a_map.objects
        json.dump(data_list, f_map)
    finally:
        f_map.close()

if __name__ == "__main__":
    test = tile.Map(30,30)
    save_file("fag.txt", test)
    test = load_file("fag.txt")
