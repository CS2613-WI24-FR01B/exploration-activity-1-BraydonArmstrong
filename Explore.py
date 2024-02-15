import pygame
import os
import math
import editor
import webbrowser
pygame.init()

clock = pygame.time.Clock()

from pygame.locals import (
    K_SPACE,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

realscreen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT], pygame.RESIZABLE)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((50, 50))
        self.surf.fill((255, 165, 0))
        self.surf.set_colorkey((0,0,0))
        self.rect = self.surf.get_rect()
        self.x = 0
        self.y = 0
        self.speedy = 0
        self.speedx = MOVE_SPEED
        self.ground = 500
        self.grounded = False

class Block(pygame.sprite.Sprite):
    def __init__(self):
        super(Block, self).__init__()
        self.surf = pygame.Surface((50, 50))
        self.surf.fill((255, 255, 255))
        self.surf.fill((0,0,0), self.surf.get_rect().inflate(-2,-2))
        self.rect = self.surf.get_rect()

class Spike(pygame.sprite.Sprite):
    def __init__(self):
        super(Spike, self).__init__()
        self.surf = pygame.Surface((50, 50))
        self.verts = []

class Orb(pygame.sprite.Sprite):
    def __init__(self):
        super(Orb, self).__init__()
        self.surf = pygame.Surface((50, 50))
        self.used = False

class BlueOrb(pygame.sprite.Sprite):
    def __init__(self):
        super(BlueOrb, self).__init__()
        self.surf = pygame.Surface((50, 50))
        self.used = False

class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super(Ship, self).__init__()
        self.surf = pygame.Surface((50, 150))
        self.surf.fill((0, 0, 0))
        self.surf.fill((255,0,255), self.surf.get_rect().inflate(-15,-15))
        self.used = False

class Cube(pygame.sprite.Sprite):
    def __init__(self):
        super(Cube, self).__init__()
        self.surf = pygame.Surface((50, 150))
        self.surf.fill((0, 0, 0))
        self.surf.fill((0,255,0), self.surf.get_rect().inflate(-15,-15))
        self.used = False

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        self.surf = pygame.Surface((50, 150))
        self.surf.fill((0, 0, 0))
        self.surf.fill((255,0,0), self.surf.get_rect().inflate(-15,-15))
        self.used = False

class Ufo(pygame.sprite.Sprite):
    def __init__(self):
        super(Ufo, self).__init__()
        self.surf = pygame.Surface((50, 150))
        self.surf.fill((0, 0, 0))
        self.surf.fill((255,200,0), self.surf.get_rect().inflate(-15,-15))
        self.used = False

class Wave(pygame.sprite.Sprite):
    def __init__(self):
        super(Wave, self).__init__()
        self.surf = pygame.Surface((50, 150))
        self.surf.fill((0, 0, 0))
        self.surf.fill((0,255,255), self.surf.get_rect().inflate(-15,-15))
        self.used = False

class Pad(pygame.sprite.Sprite):
    def __init__(self):
        super(Pad, self).__init__()
        self.surf = pygame.Surface((50, 10))
        self.surf.fill((255, 255, 0))
        self.rect = self.surf.get_rect()
        self.used = False

class BluePad(pygame.sprite.Sprite):
    def __init__(self):
        super(BluePad, self).__init__()
        self.surf = pygame.Surface((50, 10))
        self.surf.fill((0, 255, 255))
        self.rect = self.surf.get_rect()
        self.used = False

JUMP_HEIGHT = -23
MOVE_SPEED = 9
GRAVITY = 2
GRAVITYDIR = 1 #1 down -1 up
HasHeld = False

