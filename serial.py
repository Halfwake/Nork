import tile

def load_file(file_name):
    "Loads map files"
    f_map = open(file_name, "rb")
    a_map = f_map.read()
    f_map.close()
    if not read_tag("map", a_map): raise "Invalid Map!"
    grid = read_tag("grid", a_map)
    width = int(read_tag("width", a_map)[0])
    height = int(read_tag("height", a_map)[0])
    new_map = tile.Map(width, height)
    for y in range(height): #Unpacks the grid
        row, a_map = read_tag("row", a_map)
        if row == None: continue
        for x in range(width):
            a_tile, a_map = read_tag("tile", a_map)
            if a_tile == None: continue
            new_map.content[x][y] = tile.TILES[a_tile]()  
    objects = read_tag("objects", a_map) #Will unpack advanced scripting
    return new_map

    

def read_tag(tag_name, text):
    "Reads a tag and returns information on its content and position."
    tag_start = "<" + tag_name + ">"
    tag_end = "</" + tag_name + ">"
    start = text.find(tag_start)
    end = text.find(tag_end)
    if start == -1: return None, text
    if end == -1: raise "XML Error: No end tag"
    return (text[start + len(tag_start):end],
            text[end + len(tag_end):])
            
def save_file(file_name, a_map):
    "Saves map files to 'file_name'"
    f_map = open(file_name, "wb")
    try:
        f_map.write("<map>")
        f_map.write("<grid>")
        f_map.write("<height>" + str(a_map.width) + "</height>")
        f_map.write("<width>" + str(a_map.height) + "</width>")
        for row in a_map.content:
            f_map.write("<row>")
            for element in row:
                f_map.write("<tile>" + element.hash_name + "</tile>")
            f_map.write("</row>")
        f_map.write("</grid>")
        f_map.write("<objects>")
        f_map.write("</objects>")
        f_map.write("</map>")
    finally:
        f_map.close()

if __name__ == "__main__":
    print read_tag("code","<code>print 'Hello World!'</code>")
    test = tile.Map(30,30)
    save_file("fag.txt", test)
    test = load_file("fag.txt")
