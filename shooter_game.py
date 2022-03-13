#Create your own shooter
from pygame import *
from random import randint
from time import time as timer

font.init()
font2 = font.SysFont('Arial',36)

lose = font2.render("YOU LOSE", True, (180,0,0))

#Sound effect
mixer.init()
fire_sound = mixer.Sound("fire.ogg")

lost = 0
score = 0
life = 3


class GameSprite(sprite.Sprite):
    def __init__(self, player_Image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_Image),(size_x, size_y))
        self.image.set_colorkey(0,0)
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x = self.rect.x - self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 85:
            self.rect.x = self.rect.x + self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 100:
            self.rect.y = self.rect.y + self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y = self.rect.y - self.speed   
    def fire(self):
        bullet = Bullet("Fire.png", self.rect.centerx, self.rect.top, 30,50,15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y = self.rect.y + self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint (80, win_width-80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y = self.rect.y - self.speed
        if self.rect.y < 0:
            self.kill()



#Default window size
win_width = 700
win_height = 500

#Window tittle
display.set_caption("Neon Space Shooting Game")

#Window
window = display.set_mode((win_width,win_height))
background = transform.scale(image.load('galaxy.jpg'),(win_width,win_height))
ship = Player("Arrow.png", 5, win_height - 100, 80, 100, 10)
monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy("Star.png", randint(80, win_width - 80), -40, 80, 58, randint(1,5))
    monsters.add(monster)

aliens = sprite.Group()
for a in range(1,3):
    alien = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 58,1)
    aliens.add(alien)

bullets = sprite.Group()

#Game Loop
finish = False
run = True
    
rel_time = False
num_fire = 0

FPS = 60
clock = time.Clock()

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 10 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 10 and rel_time == False:
                    last_time = timer()
                    rel_time = True
                

    if not finish:
        window.blit(background,(0,0))
        #Score Table
        text_score = font2.render("Score:" +str(score),1,(255,255,255))
        window.blit(text_score,(10,20))
        #Miss Table
        text_lose = font2.render("Missed:" +str(lost),1,(225,255,255))
        window.blit(text_lose,(10,50))
        ship.update()
        monsters.update()
        aliens.update()
        bullets.update()
        aliens.draw(window)
        bullets.draw(window)

        if rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                reloading = font2.render('Wait, reloading bullets..',1,(150,0,0))
                window.blit(reloading, (260, 460))
            else:
                num_fire = 0
                rel_time = False
        
        #Collision
        collides = sprite.groupcollide(monsters  , bullets,True,True)
        for c in collides:
            score += 1
            monster = Enemy("Star.png", randint(80, win_width - 80), -40, 80, 58, randint(1,5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, aliens, False):
            sprite.spritecollide(ship, aliens, True)
            sprite.spritecollide(ship, monsters, True)
            life = life - 1

        if life ==0:
            finish = True
            window.blit(lose,(200,200))

        text_life = font2.render(str(life),1,(0,150,0))
        window.blit(text_life,(650,10))

        ship.reset()
        monsters.draw(window)
        display.update()


    clock.tick(FPS)