def update(self, pressed_keys):
    global GRAVITYDIR
    self.x += self.speedx
    self.y += self.speedy
    HELD = HasHeld
    if(gamemode == 1):
        if GRAVITYDIR == 1:
            self.grounded = self.y >= self.ground
        else:
            self.grounded = self.y <= self.ground
        if pressed_keys[K_SPACE]:
            if(self.grounded):
                self.speedy = JUMP_HEIGHT * GRAVITYDIR
                self.grounded = False
            else:
                if(HELD != True):
                    for orb in orbs:
                        if not orb.used:
                            if(orb.x < player.x + 100 and orb.x > player.x - 100):
                                orbcrash(player,orb)
                    for orb in blueorbs:
                        if not orb.used:
                            if(orb.x < player.x + 100 and orb.x > player.x - 100):
                                blueorbcrash(player,orb)
        if(not self.grounded):
            self.speedy += GRAVITY * GRAVITYDIR
        else:
            self.speedy = 0
            self.y = self.ground
    elif(gamemode == 2):
        if GRAVITYDIR == 1:
            self.grounded = self.y >= self.ground
        else:
            self.grounded = self.y <= self.ground
        if pressed_keys[K_SPACE]:
            self.speedy -= GRAVITY * GRAVITYDIR
            self.speedy = max(-10*GRAVITYDIR,self.speedy)
            self.grounded = False
            if not HELD:
                for orb in orbs:
                    if not orb.used:
                        if(orb.x < player.x + 100 and orb.x > player.x - 100):
                            orbcrash(player,orb)
                for orb in blueorbs:
                    if not orb.used:
                        if(orb.x < player.x + 100 and orb.x > player.x - 100):
                            blueorbcrash(player,orb)
        else:
            if(not self.grounded):
                self.speedy += GRAVITY * GRAVITYDIR
                self.speedy = min(10*GRAVITYDIR,self.speedy)
            else:
                self.speedy = 0
                self.y = self.ground
        if(GRAVITYDIR == 1):
            self.y = max(self.y, 50)
        else:
            self.y = min(self.y, 500)
    
    elif(gamemode == 3):
        if GRAVITYDIR == 1:
            self.grounded = self.y >= self.ground
        else:
            self.grounded = self.y <= self.ground
        if(self.grounded):
            if pressed_keys[K_SPACE]:
                if GRAVITYDIR == 1:
                    GRAVITYDIR *= -1
                    self.ground = 0
                else:
                    GRAVITYDIR *= -1
                    self.ground = 500
                self.grounded = False
        if(not self.grounded):
            
            self.speedy += GRAVITY * GRAVITYDIR
        else:
            self.speedy = 0
            self.y = self.ground
        if pressed_keys[K_SPACE]:
            if not HELD:
                for orb in orbs:
                    if not orb.used:
                        if(orb.x < player.x + 100 and orb.x > player.x - 100):
                            orbcrash(player,orb)
                for orb in blueorbs:
                    if not orb.used:
                        if(orb.x < player.x + 100 and orb.x > player.x - 100):
                            blueorbcrash(player,orb)

    elif(gamemode == 4):
        if GRAVITYDIR == 1:
            self.grounded = self.y >= self.ground
        else:
            self.grounded = self.y <= self.ground
        if pressed_keys[K_SPACE]:
            self.speedy = JUMP_HEIGHT/2 * GRAVITYDIR
            self.grounded = False
            if not HELD:
                for orb in orbs:
                    if not orb.used:
                        if(orb.x < player.x + 100 and orb.x > player.x - 100):
                            orbcrash(player,orb)
                for orb in blueorbs:
                    if not orb.used:
                        if(orb.x < player.x + 100 and orb.x > player.x - 100):
                            blueorbcrash(player,orb)

        if(not self.grounded):
            self.speedy += GRAVITY * GRAVITYDIR
        else:
            self.speedy = 0
            self.y = self.ground
        if(GRAVITYDIR == 1):
            self.y = max(self.y, 50)
        else:
            self.y = min(self.y, 500)
    elif(gamemode == 5):
        if GRAVITYDIR == 1:
            self.grounded = self.y >= self.ground
        else:
            self.grounded = self.y <= self.ground
        if pressed_keys[K_SPACE]:
            if not HELD:
                for orb in blueorbs:
                    if not orb.used:
                        if(orb.x < player.x + 100 and orb.x > player.x - 100):
                            blueorbcrash(player,orb)

            self.speedy = -12 * GRAVITYDIR
            self.grounded = False
        else:
            self.speedy = 12 * GRAVITYDIR
        if self.grounded:
            self.speedy = 0
            self.y = self.ground
        if(GRAVITYDIR == 1):
            self.y = max(self.y, 50)
        else:
            self.y = min(self.y, 500)
        HELD = pressed_keys[K_SPACE]
    return HELD
       


size = 50
def crash(player, block):
    global curr
    if GRAVITYDIR == 1:
        if player.y < (block.y):
            if ((player.x > block.x)
            and player.x < (block.x + size)
            or (((player.x + size) > block.x)
            and (player.x + size) < (block.x + size))):
                player.ground = block.y - size
                return True
            else:
                player.ground = 500
        elif((player.y + size) > (block.y) and (player.y < block.y + size)):
            
            if ((player.x > block.x)
            and player.x < (block.x + size)
            or (((player.x + size) > block.x)
            and (player.x + size) < (block.x + size))):
                print("block")
                curr = 1
    else:
        if player.y > (block.y):
            if ((player.x > block.x)
            and player.x < (block.x + size)
            or (((player.x + size) > block.x)
            and (player.x + size) < (block.x + size))):
                player.ground = block.y + size
                return True
            #else:
                #player.ground = 0
        elif((player.y + size) < (block.y) and (player.y > block.y + size)):
            
            if ((player.x > block.x)
            and player.x < (block.x + size)
            or (((player.x + size) > block.x)
            and (player.x + size) < (block.x + size))):
                print("block")
                curr = 1
    return False

