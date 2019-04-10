# Imports
import pygame
import random
import xbox360_controller

# Initialize game engine
pygame.init()


# Window
WIDTH = 1600
HEIGHT = 900
SIZE = (WIDTH, HEIGHT)
TITLE = 'SPACESHIP'
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)


# Timer
clock = pygame.time.Clock()
refresh_rate = 60


# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (100, 255, 100)

#level
level = 0

#Decide whether or not to use controller
use_controller = False

joystick_count = pygame.joystick.get_count()
if joystick_count > 0:
    use_controller = True

if use_controller:
    my_controller = xbox360_controller.Controller(0)

# Fonts
FONT_SM = pygame.font.Font('assets/fonts/spaceage.ttf', 24)
FONT_MD = pygame.font.Font('assets/fonts/spaceage.ttf', 32)
FONT_LG = pygame.font.Font('assets/fonts/spaceage.ttf', 64)
FONT_XL = pygame.font.Font('assets/fonts/spaceage.ttf', 96)


# Images
ship_img = pygame.image.load('assets/images/player.png').convert_alpha()
ship_left_img = pygame.image.load('assets/images/playerLeft.png').convert_alpha()
ship_right_img = pygame.image.load('assets/images/playerRight.png').convert_alpha()
ship_damaged_img = pygame.image.load('assets/images/playerDamaged.png').convert_alpha()
enemy_ship_img = pygame.image.load('assets/images/enemyShipChanged.png').convert_alpha()
enemy_ship_img_2 = pygame.image.load('assets/images/enemyShip2.png').convert_alpha()
enemy_ufo_img = pygame.image.load('assets/images/enemyUFO.png').convert_alpha()
green_laser_img = pygame.image.load('assets/images/laserGreen.png').convert_alpha()
red_laser_img = pygame.image.load('assets/images/laserRed.png').convert_alpha()
green_laser_shot_img = pygame.image.load('assets/images/laserGreenShot.png').convert_alpha()
red_laser_shot_img = pygame.image.load('assets/images/laserRedShot.png').convert_alpha()
background_img = pygame.image.load('assets/images/Background/starsallaround.png').convert_alpha()
repair_img = pygame.image.load('assets/images/powerupRepair.png').convert_alpha()
doubleshot_img = pygame.image.load('assets/images/powerupDoubleShot.png').convert_alpha()
invincible_img = pygame.image.load('assets/images/powerupInvincible.png').convert_alpha()
shield_img = pygame.image.load('assets/images/shield.png').convert_alpha()

# Sounds
EXPLOSION = pygame.mixer.Sound('assets/sounds/explosion.ogg')
SHOOT = pygame.mixer.Sound('assets/sounds/shoot.wav')
SHOT = pygame.mixer.Sound('assets/sounds/shot.ogg')
HIT = pygame.mixer.Sound('assets/sounds/hit.wav')
DRUMS = pygame.mixer.Sound('assets/sounds/drums_of_mordon.ogg')
pygame.mixer.music.load('assets/sounds/spaceMusic.ogg')
pygame.mixer.music.play(-1)


# Stages
START = 0
PLAYING = 1
PAUSED = 2
END = 3


# Game classes
class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.speed = 3
        self.shield = 5
        self.doubleshot = False
        self.invincible = 0

    def move_left(self):
        self.rect.x -= self.speed
    
    def move_right(self):
        self.rect.x += self.speed

    def move_up(self):
        self.rect.y -= self.speed

    def move_down(self):
        self.rect.y += self.speed

    def shoot(self):
        SHOOT.play()
        if self.doubleshot:
            laser1 = Laser(red_laser_img)
            laser1.rect.left = self.rect.left
            laser1.rect.centery = self.rect.centery
            laser2 = Laser(red_laser_img)
            laser2.rect.right = self.rect.right
            laser2.rect.centery = self.rect.centery
            lasers.add(laser1, laser2)
        else:
            laser = Laser(red_laser_img)
            laser.rect.centerx = self.rect.centerx
            laser.rect.centery = self.rect.top
            lasers.add(laser)
            

    def update(self):
        global stage
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        elif self.rect.top < 0:
            self.rect.top = 0
            
        hit_list = pygame.sprite.spritecollide(self, bombs, True, pygame.sprite.collide_mask)

        if self.invincible == 0:
            if len(hit_list) > 0:
                if self.shield > 0:
                    self.shield -= 1
                    HIT.play()
                elif self.shield == 0:
                    self.kill()
                    EXPLOSION.play()
                    stage = END
                    self.doubleshot = False

        if self.shield == 0:
            self.image = ship_damaged_img


        powerup_hit_list = pygame.sprite.spritecollide(self, powerups, True, pygame.sprite.collide_mask)

        if len(powerup_hit_list) > 0:
            for powerup in powerup_hit_list:
                if powerup.type == 1:
                    self.shield = 5
                elif powerup.type == 2:
                    self.doubleshot = True
                elif powerup.type == 3:
                    self.invincible = 300
                    shield = Shield()
                    shields.add(shield)

        if self.invincible > 0:
            self.invincible -= 1
        
