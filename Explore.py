import pygame
import os
import math
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

class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super(Ship, self).__init__()
        self.surf = pygame.Surface((50, 150))
        self.surf.fill((0, 0, 0))
        self.surf.fill((255,0,255), self.surf.get_rect().inflate(-15,-15))

class Cube(pygame.sprite.Sprite):
    def __init__(self):
        super(Cube, self).__init__()
        self.surf = pygame.Surface((50, 150))
        self.surf.fill((0, 0, 0))
        self.surf.fill((0,255,0), self.surf.get_rect().inflate(-15,-15))

class Pad(pygame.sprite.Sprite):
    def __init__(self):
        super(Pad, self).__init__()
        self.surf = pygame.Surface((50, 10))
        self.surf.fill((255, 255, 0))
        self.rect = self.surf.get_rect()

JUMP_HEIGHT = -23
MOVE_SPEED = 9
GRAVITY = 2
HasHeld = False

def update(self, pressed_keys):
    self.x += self.speedx
    self.y += self.speedy
    HELD = HasHeld
    if(gamemode == 1):
        self.grounded = self.y >= self.ground
        if pressed_keys[K_SPACE]:
            if(self.grounded):
                self.speedy = JUMP_HEIGHT
                self.grounded = False
            else:
                if(HELD != True):
                    for orb in orbs:
                        if(orb.x < player.x + 100 and orb.x > player.x - 100):
                            orbcrash(player,orb)
            HELD = True
        else:
            HELD = False
        if(not self.grounded):
            self.speedy += GRAVITY
        else:
            self.speedy = 0
            self.y = self.ground
    elif(gamemode == 2):
        self.grounded = self.y >= self.ground
        if pressed_keys[K_SPACE]:
            self.speedy -= GRAVITY
            self.speedy = max(-10,self.speedy)
            self.grounded = False
        else:
            if(not self.grounded):
                self.speedy += GRAVITY
                self.speedy = min(10,self.speedy)
            else:
                self.speedy = 0
                self.y = self.ground
        self.y = max(self.y, 50)
    return HELD
       


size = 50
def crash(player, block):
    global curr
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
    padding = 50 
    if player.y + size + padding > (block.y) and player.y < block.y + size + padding:
        if ((player.x > block.x)
           and player.x < (block.x +  + padding)
          or (((player.x + size + padding) > block.x)
           and (player.x + size + padding) < (block.x + size + padding))):
            player.speedy = JUMP_HEIGHT

def padcrash(player,block):
    if player.y + size >= (block.y + 40):
        if ((player.x > block.x)
           and player.x < (block.x + size)
          or (((player.x + size) > block.x)
           and (player.x + size) < (block.x + size))):
            player.speedy = JUMP_HEIGHT*1.4

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
		
		pos = pygame.mouse.get_pos()

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
start_button = Button(SCREEN_WIDTH/2-start_img.get_width()/2, SCREEN_HEIGHT/2-start_img.get_height()/2, start_img, 1)
icon_button = Button(SCREEN_WIDTH/4-icons_img.get_width()/2, SCREEN_HEIGHT/2-icons_img.get_height()/2, icons_img, 1)

player = Player()
player.x = 0
player.y = 500
running = True
blocks = []
spikes = []
orbs = []
pads = []
ships = []
cubes = []
endpoint = 0
def load(name):
    f = open(name, "r")
    global player
    global blocks
    global spikes
    global orbs
    global pads
    global ships
    global cubes
    global endpoint
    player.ground = 500
    player.x = 0
    player.y = 500
    endpoint = 0
    player.speedy = 0
    blocks = []
    spikes = []
    orbs = []
    pads = []
    ships = []
    cubes = []
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
        if int(a[1]) > endpoint:
            endpoint = int(a[1])
    endpoint += 50
BACKGROUND_COLOR = (0,255,0)

gamemode = 1
curr = 1
rot = 0

font = pygame.font.SysFont("arialblack", 40)

dir_path = os.getcwd()

raw = []

for path in os.listdir(dir_path):
    if(os.path.isfile(os.path.join(dir_path, path))):
        raw.append(path)
print(raw)

levels = []
icons = []
for check in raw:
    if '.txt' in check:
        levels.append(check)
    if '.png' in check:
        if 'icon_' in check:
            icons.append(check)

curricon = 0

buttons = []
iconbuttons = []
waiting = False
print(levels)
print(icons)
menu_button = pygame.image.load("button_menuback.png").convert_alpha()

right_button = pygame.image.load("button_arrow_right.png").convert_alpha()
left_button = pygame.image.load("button_arrow_left.png").convert_alpha()

leftbutton = Button(50,SCREEN_HEIGHT/2-75,left_button,1)
back_button = Button(10,SCREEN_HEIGHT-100,left_button,.5)
rightbutton = Button(600,SCREEN_HEIGHT/2-75,right_button,1)
for level in levels:
    buttons.append(Button(SCREEN_WIDTH/2-175,SCREEN_HEIGHT/2,menu_button,1))

iconimages = []

