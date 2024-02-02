import pygame
import enum


# config parameters
main_res = (x, y) = (900, 500)
path_y_pos = 420
alien_min_x = 50
alien_max_x = x//2
alien_max_speed = 5
alien_speed_change = 0.2
backg_max_speed = 2
default_snail_speed = 3
default_jump_power = 23
display_freq = 60
# end config parameters

class GameState(enum.Enum):
    INIT = 0
    GAME = 1
    LOST = 2
    END  = 3







pygame.init()
pygame.font.init()

screen = pygame.display.set_mode(main_res)
pygame.display.set_caption('runner')
clock = pygame.time.Clock()

class Alien(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale_by(pygame.image.load('pic/alien.png').convert_alpha(), 1)
        self.rect = self.image.get_rect(bottomleft=(alien_min_x+50, path_y_pos - 300))  # x, y initial position

        self.last_alien_dir_r = True
        self.alien_speed = 0
        self.alien_y_pos = 0
        #self.alien_dir_r = True
        print("sprite init")


    def inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN: # jump button handling
                keys = pygame.key.get_pressed()
                if ((keys[pygame.K_SPACE] == True) and (self.rect.bottom == path_y_pos)):
                    self.alien_y_pos = jump_power

    def move(self):
        # alien movement:
        # x-axis:
        alien_dir_r = self.last_alien_dir_r

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] == True):
            alien_dir_r = False
            self.alien_speed -= alien_speed_change
            if self.alien_speed < (-alien_max_speed) : self.alien_speed = (-alien_max_speed)
        else:
            if(self.alien_speed < 0):
                self.alien_speed += alien_speed_change
                if self.alien_speed > 0: self.alien_speed = 0

        if (keys[pygame.K_RIGHT] == True):
            alien_dir_r = True
            self.alien_speed += alien_speed_change
            if self.alien_speed > alien_max_speed: self.alien_speed = alien_max_speed
        else:
            if(self.alien_speed > 0):
                self.alien_speed -= alien_speed_change
                if self.alien_speed < 0: self.alien_speed = 0

        self.rect.centerx += self.alien_speed
        if (self.rect.centerx > alien_max_x) :
            self.rect.centerx = alien_max_x
            #global_speed_factor = -alien_speed
        elif (self.rect.centerx < alien_min_x):
            self.rect.centerx = alien_min_x
            #global_speed_factor = -alien_speed
        else:
            #global_speed_factor = 0
            pass

        # y-axis:
        self.rect.y += self.alien_y_pos
        if self.rect.bottom >= path_y_pos:
            self.rect.bottom = path_y_pos
        else:
            self.alien_y_pos += 1

            #direction

        if (self.last_alien_dir_r != alien_dir_r):
            self.last_alien_dir_r = alien_dir_r
            self.image = pygame.transform.flip(self.image , True, False)
            #print('alien r:', alien_dir_r,  last_alien_dir_r)

    def update(self):
        self.inputs()
        self.move()




alien_sprite = pygame.sprite.GroupSingle(Alien())
alien_sprite.add(Alien())


backg_surf = pygame.transform.scale(pygame.image.load('pic/background1.jpg').convert_alpha(), main_res)
backg_rect = backg_surf.get_rect(topleft = (0,0))

backg_dark_surf = pygame.transform.scale(pygame.image.load('pic/background_dark.jpg').convert_alpha(), main_res)
backg_dark_rect = backg_dark_surf.get_rect(topleft = (0,0))

path_rect = pygame.Rect(0,path_y_pos,x,y)

alien_surf = pygame.transform.scale_by(pygame.image.load('pic/alien.png').convert_alpha(), 1)
alien_rect = alien_surf.get_rect(bottomleft = (alien_min_x, path_y_pos-300)) # x, y initial position

snail_surf = pygame.transform.scale_by(pygame.image.load('pic/snail.png').convert_alpha(), 0.9)
snail_rect = snail_surf.get_rect(bottomleft = (x, 420)) # x, y initial position


