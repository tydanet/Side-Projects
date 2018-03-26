import tdl

# determines window size
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

MAP_WIDTH = 80
MAP_HEIGHT = 45

color_dark_wall = (0, 0, 100)
color_dark_ground = (50, 50, 150)

class GameObject:
    # this is a generic object: the player, a monster, an item, the stairs...
    # it's always represented by a character on screen

    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx, dy):
        # move by the given amount
        if not my_map[self.x + dx][self.y + dy].blocked:
            self.x += dx
            self.y += dy

    def draw(self):
        # draw the character that represents this object at its position
        con.draw_char(self.x, self.y, self.char, self.color)

    def clear(self):
        # erase the character that represents this object
        con.draw_char(self.x, self.y, ' ', self.color, bg=None)

class Tile:
    # a tile of the map and its properties

    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked

        # by default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight

def make_map():
    global my_map

    # fill map with "ublocked" tiles
    my_map = [ [ Tile(False) for y in range(MAP_HEIGHT) ] for x in range(MAP_WIDTH) ]

    my_map[30][22].blocked = True
    my_map[30][22].block_sight = True
    my_map[50][22].blocked = True
    my_map[50][22].block_sight = True

def render_all():
    # go through all tiles and set their background color
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            wall = my_map[x][y].block_sight

            if wall:
                con.draw_char(x, y, None, fg=None, bg=color_dark_wall)

            else:
                con.draw_char(x, y, None, fg=None, bg=color_dark_ground)

    # draw all objects in the list
    for obj in objects:
        obj.draw()
                
    root.blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)

def handle_keys():
    user_input = tdl.event.key_wait()

    if user_input.key == 'ENTER' and user_input.alt:
        tdl.set_fullscreen(not tdl.get_fullscreen())

    elif user_input.key == 'ESCAPE':
        return True

    # movement keys
    if user_input.key == 'UP':
        player.move(0, -1)

    elif user_input.key == 'DOWN':
        player.move(0, 1)

    elif user_input.key == 'LEFT':
        player.move(-1, 0)
        
    elif user_input.key == 'RIGHT':
        player.move(1, 0)

# affects appearance?
tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)

# make call to initialize window
root = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title='Roguelike', fullscreen=False)
con = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT)

player = GameObject(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, '@', (255, 255, 255))
npc = GameObject(SCREEN_WIDTH//2-5, SCREEN_HEIGHT//2, '@', (255, 255, 0))
objects = [player, npc]

make_map()

# runs until window is closed
while not tdl.event.is_window_closed():
    for obj in objects:
        obj.draw()

    render_all()
    # at the end of the mainloop we always need to present changes to the scrren
    # this is called flushing
    tdl.flush()

    # so the screen doesn't get flooded with @s
    for obj in objects:
        obj.clear()

    # will have value true if escape key is pressed
    exit_game = handle_keys()

    if exit_game:
        break