for icon in icons:
    iconimages.append(pygame.image.load(icon).convert_alpha())

for i, icon in enumerate(icons):
    iconbuttons.append(Button((100 + 60 * (i % 10)),(SCREEN_HEIGHT/2-100 + math.floor(i / 10) * 60),iconimages[i],.5))

currbutton = 0

pygame.display.set_caption("Vector Run")
pygame.display.set_icon(menu_button)

while running:
    clock.tick(30)
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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
    elif(curr == 2):
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
        draw_text(levels[currbutton].replace('.txt', ''),font,(255,255,255),SCREEN_WIDTH/2-140,SCREEN_HEIGHT/2)
        player.surf = iconimages[curricon]
    elif(curr == 3):
        
        if(player.x >= endpoint):
            curr = 1
        pressed_keys = pygame.key.get_pressed()

        screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(screen, (0,150,0), (0,550,SCREEN_WIDTH,SCREEN_HEIGHT))
        draw_text(str(round((player.x/endpoint)*100)) + "%",font,(0,0,0),SCREEN_WIDTH/2+225,30)
        pygame.draw.rect(screen,(255,255,255),(SCREEN_WIDTH/4,50,round((player.x/endpoint)*(SCREEN_WIDTH/2)),20))
        pygame.draw.rect(screen,(0,0,0),(SCREEN_WIDTH/4,50,(SCREEN_WIDTH/2),20), 4)
        HasHeld = update(player, pressed_keys)

        for block in blocks:
            if(block.x < player.x + 700 and block.x > player.x - 150):
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
            if(spike.x < player.x + 700 and spike.x > player.x - 150):
                verts = ((spike.verts[0][0] - player.x + 100, spike.verts[0][1]),(spike.verts[1][0] - player.x + 100, spike.verts[1][1]),(spike.verts[2][0] - player.x + 100, spike.verts[2][1]))
                pygame.draw.polygon(screen,  (0,0,0), verts)
                pygame.draw.polygon(screen,  (255,255,255), verts, 1)
                #pygame.draw.rect(screen, (255,255,255), (spike.x - player.x + 100 + 15,spike.y + 30 ,size - 30,size - 30 - 15))
            #elif(spike.x < player.x - 150):
                #spikes.remove(spike)

        for pad in pads:
            if(pad.x < player.x + 100 and pad.x > player.x - 100):
                padcrash(player,pad)
            if(pad.x < player.x + 700 and pad.x > player.x - 150): 
                screen.blit(pad.surf, (pad.x - player.x + 100,pad.y + 40))
            #elif(pad.x < player.x - 150):
                #pads.remove(pad)

        for orb in orbs:
            if(orb.x < player.x + 700 and orb.x > player.x - 150):
                pygame.draw.circle(screen, (255,255,255), (orb.x - player.x + 100, orb.y), 40)
                pygame.draw.circle(screen, (BACKGROUND_COLOR    ), (orb.x - player.x + 100, orb.y), 35)
                pygame.draw.circle(screen, (255,255,0), (orb.x - player.x + 100, orb.y), 25)
            #elif(orb.x < player.x - 150):
                #orbs.remove(orb)

        for ship in ships:
            if(ship.x < player.x + 100 and ship.x > player.x - 100):
                turned = portalcrash(player,ship)
                if(turned):
                    gamemode = 2
            if(ship.x < player.x + 700 and ship.x > player.x - 150):
                screen.blit(ship.surf, (ship.x - player.x + 100,ship.y))
            #elif(ship.x < player.x - 150):
                #ships.remove(ship)

        for cube in cubes:
            if(cube.x < player.x + 100 and cube.x > player.x - 100):
                turned = portalcrash(player,cube)
                if(turned):
                    gamemode = 1
            if(cube.x < player.x + 700 and cube.x > player.x - 150):
                screen.blit(cube.surf, (cube.x - player.x + 100,cube.y))
            #elif(cube.x < player.x - 150):
                #cubes.remove(cube)
        
        if(gamemode == 2):
            pygame.draw.rect(screen, (0,150,0), (0,0,SCREEN_WIDTH,50))
            smaller = pygame.transform.scale_by(iconimages[curricon],.25)
            screen.blit(smaller, (100+10,player.y+10+abs(player.speedy)))
            #pygame.draw.rect(screen, (200,100,0), (100,player.y+30,50,20))
            ship = pygame.Surface((50,20))
            ship.set_colorkey((0,0,0))
            ship.fill((200,100,0))
            newship = ship
            newship.set_colorkey((0,0,0))
            rect = newship.get_rect()
            rot = player.speedy * -3
            newnewship = pygame.transform.rotate(newship, rot)
            screen.blit(newnewship, (100,player.y+30))
            
        else:
            
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
        for i, button in enumerate(iconbuttons):
            if button.draw(screen):
                curricon = i
        if back_button.draw(screen):
            curr = 1
        screen.blit(iconimages[curricon], (SCREEN_WIDTH/2-50, 50))
    pygame.display.update()
    #clock.tick(1/30)


pygame.quit()