my_font = pygame.font.SysFont('Comic Sans MS', 30)
init_text_surf = my_font.render(' ', True, pygame.Color("cyan"))
init_text_rect = init_text_surf.get_rect(center = (x/2, y/2))

score = 0
alien_xpos = 0
dt = 0
jump_power = -default_jump_power
alien_speed = 0
backg_move = 0
backg_connection_point = 0
backg2_pos = 900
colision_detected = False
global_speed_factor = 0
alien_dir_r = True
last_alien_dir_r = alien_dir_r
snail_speed = 0
game_main_loop = True
game_state = GameState.INIT

def reset():
    global alien_surf
    global alien_rect
    global snail_rect
    global score
    global alien_xpos
    global jump_power
    global alien_speed
    global backg_move
    global backg_connection_point
    global backg2_pos
    global colision_detected
    global global_speed_factor
    global alien_dir_r
    global last_alien_dir_r
    global snail_speed
    global game_main_loop
    global game_state

    alien_surf = pygame.transform.scale_by(pygame.image.load('pic/alien.png').convert_alpha(), 1)
    alien_rect.bottomleft = (alien_min_x, path_y_pos - 300)
    snail_rect.bottomleft = (x, 420)
    score = 0
    alien_xpos = 0
    jump_power = -default_jump_power
    alien_speed = 0
    backg_move = 0
    backg_connection_point = 0
    backg2_pos = 900
    colision_detected = False
    global_speed_factor = 0
    alien_dir_r = True
    last_alien_dir_r = alien_dir_r
    snail_speed = 0
    game_main_loop = True
    game_state = GameState.INIT

def GameInit():
    global game_state
    global init_text_surf
    global init_text_rect
    # events handling:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state = GameState.END

        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_SPACE] == True:
                reset()
                game_state = GameState.GAME

    init_text_surf = my_font.render('Wciśnij spacje aby rozpocząć', True, pygame.Color("cyan"))
    init_text_rect = init_text_surf.get_rect(center=(x / 2, y / 2))

    screen.blit(backg_dark_surf, backg_dark_rect)
    screen.blit(init_text_surf, init_text_rect)

    pygame.display.flip()
    clock.tick(display_freq)

