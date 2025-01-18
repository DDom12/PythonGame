from pygame import *
from random import randint
from time import time as timer


#background music
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
 
 
#fonts and captions
font.init()
font2 = font.SysFont(None, 36)
 
num_fire = 0
rel_time = False
last_time = 0
#we need the following images:
img_back = "galaxy.jpg" # game background
img_hero = "rocket.png" # hero
img_enemy = "ufo.png"
img_bullet = "bullet.png" # enemy
img_asteroid = "asteroid.png"
bullets = sprite.Group()
 
score = 0 #ships destroyed
lost = 0 #ships missed
clock = time.Clock()
 
#parent class for other sprites
class GameSprite(sprite.Sprite):
 #class constructor
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        #Call for the class (Sprite) constructor:
        sprite.Sprite.__init__(self)
    
    
        #every sprite must store the image property
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
    
    
        #every sprite must have the rect property that represents the rectangle it is fitted in
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    #method drawing the character on the window
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

 
#main player class
class Player(GameSprite):
   #method to control the sprite with arrow keys
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    #method to "shoot" (use the player position to create a bullet there)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
        fire_sound.play()
    
 
#enemy sprite class  
class Enemy(GameSprite):
   #enemy movement
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Asteroid(GameSprite):
   #enemy movement
    def update(self):
        self.rect.y += self.speed
        global lost



    
 
#create a small window
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
 
 
#create sprites
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
 
 
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

  
asteroids = sprite.Group()
for i in range(1, 6):
    asteroid = Asteroid(img_asteroid, randint(80, win_width - 80), -30, 50, 30, randint(1, 5))
    asteroids.add(asteroid)

 
#the "game is over" variable: as soon as True is there, sprites stop working in the main loop
finish = False
#Main game loop:
run = True #the flag is reset by the window close button
while run:
    #"Close" button press event
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                        num_fire = num_fire + 1
                        fire_sound.play()
                        ship.fire()
 
                if num_fire  >= 5 and rel_time == False : #if the player fired 5 shots
                    last_time = timer() #record time when this happened
                    rel_time = True #set the reload flag


    if not finish:
        window.blit(background,(0,0))
        
 
       #write text on the screen
        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
    
    
        text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            #this loop will repeat as many times as the number of monsters hit
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(ship, asteroids, False):
            finish = True
            text_death = font2.render("You Died...", True, (255, 0, 0))
            window.blit(text_death, (290, 250))

        if score == 10:
            finish = True
        elif lost >= 3:
            finish = True


            
        
    
        #launch sprite movements
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()
    
    
        #update them in a new location in each loop iteration
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
    
        display.update()
        clock.tick(60)

    else:
        if score == 10:
            finish = True
            text_win = font2.render("You win", True, (0, 255, 0))
            window.blit(text_win, (350, 250))
        elif lost >= 3:
            finish = True
            text_lose = font2.render("You lose...", True, (255, 0, 0))
            window.blit(text_lose, (350, 250))
        display.update()
            
    #the loop is executed each 0.05 se   c
    time.delay(50)
    display.update()