def spikecrash(player,block):
    global curr
    if (player.y + size > (block.y + 30)) and (player.y < block.y - 30 + size):
        if ((player.x > block.x + 15)
           and player.x < (block.x + size - 15)
          or (((player.x + size) > block.x + 15)
           and (player.x + size) < (block.x + size - 15))):
            print("spike")
            curr = 1

def orbcrash(player,block):
    padding = 25 
    if player.y + size + padding > (block.y) and player.y < block.y + size + padding:
        if ((player.x > block.x)
           and player.x < (block.x +  + padding)
          or (((player.x + size + padding) > block.x)
           and (player.x + size + padding) < (block.x + size + padding))):
            player.speedy = JUMP_HEIGHT*1.1 * GRAVITYDIR
            block.used = True

def blueorbcrash(player,block):
    global GRAVITYDIR
    padding = 25
    if GRAVITYDIR == 1:
        if player.y + size + padding > (block.y) and player.y < block.y + size + padding:
            if ((player.x > block.x)
            and player.x < (block.x +  + padding)
            or (((player.x + size + padding) > block.x)
            and (player.x + size + padding) < (block.x + size + padding))):
                    GRAVITYDIR *= -1
                    player.grounded = False
                    player.ground = 0
                    block.used = True
    else:
        if player.y + size + padding > (block.y) and player.y < block.y + size + padding:
            if ((player.x > block.x)
            and player.x < (block.x +  + padding)
            or (((player.x + size + padding) > block.x)
            and (player.x + size + padding) < (block.x + size + padding))):
                GRAVITYDIR *= -1
                player.grounded = False
                player.ground = 500
                block.used = True


def padcrash(player,block):
    if ((player.y + size) > (block.y + 40) and (player.y < block.y + size)):
        if ((player.x > block.x)
           and player.x < (block.x + size)
          or (((player.x + size) > block.x)
           and (player.x + size) < (block.x + size))):
            player.speedy = JUMP_HEIGHT*1.4 * GRAVITYDIR
            block.used = True

def bluepadcrash(player,block):
    global GRAVITYDIR
    if GRAVITYDIR == 1:
        if ((player.y + size) > (block.y + 40) and (player.y < block.y + size)):
            if ((player.x > block.x)
            and player.x < (block.x + size)
            or (((player.x + size) > block.x)
            and (player.x + size) < (block.x + size))):
                #player.y -= 60 * GRAVITYDIR
                GRAVITYDIR *= -1
                block.used = True
                #player.speedy = 9 * GRAVITYDIR
                #player.grounded = False
    else:
        if ((player.y + size) > (block.y + 40) and (player.y < block.y + size)):
            if ((player.x > block.x)
            and player.x < (block.x + size)
            or (((player.x + size) > block.x)
            and (player.x + size) < (block.x + size))):
                #player.y -= 60 * GRAVITYDIR
                GRAVITYDIR *= -1
                player.grounded = False
                player.ground = 500
                block.used = True
                #player.speedy = 50 * GRAVITYDIR
                #player.grounded = False

def portalcrash(player,block):
    if player.y + size > (block.y - 50) and player.y < (block.y) + size + 56:
        if ((player.x > block.x       )
           and player.x < (block.x + size)
          or (((player.x + size) > block.x)
           and (player.x + size) < (block.x + size))):
            return True
    return False

class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		mousex,mousey = pygame.mouse.get_pos()
		pos = (mousex  * (SCREEN_HEIGHT/realscreen.get_height()) - ((realscreen.get_width() - ((realscreen.get_height()/SCREEN_HEIGHT) * SCREEN_WIDTH))/4),mousey * (SCREEN_HEIGHT/realscreen.get_height()))
                
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True
        
		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		surface.blit(self.image, (self.rect.x, self.rect.y))
        
		return action

def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