def GameRun():
    global backg_surf
    global backg_rect
    global path_rect
    global alien_surf
    global alien_rect
    global snail_surf
    global snail_rect

    global score
    global alien_xpos
    global dt
    global jump_power
    global alien_speed
    global backg_move
    global backg_connection_point
    global backg2_pos
    global colision_detected
    global global_speed_factor
    global alien_dir_r
    global last_alien_dir_r
    global snail_speed
    global game_main_loop
    global game_state

    jump_power = (-default_jump_power) + (score / 30)

    # events handling:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state = GameState.END

        if event.type == pygame.KEYDOWN: # jump button handling
            keys = pygame.key.get_pressed()
            if ((keys[pygame.K_SPACE] == True) and (alien_rect.bottom == path_y_pos)):
                alien_xpos = jump_power
    # events handling end

    # alien movement:
        # x-axis:
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_LEFT] == True):
        alien_dir_r = False
        alien_speed -= alien_speed_change
        if alien_speed < (-alien_max_speed) : alien_speed = (-alien_max_speed)
    else:
        if(alien_speed < 0):
            alien_speed += alien_speed_change
            if alien_speed > 0: alien_speed = 0

    if (keys[pygame.K_RIGHT] == True):
        alien_dir_r = True
        alien_speed += alien_speed_change
        if alien_speed > alien_max_speed: alien_speed = alien_max_speed
    else:
        if(alien_speed > 0):
            alien_speed -= alien_speed_change
            if alien_speed < 0: alien_speed = 0

    alien_rect.centerx += alien_speed
    if (alien_rect.centerx > alien_max_x) :
        alien_rect.centerx = alien_max_x
        global_speed_factor = -alien_speed
    elif (alien_rect.centerx < alien_min_x):
        alien_rect.centerx = alien_min_x
        global_speed_factor = -alien_speed
    else:
        global_speed_factor = 0

        # y-axis:
    alien_rect.y += alien_xpos
    if alien_rect.bottom >= path_y_pos:
        alien_rect.bottom = path_y_pos
    else:
        alien_xpos += 1

        #direction

    if (last_alien_dir_r != alien_dir_r):
        last_alien_dir_r = alien_dir_r
        alien_surf = pygame.transform.flip(alien_surf, True, False)
        print('alien r:', alien_dir_r,  last_alien_dir_r)

    # alien movement end


    # alien collision detection
    if alien_rect.colliderect(snail_rect):
        if (colision_detected == False):
            colision_detected = True
            game_state = GameState.LOST
    else:
        colision_detected = False
    # alien collision detection end

    # snail movement
    snail_speed = default_snail_speed + (score/10) # score snail speed factor
    snail_speed = (snail_speed - (global_speed_factor * 1)) # global speed factor influence on snail speed
    snail_rect.left -= snail_speed
    if (snail_rect.right < 0):
        score +=1
        print("score:{}, jump:{:.1f}, speed:{:.1f}".format(score, jump_power, snail_speed ))
        snail_rect.left = x
    # snail movement end

    # background movement
    backg_move = global_speed_factor
    backg_connection_point += backg_move
    if (backg_connection_point > 0): # background move right
        if backg_connection_point > x:
            backg_connection_point = 0

        #screen left
        backg_rect.right = backg_connection_point
        screen.blit(backg_surf, backg_rect)

        #screen right
        backg_rect.left = backg_connection_point
        screen.blit(backg_surf, backg_rect)

    elif (backg_connection_point < 0): # background move left
        if backg_connection_point < 0:
            backg_connection_point = x

        # screen left
        backg_rect.right = backg_connection_point
        screen.blit(backg_surf, backg_rect)

        # screen right
        backg_rect.left = backg_connection_point
        screen.blit(backg_surf, backg_rect)

    else: #no background movement
        # screen left
        backg_rect.right = backg_connection_point - 1
        screen.blit(backg_surf, backg_rect)

        # screen right
        backg_rect.left = backg_connection_point
        screen.blit(backg_surf, backg_rect)

    # background movement

    alien_sprite.update()
    alien_sprite.draw(screen)

    screen.blit(alien_surf, alien_rect)
    screen.blit(snail_surf, snail_rect)

    pygame.display.flip()

    dt = clock.tick(display_freq)




def GameLost():
    global game_state
    global init_text_surf
    global init_text_rect
    global score

    # events handling:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state = GameState.END

        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_SPACE] == True:
                reset()
                game_state = GameState.GAME

    screen.blit(backg_dark_surf, backg_dark_rect)

    init_text_surf = my_font.render(f'Przegrałeś! twoj wynik to {score}', True, pygame.Color("cyan"))
    init_text_rect = init_text_surf.get_rect(center=(x / 2, (y / 2)-25))
    screen.blit(init_text_surf, init_text_rect)

    init_text_surf = my_font.render('Wciśnij spacje żeby zagrać ponownie', True, pygame.Color("cyan"))
    init_text_rect = init_text_surf.get_rect(center=(x / 2, (y / 2)+25))
    screen.blit(init_text_surf, init_text_rect)

    pygame.display.flip()
    clock.tick(display_freq)


while(game_main_loop):
    if game_state == GameState.INIT:
        GameInit()
    elif game_state == GameState.GAME:
        GameRun()
    elif game_state == GameState.LOST:
        GameLost()
    elif game_state == GameState.END:
        game_main_loop = False
    else:
        #shall never enter here
        pass


pygame.quit()

