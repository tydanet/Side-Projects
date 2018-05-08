from random import randint

import colors
import tdl

# determines window size
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

MAP_WIDTH = 80
MAP_HEIGHT = 45

ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30

FOV_ALGO = 'BASIC'
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10

MAX_ROOM_MONSTERS = 3

color_dark_wall = (0, 0, 100)
color_light_wall = (130, 110, 50)
color_dark_ground = (50, 50, 150)
color_light_ground = (200, 180, 50)

game_state = 'playing'
player_action = None

class Tile:
    # a tile of the map and its properties

    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked

        # by default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight
        self.explored = False

class Rect:
    # a rectangle on the map. used to characterize a room.

    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        x = (self.x1 + self.x2) // 2
        y = (self.y1 + self.y2) // 2

        return x, y

    def intersect(self, other):
        # returns true if this rectangle intersects with another

        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

class GameObject:
    # this is a generic object: the player, a monster, an item, the stairs...
    # it's always represented by a character on screen

    def __init__(self, x, y, char, name, color, blocks=False):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks

    def move(self, dx, dy):
        # move by the given amount
        #if not my_map[self.x + dx][self.y + dy].blocked:
        if not is_blocked(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy

    def draw(self):
        global visible_tiles

        # draw the character that represents this object at its position
        if (self.x, self.y) in visible_tiles:
            con.draw_char(self.x, self.y, self.char, self.color, bg=None)

    def clear(self):
        # erase the character that represents this object
        con.draw_char(self.x, self.y, ' ', self.color, bg=None)

def is_blocked(x, y):
    if my_map[x][y].blocked:
        return True

    for obj in objects:
        if obj.blocks and obj.x == x and obj.y == y:
            return True

    return False

def create_room(room):
    global my_map

    # go through the tiles i nthe rectangle and make them passable
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            my_map[x][y].blocked = False
            my_map[x][y].block_sight = False

def create_h_tunnel(x1, x2, y):
    global my_map

    if x2 < x1:
        x1, x2 = x2, x1

    for x in range(x1, x2 + 1):
        my_map[x][y].blocked = False
        my_map[x][y].block_sight = False
    
def create_v_tunnel(y1, y2, x):
    global my_map

    if y2 < y1:
        y1, y2 = y2, y1

    for y in range(y1, y2 + 1):
        my_map[x][y].blocked = False
        my_map[x][y].block_sight = False
    
def connect_rooms(r1, r2):
    a, b = r1.center()
    x, y = r2.center()

    if randint(0, 1):
        create_h_tunnel(min(a, x), max(a, x), b)
        create_v_tunnel(min(b, y), max(b, y), x)

    else:
        create_h_tunnel(min(a, x), max(a, x), y)
        create_v_tunnel(min(b, y), max(b, y), a)

def is_visible_tile(x, y):
    global my_map

    if x >= MAP_WIDTH or x < 0:
        return False
    elif y >= MAP_HEIGHT or y < 0:
        return False
    elif my_map[x][y].blocked:
        return False
    elif my_map[x][y].block_sight:
        return False
    else:
        return True

def make_map():
    global player, my_map

    rooms = []

    # fill map with "blocked" tiles
    my_map = [ [ Tile(True) for y in range(MAP_HEIGHT) ] for x in range(MAP_WIDTH) ]

    for i in range(MAX_ROOMS):
        # randomized width and heigth
        w = randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        h = randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        # randomized position
        x = randint(0, MAP_WIDTH - w - 1)
        y = randint(0, MAP_HEIGHT - h - 1)
        # create room
        room = Rect(x, y, w, h)

        # boolean list of all intersections with existings rooms
        intersections = [ room.intersect(other) for other in rooms ]

        if not any(intersections):
            create_room(room)
            place_objects(room)
            rooms.append(room)

        if rooms == [room]:
            a, b = room.center()

            player.x = a
            player.y = b

        else:
            # connects the last two rooms
            connect_rooms(rooms[-2], rooms[-1])

def place_objects(room):
    # choose random number of monsters
    num_monsters = randint(0, MAX_ROOM_MONSTERS)

    for i in range(num_monsters):
        # choose random spot for this monster
        x = randint(room.x1+1, room.x2-1)
        y = randint(room.y1+1, room.y2-1)

        if randint(0, 100) < 80: # 80% chance of getting an orc
            # create an orc
            monster = GameObject(x, y, 'o', 'orc', colors.desaturated_green, blocks=True)
        else:
            # create a troll
            monster = GameObject(x, y, 'T', 'troll', colors.darker_green, blocks=True)

        if not is_blocked:
            objects.append(monster)

def render_all():
    global fov_recompute
    global visible_tiles

    if fov_recompute:
        fov_recompute = False
        visible_tiles = tdl.map.quickFOV(player.x, player.y,
                                         is_visible_tile,
                                         fov=FOV_ALGO,
                                         radius=TORCH_RADIUS,
                                         lightWalls=FOV_LIGHT_WALLS)

    # go through all tiles and set their background color
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            visible = (x, y) in visible_tiles
            wall = my_map[x][y].block_sight

            if not visible:
                if my_map[x][y].explored:
                    if wall:
                        con.draw_char(x, y, None, fg=None, bg=color_dark_wall)

                    else:
                        con.draw_char(x, y, None, fg=None, bg=color_dark_ground)
            else:
                my_map[x][y].explored = True
                if wall:
                    con.draw_char(x, y, None, fg=None, bg=color_light_wall)

                else:
                    con.draw_char(x, y, None, fg=None, bg=color_light_ground)

    # draw all objects in the list
    for obj in objects:
        obj.draw()
                
    root.blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)

def handle_keys():
    global fov_recompute

    user_input = tdl.event.key_wait()
    movement_keys = ['UP', 'DOWN', 'LEFT', 'RIGHT']

    if game_state == 'playing':

        if user_input.key in movement_keys:
            fov_recompute = True

        # movement keys
        if user_input.key == 'UP':
            player.move(0, -1)

        elif user_input.key == 'DOWN':
            player.move(0, 1)

        elif user_input.key == 'LEFT':
            player.move(-1, 0)
            
        elif user_input.key == 'RIGHT':
            player.move(1, 0)

    if user_input.key == 'ENTER' and user_input.alt:
        tdl.set_fullscreen(not tdl.get_fullscreen())

    elif user_input.key == 'ESCAPE':
        return 'exit'

    else:
        return 'didnt-take-turn'

# affects appearance?
tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)

# make call to initialize window
root = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title='Roguelike', fullscreen=False)
con = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT)

player = GameObject(0, 0, '@', 'player', colors.white, blocks=True)
objects = [player]

make_map()
fov_recompute = True

# runs until window is closed
while not tdl.event.is_window_closed():
    render_all()
    # at the end of the mainloop we always need to present changes to the scrren
    # this is called flushing
    tdl.flush()

    for obj in objects:
        obj.draw()

    # so the screen doesn't get flooded with @s
    for obj in objects:
        obj.clear()

    # will have value true if escape key is pressed
    player_action = handle_keys()

    if player_action == 'exit':
        break
