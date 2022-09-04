import pygame
import os
import random
import math

pygame.font.init()
WIDTH, HEIGHT = 900, 700

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACE SHOOTER GAME")

# loading the space ship model
SPACE_SHIP = [pygame.transform.scale(pygame.image.load(os.path.join('IMG', f"{i}B.png")), 
                (50, 50)) for i in range(1, 14)]
# for i in range(1, 14): SPACE_SHIP.append(pygame.transform.scale(pygame.image.load(os.path.join('IMG', f"{i}.png")), 
#                 (50, 50)))
# SPACE_SHIP = [pygame.image.load(os.path.join('IMG', f"{i}B.png")) for i in range(1, 11)]
# BG = pygame.transform.scale(pygame.image.load(os.path.join('IMG', 'Stars.png')), (WIDTH, HEIGHT+300))
BG = pygame.transform.scale(pygame.image.load(os.path.join('IMG', 'Stars.png')), (WIDTH, HEIGHT))
LASER_IMG = pygame.transform.scale(pygame.image.load(os.path.join('IMG', 'pixel_laser_red.png')), (5, 15))

SPACE_SHIP_ORIGINAL = [pygame.image.load(os.path.join('IMG', f"{i}B.png")) for i in range(1, 14)]

ship_index = 0

main_font = pygame.font.SysFont("comicsans", 50)
label_font = pygame.font.SysFont("comicscans", 30)

class Ship:
    def __init__(self, x, y, health):
        self.x = x
        self.y = y
        self.health = health
        self.img = None
        self.laser_img = None
        self.lasers = []
    
    def draw(self, window):
        for laser in self.lasers:
            laser.draw(window)
        window.blit(self.img, (self.x, self.y))

    def move_laser(self, vel, obj):
        for laser in self.lasers:
            laser.move(vel)

            if laser.offScreen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def shoot(self):
        laser = Laser(self.x + 50 / 2, self.y, self.laser_img)
        self.lasers.append(laser)

    def offScreen(self, height):
         return  not (self.y < height)

    def get_width(self):
        return self.img.get_width()
        
    def get_height(self):
        return self.img.get_height()

class Player(Ship):
    def __init__(self, x, y, ship_index, health=100):
        super().__init__(x, y, health)
        self.img = SPACE_SHIP[ship_index]
        self.laser_img = LASER_IMG

        self.max_health = self.health
        self.mask = pygame.mask.from_surface(self.img)

        self.damage = 50
    
    def move_laser(self, vel, objs):
        for laser in self.lasers:
            laser.move(-vel)

            if laser.offScreen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        obj.health -= self.damage
                        self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        if self.img in SPACE_SHIP:
            self.healthBar(window)

    def healthBar(self, window):
        pygame.draw.rect(window, (255, 255, 255), (self.x, self.y + self.get_height() + 10, self.get_width(), 10))
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.get_height() + 10, self.get_width() * (self.health/self.max_health), 10))
                       

