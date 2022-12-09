Gversion = "alpha1"
try:
    import pyi_splash
except:
    pass
import os
import pygame
import math
import random
import json
import time

from pygame import color

try:
    os.mkdir("res")
except FileExistsError:
    pass
try:
    os.mkdir("./res/screenshots")
except FileExistsError:
    pass

pygame.init()

res = 500

window = pygame.display.set_mode((res, res))
pygame.display.set_caption("FA-Alpha-1")

temp = open("./res/game_logo.png", "wb")
temp.write(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00 \x00\x00\x00 \x08\x00\x00\x00\x00V\x11%(\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00 cHRM\x00\x00z&\x00\x00\x80\x84\x00\x00\xfa\x00\x00\x00\x80\xe8\x00\x00u0\x00\x00\xea`\x00\x00:\x98\x00\x00\x17p\x9c\xbaQ<\x00\x00\x00\x02bKGD\x00\xff\x87\x8f\xcc\xbf\x00\x00\x00\x07tIME\x07\xe5\n\x0b\x0f\x19\x1az\xd2\xa8n\x00\x00\x01/IDAT8\xcbc\xfc\xcf\x80\x1f01\x8c*`````\x81\xd2\xff\xff\xfd\x83\xea`\xfe\xfb\x8f\x81\x81\x91\x99\x11M\xc1\xdd\xb5G\xbf0000\xfc\xf1\x89\xdc\xb6\xe7-\xa3H\xaf\x0c\x9a\x02n\xb1_\xe2\xe2\xacL\x7f\xaf}\xf9/ep\xec\xa5\xea+\x11\x0e\x88\x04#,.\xde\xaf\xb7\xd0\xfc\xfdIp\xd77'~\xa6\x1d\x0f]ni\xcb\xa1;\xf2\xf7\xab{\xa76|`ge\xfa\x7f\xfb\xbf\xb6\xe8\xab\x8fhV00\xfem\xba'\x1f\xc4`\xf1\x9b\xf7\xefa\t\xb3?\xbc\x1f\xde\n\xa3*\xf8\xcf\xe4\xce\xf4\x97\xf1\x1f\x17\xc3\xff\x1f\xff\xb9\xd8\x98\x0co<\xc0P\xe0\xa5\xf5\xe6:\x07\x03\xc3\xaf\xbb\x97\xae\xdc\xfc\xfb\xe3\x82\x851\x9a\x15\x8c\x7f\xfe\x8a\x8b300|\xbfp\xeb\xc1.\x06\xc6O\xd2\xbfY\x18\x91\x15\xfc\xfa\xf5\xfd\xdb\x7f\x16f\x06\x86\xf7\xf7+5\x18\x19\xfe^}wN\x9f\x83\x81\x81\x81\xe1?\x04\xdc\xae\xd3\xd41\x89\xda\xf5\xe5\xefjcI\xfd\xc9\x1f\xbem\x0fWvX\xf4\xe6\xff\xff\xff\xf0\x80\xd2c\xfb\xf1W\\\x9c\x85Q\xca\x83\xe5\xb7<3\xb3\xa8\xad\xa2\x90<\x1br@\r\xe6\x043<\x14\x00\x00'\x8bu\x85\x8b}\xd3\xb2\x00\x00\x00%tEXtdate:create\x002021-10-11T15:25:24+00:00\xdf\x12`(\x00\x00\x00%tEXtdate:modify\x002021-10-11T15:25:24+00:00\xaeO\xd8\x94\x00\x00\x00\x00IEND\xaeB`\x82")
temp.close()

game_icon = pygame.image.load("./res/game_logo.png")

pygame.display.set_icon(game_icon)

try:
    pyi_splash.close()
except:
    pass

clock = pygame.time.Clock()
delta = 1
fps = 30

class Biome():
    def __init__(self, biome_id):
        self.biome_id = biome_id
        self.color = (0, 0, 0)

    def update(self):
        if self.biome_id == 0:
            self.color = (0, 255, 0)

        elif self.biome_id == 1:
            self.color = (100, 200, 0)

        elif self.biome_id == 2:
            self.color = (255, 255, 0)

        elif self.biome_id == 3:
            self.color = (255, 255, 255)
        
        else:
            self.color = (0, 0, 0)

class Obj():
    def __init__(self, x=0, y=0, chunk = [0, 0]):
        self.chunk = chunk
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.name = None
        self.speed = 0
        self.facing = 0 # 0 is north, 1 is east, 2 is south, 3 is west

    def update(self):
        self.x += self.dx * delta
        self.y += self.dy * delta

class Player(Obj):
    def __init__(self, x=0, y=0, chunk=[0, 0]):
        Obj.__init__(self, x, y, chunk)
        self.name = "player"
        self.speed = 0.1
        self.inventory = {}

    def render(self):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, 10, 10))