class Laser(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.speed = 5

    def update(self):
        self.rect.y -= self.speed
        
        if self.rect.bottom < 0:
            self.kill()

class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.shield = random.randint(1, 5)
        self.value = self.shield
        self.rect.x = x
        self.rect.y = y

    def drop_bomb(self):
        SHOOT.play()

        bomb = Bomb(green_laser_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)
        
    def update(self):
        hit_list = pygame.sprite.spritecollide(self, lasers, True, pygame.sprite.collide_mask)

        if len(hit_list) > 0:
            if self.shield > 0:
                self.shield -= 1
                HIT.play()
                player.score += 1
            elif self.shield == 0:
                self.kill()
                EXPLOSION.play()
                player.score += self.value
                fleet.speed += 1

class Bomb(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        
        if self.rect.top > HEIGHT:
            self.kill()

class Fleet():
    def __init__(self, mobs):
        self.mobs = mobs
        self.speed = 5
        self.moving_right = True
        self.drop_speed = 20
        self.bomb_rate = 60

    def move(self):
        hits_edge = False
        for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed

                if m.rect.right >= WIDTH:
                    hits_edge = True
            else:
                m.rect.x -=self.speed
                
                if m.rect.left <= 0:
                    hits_edge = True

        if hits_edge:
            self.reverse()
            #self.move_down()
            
    def reverse(self):
        self.moving_right = not self.moving_right

    def move_down(self):
        for m in mobs:
            m.rect.y += self.drop_speed

    def choose_bomber(self):
        rand = random.randrange(self.bomb_rate)
        mob_list = mobs.sprites()

        if len(mob_list) > 0 and rand == 0:
            bomber = random.choice(mob_list)
            bomber.drop_bomb()

    def update(self):
        self.move()
        self.choose_bomber()

class UFO(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(-2000, -1000)
        self.rect.y = 400
        self.speed = 5

    def move(self):
        self.rect.x += self.speed

    def update(self):
        self.move()
          
        hit_list = pygame.sprite.spritecollide(self, lasers, True, pygame.sprite.collide_mask)

        if len(hit_list) > 0:
            player.score += 20
            self.kill()
            EXPLOSION.play()

class Powerup(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.type = 3
        if self.type == 1:
            self.image = repair_img
        elif self.type == 2:
            self.image = doubleshot_img
        elif self.type == 3:
            self.image = invincible_img
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.speed = 3


    def move(self):
        self.rect.y += self.speed

    def update(self):
        self.move()
        if self.rect.y > HEIGHT:
            self.kill()

class Shield(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = shield_img
        self.rect = self.image.get_rect()
        self.rect.centerx = ship.rect.centerx
        self.rect.centery = ship.rect.top
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.centerx = ship.rect.centerx
        self.rect.centery = ship.rect.top

        hit_list = pygame.sprite.spritecollide(self, bombs, False, pygame.sprite.collide_mask)
        for hit in hit_list:
            hit.kill()

        if ship.invincible == 0:
            self.kill
          
# Game helper functions
def show_title_screen():
    text = FONT_XL.render('SPACHESHIP!', 1, WHITE)
    textRect = text.get_rect()
    textRect.centerx = WIDTH/2
    textRect.centery = HEIGHT/2
    
    screen.blit(text, textRect)

def show_end():
    ship_list = player.sprites()

    text = FONT_XL.render('YOU DIED!', 1, WHITE)

    textRect = text.get_rect()
    textRect.centerx = WIDTH/2
    textRect.centery = HEIGHT/2

    screen.blit(text, textRect)

    text2 = FONT_XL.render('YOUR SCORE WAS: ' + str(player.score), 1, WHITE)

    text2Rect = text2.get_rect()
    text2Rect.centerx = WIDTH/2
    text2Rect.top = textRect.bottom + 20

    screen.blit(text2, text2Rect)
    
def display_stats(ship):
    global level
    score_text = FONT_LG.render("Score: " + str(player.score), 1, WHITE)
    screen.blit(score_text, [10, 10])

    level_text = FONT_LG.render("Level: " + str(level), 1, WHITE)
    level_text_rect = level_text.get_rect()
    level_text_rect.right = WIDTH - 10
    level_text_rect.top = 10
    screen.blit(level_text, level_text_rect)
    
    shield = "Shield: " + str(ship.shield * 20) + "%"
    shield_text = FONT_MD.render(shield, 1, WHITE)
    shield_text_height = shield_text.get_height()
    screen.blit(shield_text, [10, 850 - (shield_text_height + 10)])
    pygame.draw.rect(screen, RED, [0, 850, 200, 50])
    pygame.draw.rect(screen, GREEN, [0, 850, ship.shield * 40, 50])
    
def setup():
    global stage, done, attack_delay, level
    global player, ship, lasers, bombs, mobs, fleet, ufos, powerups, shields

    level += 1
    
    #Ship
    ''' Make game objects '''
    ship = Ship(384, 525, ship_img)
    ship.rect.centerx = WIDTH/2
    ship.rect.bottom = HEIGHT - 45
    
    ''' Make sprite groups '''
    player = pygame.sprite.GroupSingle()
    player.add(ship)

    #Lasers and Bombs
    lasers = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    
    #Row 1
    mob1 = Mob(100, 100, enemy_ship_img)
    mob2 = Mob(300, 100, enemy_ship_img)
    mob3 = Mob(500, 100, enemy_ship_img)
    mob4 = Mob(700, 100, enemy_ship_img)
    mob5 = Mob(900, 100, enemy_ship_img)
    mob6 = Mob(1100, 100, enemy_ship_img)
    mob7 = Mob(1300, 100, enemy_ship_img)
    mob8 = Mob(1500, 100, enemy_ship_img)

    #Row 2
    mob9 = Mob(100, 200, enemy_ship_img_2)
    mob10 = Mob(300, 200, enemy_ship_img_2)
    mob11 = Mob(500, 200, enemy_ship_img_2)
    mob12 = Mob(700, 200, enemy_ship_img_2)
    mob13 = Mob(900, 200, enemy_ship_img_2)
    mob14 = Mob(1100, 200, enemy_ship_img_2)
    mob15 = Mob(1300, 200, enemy_ship_img_2)
    mob16 = Mob(1500, 200, enemy_ship_img_2)

    mobs = pygame.sprite.Group()
    mobs.add(mob1,mob2,mob3,mob4,mob5,mob6,mob7,mob8,mob9,mob10,mob11,mob12,mob13,mob14,mob15,mob16)

    #Powerups
    powerups = pygame.sprite.Group()
    
    #Fleet
    fleet = Fleet(mobs)

    #UFO
    ufo = UFO(enemy_ufo_img)

    ufos = pygame.sprite.GroupSingle()

    ufos.add(ufo)

    #Shield
    shields = pygame.sprite.Group()

    ''' set stage '''
    stage = START
    done = False
    
# Game loop
setup()
player.score = 0

while not done:
    # Input handling (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
        if not use_controller:        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if stage == START:
                        stage = PLAYING
                    elif stage == PLAYING:
                        ship.shoot()
                    elif stage == END:
                        stage = START
                        setup()
                elif event.key == pygame.K_ESCAPE:
                    if stage == PLAYING:
                        stage = PAUSED
                    

        elif use_controller:            
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == xbox360_controller.A:
                    if stage == PLAYING:
                        ship.shoot()
                if event.button == xbox360_controller.START:
                    if stage == START:
                        stage = PLAYING
                    elif stage == PLAYING:
                        stage == PAUSED
                    elif stage == END:
                        stage = START
                        setup()

                    
    if stage == PLAYING:
        if use_controller:
            left_x, left_y = my_controller.get_left_stick()
            if left_x >= .5:
                ship.move_right()
                ship.image = ship_right_img
            elif left_x <= -.5:
                ship.move_left()
                ship.image = ship_left_img
            else:
                ship.image = ship_img

            if left_y >= .5:
                ship.move_down()

            elif left_y <= -.5:
                ship.move_up()

        elif not use_controller:
            pressed = pygame.key.get_pressed()

            w = pressed[pygame.K_w]
            s = pressed[pygame.K_s]
            a = pressed[pygame.K_a]
            d = pressed[pygame.K_d]

            if w:
                ship.move_up()
            elif s:
                ship.move_down()
            if d:
                ship.move_right()
            elif a:
                ship.move_left()

        powerup_spawn = random.randint(1, 1000)
        if powerup_spawn == 512:
            powerup = Powerup()
            powerup.rect.x = random.randrange(1, 1400)
            powerup.rect.bottom = 0
            powerups.add(powerup)
    
        # Game logic (Check for collisions, update points, etc.)
        player.update()
        lasers.update()
        bombs.update()
        powerups.update()
        fleet.update()
        mobs.update()
        ufos.update()
        shields.update()
            
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    screen.blit(background_img, [0,0])
    lasers.draw(screen)
    bombs.draw(screen)
    powerups.draw(screen)
    player.draw(screen)
    mobs.draw(screen)
    ufos.draw(screen)
    shields.draw(screen)
    
    if stage == START:
        show_title_screen()
        
    if stage == PLAYING:
        display_stats(ship)

    if stage == END:
        show_end()

        
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