class Enemy(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.img = random.choice(SPACE_SHIP)
        self.mask = pygame.mask.from_surface(self.img)

        self.laser_img = LASER_IMG
    
    def move(self, vel):
        self.y += vel
    
    def shoot(self):
        laser = Laser(self.x + 50 / 2, self.y + 50, self.laser_img)
        self.lasers.append(laser)


class Laser():
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    
    def move(self, vel):
        self.y += vel
    
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def offScreen(self, height):
         return  not (self.y > 0 and self.y < height)

    def collision(self, obj):
        return collide(self, obj)

def changeShip(_player, increment):
    shipIndex = SPACE_SHIP.index(_player.img)
    if shipIndex + increment >= len(SPACE_SHIP):
        shipIndex = 0
    _player.img = SPACE_SHIP[shipIndex + increment]

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj1.y - obj2.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def main():
    FPS = 60
    PLAYER_VEL = 5
    ENEMY_VEL = 1

    LASER_VEL = 5

    enemies = []
    wave_length = 5

    level = 0
    lives = 3
    
    player = Player(400, 400, ship_index)
    
    lost = False


    def reDrawWindow():
        leves_label = label_font.render(f"LIVES: {lives}", 1, (255, 255, 255))
        level_lebel = label_font.render(f"LEVEL: {level}", 1, (255, 255, 255))
        WIN.blit(BG, (0, 0))
        
        player.draw(WIN)
        for enemy in enemies:
            enemy.draw(WIN)

        WIN.blit(leves_label, (WIDTH - leves_label.get_width() - 10, leves_label.get_height() + 10))
        WIN.blit(level_lebel, (10, leves_label.get_height() + 10))

        # lost menu
        if lost:
            lost_label = main_font.render("YOU LOST", 1, (255, 19, 50))
            play_again_label = main_font.render("PRESS SPACE TO PLAY AGAIN", 1, (255, 255, 255))
           
            inLostMenu = True
            while inLostMenu:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.display.quit()
                        exit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            main_menu()
                WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width() / 2, HEIGHT / 2 - lost_label.get_height() / 2))
                WIN.blit(play_again_label, (WIDTH / 2 - play_again_label.get_width() / 2, HEIGHT - play_again_label.get_height() - 10))

                pygame.display.update()

        pygame.display.update()
 
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        reDrawWindow()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                # if event.key == pygame.K_q:
                #     changeShip(player, 1)
                # if event.key == pygame.K_e:
                #     changeShip(player, -1)

                if event.key == pygame.K_SPACE:
                    player.shoot()
                
        
        keys = pygame.key.get_pressed()
        # Player movement
        if keys[pygame.K_w] and not (player.y - PLAYER_VEL <= 0):
            if keys[pygame.K_d]:
                player.x += math.cos(45) * PLAYER_VEL
                player.y -= math.sin(45) * PLAYER_VEL
            elif keys[pygame.K_a]:
                player.x -= math.cos(45) * PLAYER_VEL
                player.y -= math.sin(45) * PLAYER_VEL
            else:
                player.y -= PLAYER_VEL
        elif keys[pygame.K_s] and not (player.y + PLAYER_VEL + player.get_height() >= HEIGHT):
            if keys[pygame.K_d]:
                player.x += math.cos(45) * PLAYER_VEL
                player.y += math.sin(45) * PLAYER_VEL
            elif keys[pygame.K_a]:
                player.x -= math.cos(45) * PLAYER_VEL
                player.y += math.sin(45) * PLAYER_VEL
            else:
                player.y += PLAYER_VEL
        elif keys[pygame.K_a] and not (player.x - PLAYER_VEL <= 0):
            player.x -= PLAYER_VEL
        elif keys[pygame.K_d] and not (player.x + PLAYER_VEL + player.get_width() >= WIDTH):
            player.x += PLAYER_VEL
        
        # Enemies spawn
        if len(enemies) == 0:
            for _ in range(wave_length):
                enemy = Enemy(random.randrange(100, WIDTH - 100), random.randrange(-1500, -100))
                enemies.append(enemy) 
            
            level += 1
            wave_length += 5
            
        for enemy in enemies:
            enemy.move(ENEMY_VEL)
            enemy.move_laser(LASER_VEL, player)

            shoot = random.randint(0, 2*180) == 1

            if shoot:
                enemy.shoot()

            if enemy.health <= 0:
                enemies.remove(enemy)

            if enemy.offScreen(HEIGHT):
                enemies.remove(enemy)
                lives -= 1

            if lost:
                enemies.remove(enemy)

        player.move_laser(LASER_VEL, enemies)

        if player.health <= 0 or lives <= 0:
            lost = True


def main_menu():
    player = Player(100, 100, ship_index)
    player.img = SPACE_SHIP_ORIGINAL[ship_index]

    def chgShip(_player, increment):
        global ship_index
        if ship_index + increment >= len(SPACE_SHIP_ORIGINAL):
            ship_index = -1
        if ship_index + increment < 0:
            ship_index = len(SPACE_SHIP_ORIGINAL)
        ship_index += increment
        _player.img = SPACE_SHIP_ORIGINAL[ship_index]
        # print(ship_index)

    
    def reDraw(window):
        choose_ship_label = main_font.render("PRESS Q AND E TO CHOOSE SHIP", 1, (255, 255, 255))

        play_label = main_font.render("PRESS SPACE TO PLAY", 1, (255, 255, 255))

        window.blit(BG, (0, 0))
        player.draw(window)

        window.blit(choose_ship_label, (WIDTH / 2 - choose_ship_label.get_width() / 2, 10))
        window.blit(play_label, (WIDTH / 2 - play_label.get_width() / 2, HEIGHT - play_label.get_height() - 10))
        pygame.display.update()


    run = True
    while run:
        player.x = (WIDTH / 2) - (player.get_width() / 2)
        player.y = (HEIGHT / 2) - (player.get_height() / 2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    chgShip(player, -1)
                if event.key == pygame.K_e:
                    chgShip(player, 1)

                if event.key == pygame.K_SPACE:
                    run = False
        
        reDraw(WIN)
        
    main()
        

if __name__ == '__main__':
    main_menu()
    pygame.display.quit()