start_img = pygame.image.load("button_start.png").convert_alpha()
icons_img = pygame.image.load("button_icons.png").convert_alpha()
editor_img = pygame.image.load("button_editor.png").convert_alpha()
more_img = pygame.image.load("button_more.png").convert_alpha()
start_button = Button(SCREEN_WIDTH/2-start_img.get_width()/2, SCREEN_HEIGHT/2-start_img.get_height()/2, start_img, 1)
icon_button = Button(SCREEN_WIDTH/4-icons_img.get_width()/2, SCREEN_HEIGHT/2-icons_img.get_height()/2, icons_img, 1)
editor_button = Button((3 * SCREEN_WIDTH)/4-editor_img.get_width()/2, SCREEN_HEIGHT/2-editor_img.get_height()/2, editor_img, 1)
more_button = Button(SCREEN_WIDTH-more_img.get_width()-10,SCREEN_HEIGHT-more_img.get_height()-10,more_img,1)

player = Player()
player.x = 0
player.y = 475
running = True
blocks = []
spikes = []
orbs = []
blueorbs = []
pads = []
bluepads = []
ships = []
cubes = []
ufoz = []
ballz = []
wavez = []
endpoint = 0
def load(name):
    f = open(name, "r")
    global player
    global blocks
    global spikes
    global orbs
    global blueorbs
    global pads
    global bluepads
    global ships
    global cubes
    global ufoz
    global ballz
    global wavez
    global gamemode
    global endpoint
    global rot
    global GRAVITYDIR
    GRAVITYDIR = 1
    player.ground = 500
    player.x = 0
    player.y = 500
    gamemode = 1
    endpoint = 0
    player.speedy = 0
    rot = 0
    blocks = []
    spikes = []
    orbs = []
    blueorbs = []
    pads = []
    bluepads = []
    ships = []
    cubes = []
    ufoz = []
    ballz = []
    wavez = []
    for i, x in enumerate(f):
        a = str.split(x.rstrip())
        if(a[0] == "b"):
            blocks.append(Block())
            blocks[len(blocks) - 1].x = int(a[1])
            blocks[len(blocks) - 1].y = int(a[2])
        elif(a[0] == "s"):
            spikes.append(Spike()) 
            spikes[len(spikes) - 1].x = int(a[1])
            spikes[len(spikes) - 1].y = int(a[2])
            spikes[len(spikes) - 1].verts.append([int(a[1]) + 50, int(a[2]) + 50])
            spikes[len(spikes) - 1].verts.append([int(a[1])     , int(a[2]) + 50])
            spikes[len(spikes) - 1].verts.append([int(a[1]) + 25, int(a[2])])
        elif(a[0] == "y"):
            orbs.append(Orb())
            orbs[len(orbs) - 1].x = int(a[1])
            orbs[len(orbs) - 1].y = int(a[2])
        elif(a[0] == "p"):
            pads.append(Pad())
            pads[len(pads) - 1].x = int(a[1])
            pads[len(pads) - 1].y = int(a[2])
        elif(a[0] == "h"):
            ships.append(Ship())
            ships[len(ships) - 1].x = int(a[1])
            ships[len(ships) - 1].y = int(a[2]) - 50
        elif(a[0] == "c"):
            cubes.append(Cube())
            cubes[len(cubes) - 1].x = int(a[1])
            cubes[len(cubes) - 1].y = int(a[2]) - 50
        elif(a[0] == "o"):
            bluepads.append(BluePad())
            bluepads[len(bluepads) - 1].x = int(a[1])
            bluepads[len(bluepads) - 1].y = int(a[2])
        elif(a[0] == "t"):
            blueorbs.append(BlueOrb())
            blueorbs[len(blueorbs) - 1].x = int(a[1])
            blueorbs[len(blueorbs) - 1].y = int(a[2])
        elif(a[0] == "i"):
            ballz.append(Ball())
            ballz[len(ballz) - 1].x = int(a[1])
            ballz[len(ballz) - 1].y = int(a[2]) - 50
        elif(a[0] == "u"):
            ufoz.append(Ufo())
            ufoz[len(ufoz) - 1].x = int(a[1])
            ufoz[len(ufoz) - 1].y = int(a[2]) - 50
        elif(a[0] == "w"):
            wavez.append(Wave())
            wavez[len(wavez) - 1].x = int(a[1])
            wavez[len(wavez) - 1].y = int(a[2]) - 50
        if int(a[1]) > endpoint:
            endpoint = int(a[1])
    endpoint += 50
BACKGROUND_COLOR = (0,255,0)

gamemode = 5
curr = 1
rot = 0