class Tree(Obj):
    def __init__(self, x=0, y=0, biome_id=-1, chunk=[0, 0]):
        Obj.__init__(self, x, y, chunk)
        self.name = "tree"
        self.biome_id = biome_id

    def render(self):
        if self.biome_id == 0 or self.biome_id == 1:
            color = (0, 100, 0)
        elif self.biome_id == 2:
            color = (200, 100, 0)
        elif self.biome_id == 3:
            color = (100, 100, 100)
        else:
            color = (255, 0, 0)

        pygame.draw.rect(window, (100, 100, 0), (self.x, self.y-20, 10, 20))
        pygame.draw.circle(window, color, (self.x+5, self.y-30), 10)

class Stone(Obj):
    def __init__(self, x=0, y=0, chunk=[0, 0]):
        Obj.__init__(self, x, y, chunk)
        self.name = "stone"

    def render(self):
        x, y = self.x, self.y
        pygame.draw.polygon(window, (100, 100, 100), ([x, y], [x+5, y-5], [x+20, y], [x+20, y+10], [x, y+10]))

class Flower(Obj):
    def __init__(self, x=0, y=0, chunk=[0, 0], color=(255, 0, 0)):
        Obj.__init__(self, x, y, chunk)
        self.name = "flower"
        self.color = color

    def render(self):
        pygame.draw.rect(window, (0, 200, 0), (self.x, self.y-1, 0.5, 1))
        pygame.draw.circle(window, self.color, (self.x+1, self.y-1.5), 2)

try:
    x = open("./res/world.json", "x")
except:
    pass

try:
    chunk_dict = json.loads(open("./res/world.json", "r").read())
except:
    chunk_dict = {}

biome = Biome(0)

try:
    seed = chunk_dict["seed"]
except:
    chunk_dict["seed"] = str(time.time())
    seed = chunk_dict["seed"]

try:
    chunk_dict["version"]
except:
    chunk_dict["version"] = Gversion

def generate_chunk(chunk_id):
    global chunk_dict
    str_chunk = f"{chunk_id}"
    if not str_chunk in chunk_dict:
        random.seed(seed+str_chunk)
        biome.biome_id = random.randint(0, 3)
        temp_obj_list = []

        num_trees = 0
        num_stone = 0
        num_flower = 0

        if biome.biome_id == 0:
            num_trees = random.randint(4, 6)
            num_stone = random.randint(0, 3)
            num_flower = random.randint(10, 50)

        elif biome.biome_id == 1:
            num_trees = random.randint(8, 10)
            num_stone = random.randint(0, 1)

        elif biome.biome_id == 2:
            num_trees = random.randint(0, 3)
            num_stone = random.randint(0, 10)

        elif biome.biome_id == 3:
            num_trees = random.randint(0, 10)
            num_stone = random.randint(0, 3)

        y = -15
        for _ in range(num_stone):
            x = random.randint(10, res-10)
            y += res//num_stone
            temp_obj_list.append([x, y, "stone"])

        y = -5
        for _ in range(num_trees):
            x = random.randint(25, res-25)
            y += res//num_trees
            temp_obj_list.append([x, y, "tree"])

        y = -2
        for _ in range(num_flower):
            x = random.randint(2, res-2)
            y += res//num_flower
            color = [(255, 0, 255), (255, 255, 255), (255, 0, 0), (255, 255, 0)]
            temp_obj_list.append([x, y, "flower", random.choice(color)])

        chunk_dict[str_chunk] = [temp_obj_list, biome.biome_id]

def distance(a1, a2):
    return math.sqrt(math.pow(a1[0]-a2[0],2)+math.pow(a1[1]-a2[1], 2))

