import pygame as pg 

from pygame.locals import *

screen_width = 1000
screen_height = 1000

pg.init()
pg.display.set_caption("Fighting Game")
clock = pg.time.Clock()

screen = pg.display.set_mode([screen_width,screen_height])


floor = pg.Surface((1000,200))
floor.fill((71,142,36))

running = True
instances  = 0
bullets = pg.sprite.Group()

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        global instances
       
        if instances == 0:
            image = pg.image.load("H:\James School Work\A Level\Comp Sci\Coding\Python Coding\Fighting Game\FightingGamePlayer1.png").convert()
            image = pg.transform.scale(image,(50,100))
            self.surf = image
            self.rect = self.surf.get_rect(bottomleft = (200, 800))
            instances += 1
            self.instance = True
        else:
            image = pg.image.load("H:\James School Work\A Level\Comp Sci\Coding\Python Coding\Fighting Game\FightingGamePlayer2.png").convert()
            image = pg.transform.scale(image,(50,100))
            self.surf = image
            self.rect = self.surf.get_rect(bottomright = (800, 800))
            self.instance = False
        self.health = 400
        self.healthbar = pg.Surface((400,50))
        self.healthbar.fill((255,0,0))
        
        if self.instance:
            self.healthbar_rect = self.healthbar.get_rect(topleft = (50,50))
        else:
            self.healthbar_rect = self.healthbar.get_rect(topleft= (550,50))
      
        self.greenbar = pg.Surface((self.health,50))
        self.greenbar.fill((0,255,0))
        
        self.jumping = False
        self.jumpheight = 300
        self.cooldown = 500
        self.lasttick = 0
        self.direction = True
    def update(self):
        
        global bullets
        if self.jumping:
            if self.jumpheight > 0:
                self.rect.y -= 20  
                self.jumpheight -= 20
            else:
                self.jumping = False
                self.jumpheight = 300
        elif self.rect.y < 700:
            self.rect.y += 10
        
        keyspressed = pg.key.get_pressed()
        if self.instance:
           if self.rect.x >= 5:  
            if keyspressed[pg.K_a]:
                self.rect.x -= 5
                self.direction = True
           if self.rect.x <= 995:
            if keyspressed[pg.K_d]:
                self.rect.x += 5
                self.direction = False
            if keyspressed[pg.K_w] and not self.jumping and self.rect.y == 700:
                self.jumping = True
            if keyspressed[pg.K_s]:
                self.jumping = False
                if self.rect.y < 700:
                    self.rect.y += 10
            if keyspressed[pg.K_SPACE]:
                self.now = pg.time.get_ticks()
                if self.now - self.lasttick > self.cooldown:
                    if self.direction:
                        projectile = bullet(self.rect.x - 25, self.rect.y + 45, self.instance)
                        bullets.add(projectile)
                        self.lasttick = pg.time.get_ticks()  
                    else:
                        projectile = bullet(self.rect.x + 60, self.rect.y + 45, self.direction)
                        bullets.add(projectile)
                        self.lasttick = pg.time.get_ticks()
        if not self.instance:
           if self.rect.x >= 5:   
            if keyspressed[pg.K_LEFT]:
                self.rect.x -= 5
                self.direction = True
           if self.rect.x <= 945:
            if keyspressed[pg.K_RIGHT]:
                self.rect.x +=5
                self.direction = False
            if keyspressed[pg.K_UP] and not self.jumping and self.rect.y == 700:
                self.jumping = True
            if keyspressed[pg.K_DOWN]:
                self.jumping = False
                if self.rect.y < 700:
                    self.rect.y += 10
            if keyspressed[K_RSHIFT]:
                self.now = pg.time.get_ticks()
                if self.now - self.lasttick > self.cooldown: 
                    if self.direction:
                        projectile = bullet(self.rect.x - 25, self.rect.y + 45, self.direction)
                        bullets.add(projectile)
                        self.lasttick = pg.time.get_ticks()
                    else:
                        projectile = bullet(self.rect.x + 60, self.rect.y + 45, self.direction)
                        bullets.add(projectile)
                        self.lasttick = pg.time.get_ticks()
        for projectile in bullets:
            if pg.sprite.collide_rect(projectile,self):
                projectile.kill()
                self.health -= 50
        if self.health <= 0:
            self.kill()

class bullet(pg.sprite.Sprite):
    
    def __init__(self,x,y,direction):
        pg.sprite.Sprite.__init__(self)
        image = pg.image.load("H:\James School Work\A Level\Comp Sci\Coding\Python Coding\Fighting Game\FightingGameBullet.png").convert()
        image = pg.transform.scale(image,(25,10))
        if direction:
            image = pg.transform.rotate(image,180)
        self.surf = image
        self.rect = self.surf.get_rect(topleft = (x,y))
        self.direction = direction
    
    def update(self):
        if self.rect.x > 1000 or self.rect.x < -25:
            self.kill()
        if self.direction:
            self.rect.x -= 20
        else:
            self.rect.x += 20

def eventhandling():
    global running
    for event in pg.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

player1 = Player()
player2 = Player()
players = pg.sprite.Group()
players.add(player1)
players.add(player2)

while running:
    screen.fill((10,207,209))
    eventhandling()
    for player in players:
        player.update()
        screen.blit(player.surf,player.rect)
        screen.blit(player.healthbar,player.healthbar_rect)
        screen.blit(player.greenbar,player.healthbar_rect, (0, 0, player.health, 50))
    for projectile in bullets:
        projectile.update()
        screen.blit(projectile.surf,projectile.rect)
    
    screen.blit(floor,(0,800))
    pg.display.flip()

    if player1.health <= 0:
        while running:
            eventhandling()
            bg = pg.image.load("H:\James School Work\A Level\Comp Sci\Coding\Python Coding\Fighting Game\Player2wins.png")
            screen.blit(bg,(0,0))
            pg.display.flip()
    elif player2.health <= 0:
        while running:
            eventhandling()
            bg = pg.image.load("H:\James School Work\A Level\Comp Sci\Coding\Python Coding\Fighting Game\Player1wins.png")
            screen.blit(bg,(0,0))
            pg.display.flip()
    clock.tick(60)

pg.quit()