levels = []
icons = []
shipz = []
balls = []
ufos = []
wave = []
font = pygame.font.SysFont("arialblack", 40)
def checkdir():
    global levels
    global icons
    global shipz
    global balls
    global ufos
    global waves
    dir_path = os.getcwd()

    raw = []

    for path in os.listdir(dir_path):
        if(os.path.isfile(os.path.join(dir_path, path))):
            raw.append(path)

    levels = []
    icons = []
    shipz = []
    balls = []
    ufos = []
    waves = []
    for check in raw:
        if '.txt' in check:
            levels.append(check)
        if '.png' in check:
            if 'icon_' in check:
                icons.append(check)
            if 'ball_' in check:
                balls.append(check)
            if 'ship_' in check:
                shipz.append(check)
            if 'ufo_' in check:
                ufos.append(check)
            if 'wave_' in check:
                waves.append(check)

checkdir()
print(balls)
curricon = 0
currship = 0
currball = 0
currufo = 0
currwave = 0

buttons = []
iconbuttons = []
shipbuttons = []
ballbuttons = []
ufobuttons = []
wavebuttons = []
waiting = False

menu = 0

menu_button = pygame.image.load("button_menuback.png").convert_alpha()


right_button = pygame.image.load("button_arrow_right.png").convert_alpha()
left_button = pygame.image.load("button_arrow_left.png").convert_alpha()

leftbutton = Button(10,SCREEN_HEIGHT/2-75,left_button,.5)
back_button = Button(10,SCREEN_HEIGHT-100,left_button,.5)
rightbutton = Button(700,SCREEN_HEIGHT/2-75,right_button,.5)

for level in levels:
    buttons.append(Button(SCREEN_WIDTH/2-175,SCREEN_HEIGHT/2-50,menu_button,1))

iconimages = []

for icon in icons:
    iconimages.append(pygame.image.load(icon).convert_alpha())

shipimages = []

for ship in shipz:
    shipimages.append(pygame.image.load(ship).convert_alpha())

ballimages = []

for ball in balls:
    ballimages.append(pygame.image.load(ball).convert_alpha())

ufoimages = []

for ufo in ufos:
    ufoimages.append(pygame.image.load(ufo).convert_alpha())

waveimages = []

for wave in waves:
    waveimages.append(pygame.image.load(wave).convert_alpha())

for i, icon in enumerate(icons):
    iconbuttons.append(Button((100 + 60 * (i % 10)),(SCREEN_HEIGHT/2-100 + math.floor(i / 10) * 60),iconimages[i],.5))

for i, icon in enumerate(balls):
    ballbuttons.append(Button((100 + 60 * (i % 10)),(SCREEN_HEIGHT/2-100 + math.floor(i / 10) * 60),ballimages[i],.5))

for i, icon in enumerate(shipz):
    shipbuttons.append(Button((100 + 60 * (i % 10)),(SCREEN_HEIGHT/2-100 + math.floor(i / 10) * 60),shipimages[i],.5))

for i, icon in enumerate(ufos):
    ufobuttons.append(Button((100 + 60 * (i % 10)),(SCREEN_HEIGHT/2-100 + math.floor(i / 10) * 60),ufoimages[i],.5))

for i, icon in enumerate(waves):
    wavebuttons.append(Button((100 + 60 * (i % 10)),(SCREEN_HEIGHT/2-100 + math.floor(i / 10) * 60),waveimages[i],.5))

currbutton = 0

pygame.display.set_caption("Vector Run")
pygame.display.set_icon(menu_button)