player = Player(res//2, res//2)

font = pygame.font.Font("C:\Windows\Fonts\Arial.ttf", 16)

try:
    x = chunk_dict["player"]
except:
    x = [res//2, res//2, [0, 0]]
try:
    player.chunk = x[2]
    player.x = x[0]
    player.y = x[1]
    player.facing = x[3]
    player.inventory = x[4]
except:
    player.chunk = [0, 0]
    player.x = player.y = res//2
    player.facing = 0
    player.inventory = {}

def add_inventory(item_name, amount):
    global player
    if not(item_name in player.inventory):
        player.inventory[item_name] = 0
    player.inventory[item_name] += amount

def add_chunk(chunk, obj_data):
    global chunk_dict
    t_obj_list = []
    for i in chunk_dict[chunk][0]:
        t_obj_list.append(i)
    t_obj_list.append(obj_data)
    chunk_dict[chunk][0] = t_obj_list

obj_renderable = []
generate_chunk(player.chunk)
biome.biome_id = chunk_dict[f"{player.chunk}"][1]

debugger = -1
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                player.dy = 0

            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                player.dx = 0

            if event.key == pygame.K_LSHIFT:
                player.speed = 0.1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player.dy -= player.speed
                player.facing = 0

            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player.dy += player.speed
                player.facing = 2

            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.dx -= player.speed
                player.facing = 3

            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.dx += player.speed
                player.facing = 1

            if event.key == pygame.K_LSHIFT:
                player.speed = 1
            
            if event.key == pygame.K_0:
                player.chunk = [0, 0]
                player.x = res//2
                player.y = res//2
            
            if event.key == pygame.K_F3:
                debugger *= -1

            if event.key == pygame.K_F2:
                pygame.image.save(window, "./res/screenshots/" + str(time.time())+".png")

            if event.key == pygame.K_RETURN:
                for i in range(len(chunk_dict[f"{player.chunk}"][0])):
                    if distance(chunk_dict[f"{player.chunk}"][0][i], [player.x, player.y]) < 20:
                        if "tree" in chunk_dict[f"{player.chunk}"][0][i]:
                            add_inventory("log", 1)
                            add_inventory("sapling", 1)
                        del chunk_dict[f"{player.chunk}"][0][i]
                        break

            if event.key == pygame.K_SPACE:
                try:
                    if player.inventory["sapling"] > 0:
                        add_chunk(f"{player.chunk}", [int(player.x), int(player.y), "tree"])
                        add_inventory("sapling", -1)
                except KeyError:
                    pass

    if player.x+10 > res:
        player.chunk = [player.chunk[0]+1, player.chunk[1]]
        player.x = 0
        generate_chunk(player.chunk)
    
    elif player.x < 0:
        player.chunk = [player.chunk[0]-1, player.chunk[1]]
        player.x = res-10
        generate_chunk(player.chunk)

    if player.y+10 > res:
        player.chunk = [player.chunk[0], player.chunk[1]-1]
        player.y = 0
        generate_chunk(player.chunk)
    
    elif player.y < 0:
        player.chunk = [player.chunk[0], player.chunk[1]+1]
        player.y = res-10
        generate_chunk(player.chunk)

    if f"{player.chunk}" in chunk_dict:
        obj = chunk_dict[f"{player.chunk}"]
    else:
        generate_chunk(player.chunk)
        obj = chunk_dict[f"{player.chunk}"]

    try:
        for i in obj[0]:
            if i[2] == "tree":
                obj_renderable.append(Tree(i[0], i[1], biome.biome_id))
            elif i[2] == "stone":
                obj_renderable.append(Stone(i[0], i[1], player.chunk))
            elif i[2] == "flower":
                obj_renderable.append(Flower(i[0], i[1], player.chunk, i[3]))
    except:
        pass

    biome.biome_id = obj[1]
    biome.update()

    player.update()

    for obj in obj_renderable:
        obj.update()

    window.fill(biome.color)

    for obj in obj_renderable:
        obj.render()

    player.render()
    obj_renderable = []

    if debugger > 0:
        text = f"FPS:{int(clock.get_fps())};{player.chunk}:{int(player.x)},{int(player.y)};Biome:{biome.biome_id};"
        if Gversion != chunk_dict["version"]:
            text = text + "World out of date!"
        text = font.render(text, True, (0, 0, 0))
        textRect = text.get_rect()
        window.blit(text, textRect)
    
    pygame.display.flip()
    delta = clock.tick(fps)

chunk_dict[player.name] = [player.x, player.y, player.chunk, player.facing, player.inventory]
x = open("./res/world.json", "w")
x.write(json.dumps(chunk_dict))
x.close()
pygame.quit()