trail = []
frame = 0
while running:
    clock.tick(30)
    frame += 1
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if curr == 5:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        out = ""
                        print(editor.convert(out.join(newtext)))
                        newtext = []
                        checkdir()
                    elif event.key == pygame.K_BACKSPACE:
                        newtext = newtext[:-1]
                    else:
                        newtext.append(event.unicode)

    if(curr == 1):
        screen.fill((0,0,255))
        draw_text("VECTOR RUN", font, (255,175,0),SCREEN_WIDTH/2-140,100)
        if start_button.draw(screen):
            waiting = True
        if(waiting):
            if(not pygame.mouse.get_pressed(3)[0]):
                curr = 2
        if icon_button.draw(screen):
            curr = 4
        if editor_button.draw(screen):
            newtext = []
            curr = 5
        if more_button.draw(screen):
            webbrowser.open(r"https://bearpolice.itch.io")
    elif(curr == 2):
        currbutton = currbutton % len(buttons)
        waiting = False
        screen.fill((0,0,255))
        if leftbutton.draw(screen):
            currbutton = (currbutton - 1) % len(buttons)
        if rightbutton.draw(screen):
            currbutton = (currbutton + 1) % len(buttons)
        if buttons[currbutton].draw(screen):
            load(levels[currbutton])
            curr = 3
        if back_button.draw(screen):
            curr = 1
        draw_text(levels[currbutton].replace('.txt', ''),font,(255,255,255),SCREEN_WIDTH/2-140,SCREEN_HEIGHT/2-50)
        player.surf = iconimages[curricon]
    elif(curr == 3):
        
        if(player.x >= endpoint):
            curr = 1
        pressed_keys = pygame.key.get_pressed()

        screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(screen, (0,150,0), (0,550,SCREEN_WIDTH,SCREEN_HEIGHT))
        draw_text(str(round((player.x/endpoint)*100)) + "%",font,(0,0,0),3*SCREEN_WIDTH/4+50,30)
        pygame.draw.rect(screen,(255,255,255),(SCREEN_WIDTH/4,50,round((player.x/endpoint)*(SCREEN_WIDTH/2)),20))
        pygame.draw.rect(screen,(0,0,0),(SCREEN_WIDTH/4,50,(SCREEN_WIDTH/2),20), 4)
        HasHeld = update(player, pressed_keys)

        for block in blocks:
            if(block.x < player.x + SCREEN_WIDTH and block.x > player.x - 150):
                screen.blit(block.surf, (block.x - player.x + 100,block.y))
            #elif(block.x < player.x - 150):
                #blocks.remove(block)

        for block in blocks:
            if(block.x < player.x + 100 and block.x > player.x - 100):
                touched = crash(player,block)
                if(touched):
                    break 
                
        for spike in spikes:
            if(spike.x < player.x + 100 and spike.x > player.x - 100):
                spikecrash(player,spike)
            if(spike.x < player.x + SCREEN_WIDTH and spike.x > player.x - 150):
                verts = ((spike.verts[0][0] - player.x + 100, spike.verts[0][1]),(spike.verts[1][0] - player.x + 100, spike.verts[1][1]),(spike.verts[2][0] - player.x + 100, spike.verts[2][1]))
                pygame.draw.polygon(screen,  (0,0,0), verts)
                pygame.draw.polygon(screen,  (255,255,255), verts, 1)
                #pygame.draw.rect(screen, (255,255,255), (spike.x - player.x + 100 + 15,spike.y + 30 ,size - 30,size - 30 - 15))
            #elif(spike.x < player.x - 150):
                #spikes.remove(spike)

        for pad in pads:
            if not pad.used:
                if(pad.x < player.x + 100 and pad.x > player.x - 100):
                    padcrash(player,pad)
            if(pad.x < player.x + SCREEN_WIDTH and pad.x > player.x - 150): 
                screen.blit(pad.surf, (pad.x - player.x + 100,pad.y + 40))
                #elif(pad.x < player.x - 150):
                    #pads.remove(pad)

        for bluepad in bluepads:
            if not bluepad.used:
                if(bluepad.x < player.x + 100 and bluepad.x > player.x - 100):
                    bluepadcrash(player,bluepad)
            if(bluepad.x < player.x + SCREEN_WIDTH and bluepad.x > player.x - 150): 
                screen.blit(bluepad.surf, (bluepad.x - player.x + 100,bluepad.y + 40))
            #elif(pad.x < player.x - 150):
                #pads.remove(pad)

        for orb in orbs:
            if(orb.x < player.x + SCREEN_WIDTH and orb.x > player.x - 150):
                pygame.draw.circle(screen, (255,255,255), (orb.x - player.x + 100 + 25, orb.y + 25), 40)
                pygame.draw.circle(screen, (BACKGROUND_COLOR    ), (orb.x - player.x + 100 + 25, orb.y + 25), 35)
                pygame.draw.circle(screen, (255,255,0), (orb.x - player.x + 100 + 25, orb.y + 25), 25)
            #elif(orb.x < player.x - 150):
                #orbs.remove(orb)
        
        for orb in blueorbs:
            if(orb.x < player.x + SCREEN_WIDTH and orb.x > player.x - 150):
                pygame.draw.circle(screen, (255,255,255), (orb.x - player.x + 100+25, orb.y+25), 40)
                pygame.draw.circle(screen, (BACKGROUND_COLOR), (orb.x - player.x + 100+25, orb.y+25), 35)
                pygame.draw.circle(screen, ((0, 255, 255)), (orb.x - player.x + 100+25, orb.y+25), 25)
            #elif(orb.x < player.x - 150):
                #orbs.remove(orb)

        for ship in ships:
            if(ship.x < player.x + 100 and ship.x > player.x - 100):
                turned = portalcrash(player,ship)
                if(turned):
                    gamemode = 2
            if(ship.x < player.x + SCREEN_WIDTH and ship.x > player.x - 150):
                screen.blit(ship.surf, (ship.x - player.x + 100,ship.y))
            #elif(ship.x < player.x - 150):
                #ships.remove(ship)

        for cube in cubes:
            if(cube.x < player.x + 100 and cube.x > player.x - 100):
                turned = portalcrash(player,cube)
                if(turned):
                    gamemode = 1
            if(cube.x < player.x + SCREEN_WIDTH and cube.x > player.x - 150):
                screen.blit(cube.surf, (cube.x - player.x + 100,cube.y))
            #elif(cube.x < player.x - 150):
                #cubes.remove(cube)

        for cube in ballz:
            if(cube.x < player.x + 100 and cube.x > player.x - 100):
                turned = portalcrash(player,cube)
                if(turned):
                    gamemode = 3
            if(cube.x < player.x + SCREEN_WIDTH and cube.x > player.x - 150):
                screen.blit(cube.surf, (cube.x - player.x + 100,cube.y))
            #elif(cube.x < player.x - 150):
                #cubes.remove(cube)

        for cube in ufoz:
            if(cube.x < player.x + 100 and cube.x > player.x - 100):
                turned = portalcrash(player,cube)
                if(turned):
                    gamemode = 4
            if(cube.x < player.x + SCREEN_WIDTH and cube.x > player.x - 150):
                screen.blit(cube.surf, (cube.x - player.x + 100,cube.y))
            #elif(cube.x < player.x - 150):
                #cubes.remove(cube)

        for cube in wavez:
            if(cube.x < player.x + 100 and cube.x > player.x - 100):
                turned = portalcrash(player,cube)
                if(turned):
                    gamemode = 5
            if(cube.x < player.x + SCREEN_WIDTH and cube.x > player.x - 150):
                screen.blit(cube.surf, (cube.x - player.x + 100,cube.y))
            #elif(cube.x < player.x - 150):
                #cubes.remove(cube)
        
        if(gamemode == 2):
            pygame.draw.rect(screen, (0,150,0), (0,0,SCREEN_WIDTH,50))
            smaller = pygame.transform.scale_by(iconimages[curricon],.25)
            rot = player.speedy * -2
            smaller = pygame.transform.rotate(smaller, rot)
            if player.speedy == 0:
                screen.blit(smaller, (100+20,player.y+5))
            elif player.speedy > 0:
                screen.blit(smaller, (100+20+1*abs(player.speedy),player.y+1*abs(player.speedy)))
            else:
                screen.blit(smaller, (100+20,player.y+2*abs(player.speedy)))
            #pygame.draw.rect(screen, (200,100,0), (100,player.y+30,50,20))
            #ship = pygame.Surface((50,20))
            #ship.set_colorkey((0,0,0))
            #ship.fill((200,100,0))
            #newship = ship
            #newship.set_colorkey((0,0,0))
            #rect = newship.get_rect()
            
            newship = pygame.transform.rotate(shipimages[currship], rot)
            screen.blit(newship, (100-10,player.y-15))
        elif(gamemode == 3):
            newball = pygame.transform.scale_by(ballimages[currball],.5)
            if(player.grounded):
                #player.surf = pygame.transform.rotate(player.surf, 1)
                rot = (rot - 10 * GRAVITYDIR)%360
            newball = pygame.transform.rotate(newball, rot)
            screen.blit(newball, (100, player.y))
        elif(gamemode == 4):
            pygame.draw.rect(screen, (0,150,0), (0,0,SCREEN_WIDTH,50))
            smaller = pygame.transform.scale_by(iconimages[curricon],.25)
            screen.blit(smaller, (100+25,player.y+10))
            #smallufo = pygame.transform.scale_by(ufoimages[currufo],.5)
            screen.blit(ufoimages[currufo], (100-10,player.y-40))
        elif(gamemode == 5):
            if(player.speedy < 0): 
                rot = 45
                yoff = 20
            elif(player.speedy == 0): 
                rot = 0
                yoff = 0
            else: 
                rot = 315
                yoff = 10
            newwave = pygame.transform.rotate(waveimages[currwave],rot)
            newwave = pygame.transform.scale_by(newwave,.5)
            if(len(trail) == 12): trail = trail[1:]
            trail.append((player.y+35+yoff))
            for i,point in enumerate(trail):
                if(i != 0):
                    if(player.speedy < 0): 
                        newx = 130
                    elif(player.speedy == 0): 
                        newx = 130
                    else:
                        newx = 132
                    
                    pygame.draw.line(screen,(255,255,255),(newx-(len(trail)-i-1)*15,point),(newx-(len(trail)-i)*15,trail[i-1] ),10)
            screen.blit(newwave, (100,player.y+15))
        elif(gamemode == 1):
            
            if(not player.grounded):
                #player.surf = pygame.transform.rotate(player.surf, 1)
                rot = (rot - 4)%360
            else:
                #player.surf = pygame.transform.rotate(player.surf, 0)
                rot = round(rot/90)*90
            new_image = pygame.transform.rotate(player.surf, rot)
            new_image = pygame.transform.scale_by(new_image, .5)
            screen.blit(new_image, (100, player.y))
    elif curr == 4:
        screen.fill((0,0,255))
        if menu == 0:
            for i, button in enumerate(iconbuttons):
                if button.draw(screen):
                    curricon = i
            screen.blit(iconimages[curricon], (SCREEN_WIDTH/2-50, 50))
        elif menu == 1:
            for i, button in enumerate(shipbuttons):
                if button.draw(screen):
                    currship = i
            screen.blit(shipimages[currship], (SCREEN_WIDTH/2-50, 50))
        elif menu == 2:
            for i, button in enumerate(ballbuttons):
                if button.draw(screen):
                    currball = i
            screen.blit(ballimages[currball], (SCREEN_WIDTH/2-50, 50))
        elif menu == 3:
            for i, button in enumerate(ufobuttons):
                if button.draw(screen):
                    currufo = i
            screen.blit(ufoimages[currufo], (SCREEN_WIDTH/2-50, 50))
        elif menu == 4:
            for i, button in enumerate(wavebuttons):
                if button.draw(screen):
                    currwave = i
            screen.blit(waveimages[currwave], (SCREEN_WIDTH/2-50, 50))
        if leftbutton.draw(screen):
            menu = (menu - 1) % 5
        if rightbutton.draw(screen):
            menu = (menu + 1) % 5
        if back_button.draw(screen):
                curr = 1
    elif curr == 5:
        screen.fill((0,0,255))
        out = ""
        if back_button.draw(screen):
            curr = 1
        
        pygame.draw.rect(screen,(0,0,0),(SCREEN_WIDTH/2 - 150,SCREEN_HEIGHT/2+10, 400, 50))
        draw_text(out.join(newtext),font,(255,255,255),SCREEN_WIDTH/2-140,SCREEN_HEIGHT/2)
        draw_text("Input the name of your CSV",font,(255,255,255),SCREEN_WIDTH/4-150,SCREEN_HEIGHT/4)
        draw_text("you wish to convert to a level",font,(255,255,255),SCREEN_WIDTH/4-150,SCREEN_HEIGHT/4+50)
        draw_text("check terminal for result",font,(255,255,255),SCREEN_WIDTH/4-150,SCREEN_HEIGHT/4+100)
    
    #sc = pygame.Surface((3020,2000))
    #sc = pygame.transform.scale(screen, (SCREEN_WIDTH / realscreen.get_width(), SCREEN_HEIGHT /realscreen.get_height()))
    #realscreen = pygame.transform.scale_by(screen, (realscreen.get_width()/SCREEN_WIDTH, realscreen.get_height()/SCREEN_HEIGHT))
    #screen = pygame.display.set_mode([realscreen.get_width(),realscreen.get_height()])
    if(curr == 3):
        
        ratio = (realscreen.get_width()/realscreen.get_height())
        SCREEN_WIDTH = SCREEN_HEIGHT * ratio
        sc = pygame.transform.scale(screen,[SCREEN_WIDTH,SCREEN_HEIGHT])
        sc = pygame.transform.scale_by(screen,realscreen.get_height()/SCREEN_HEIGHT)
        
        
        realscreen.blit(sc, (0,0))
    else:
        SCREEN_WIDTH = 800
        sc = pygame.transform.scale_by(screen, realscreen.get_height()/SCREEN_HEIGHT)
        screen.fill((0,0,255))
        realscreen.blit(sc, (0+ (realscreen.get_width() - ((realscreen.get_height()/SCREEN_HEIGHT) * SCREEN_WIDTH))/2,0))
    #sc = pygame.transform.scale_by(screen, [realscreen.get_width()/SCREEN_WIDTH,realscreen.get_height()/SCREEN_HEIGHT])
    #sc = pygame.transform.scale_by(sc, ((realscreen.get_height()/(realscreen.get_width()/SCREEN_WIDTH)),1))
    #  
    
    #pygame.draw.rect(realscreen)
    pygame.display.flip()
    #clock.tick(1/30)


pygame.quit()