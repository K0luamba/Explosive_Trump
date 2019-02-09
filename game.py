import pygame
import random

pygame.init()
win = pygame.display.set_mode((500,530))
info_string = pygame.Surface((500,30))
info_string.fill((45,80,40))
pygame.display.set_caption("Cubes Game")
clock = pygame.time.Clock()
#loading sprites
walkRight = [pygame.image.load('right_1.png'), pygame.image.load('right_2.png'), pygame.image.load('right_3.png'), pygame.image.load('right_4.png'), pygame.image.load('right_5.png'), pygame.image.load('right_6.png')]
walkLeft = [pygame.image.load('left_1.png'), pygame.image.load('left_2.png'), pygame.image.load('left_3.png'), pygame.image.load('left_4.png'), pygame.image.load('left_5.png'), pygame.image.load('left_6.png')]
bg = pygame.image.load('bg.jpg')
playerStand = pygame.image.load('idle.png')
explosion = pygame.image.load('explosion.png')
aim = pygame.image.load('aim.png')
#characteristics of player
x = 50 
y = 450
width = 40
height = 60
speed = 5
isJump = False
jumpCount = 10
left = False
right = False
animCount = 0
points = 0
lastMove = "right"
run = True
playTime = 30 #seconds
bullets = []
bulletsCount = 0
#we make aim to player
aimR = 20
aimXL = random.randint(2*aimR,500-aimR*2)
aimYU = random.randint(280,480-aimR*2)
aimXR = aimXL + 2*aimR
aimYD = aimYU + 2*aimR
#using fonts
pygame.font.init()
inf_font = pygame.font.SysFont('Comic Sans MS', 24)

class snaryad():
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing
    def draw(self, win): #before explosion
        pygame.draw.circle(win, self.color, (self.x, self.y), self. radius)
    def explode(self, win): #explosion
        #pygame.draw.circle(win, (0,0,255), (self.x, self.y), self. radius * 3)
        if self.x < 8:
            win.blit(explosion, (self.x - 80, self.y - 120))
        else:
            win.blit(explosion, (self.x - 120, self.y - 120))

def DrawWindow():
    global animCount, aimXR, aimXL, aimYD, aimYU, points, inf_font, playTime
    win.blit(info_string,(0,0))
    info_string.fill((0,80,40))
    info_string.blit(inf_font.render('Score: ' + str(points), 1, (210, 120, 200)), (10, 0))
    info_string.blit(inf_font.render('Time: ' + str(round(playTime)), 1, (210, 120, 200)), (300, 0))  
    win.blit(bg, (0,30)) #need to move our objects on 30 pixels down
    #pygame.draw.circle(win, (255, 0 ,0), (0, 0), 20)
    if animCount + 1 >= 30: #we have 30 frames per second
        animCount = 0
    if left:
        win.blit(walkLeft[animCount//5], (x,y))
        animCount += 1
    elif right:
        win.blit(walkRight[animCount//5], (x,y))
        animCount += 1
    else:
        win.blit(playerStand, (x,y))
    win.blit(aim, (aimXL, aimYU-2))
    for bullet in bullets:
        if bullet.x < 492 and bullet.x > 8:
            bullet.draw(win)
        else:
            bullet.explode(win)
        if bullet.x <= aimXR and bullet.x >= aimXL and bullet.y <= aimYD+4 and bullet.y >= aimYU-4: 
            bullet.explode(win)
            points += 1
            aimXL = random.randint(2*aimR,500-aimR*2) #making new aim
            aimYU = random.randint(280,480-aimR*2)
            aimXR = aimXL + 2*aimR
            aimYD = aimYU + 2*aimR      
    pygame.display.update() #in this moment we load all info on screen

while run:
    clock.tick(30)
    pygame.time.delay(50) #time for one cycle (ms)
    playTime -= 1/20
    if playTime <= 0: #player have limited time for game
        run = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False #exit from cycle
            
    if bulletsCount > 0:
        bulletsCount -= 1
    for bullet in bullets:
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]: #exit using key
        run = False
    if keys[pygame.K_f] and bulletsCount == 0:
        if lastMove == "right":
            facing = 1
        else:
            facing = -1
        bulletsCount = 15 #player can fire only 2 bullets per second
        bullets.append(snaryad(round(x + width // 2),round(y + height // 2), 5, (255, 0, 0), facing))
    
    if keys[pygame.K_LEFT] and x > 5: #moving
        x -= speed
        left = True
        right = False
        lastMove = "left"
    elif keys[pygame.K_RIGHT] and x < 500 - width - 5:
        x += speed
        left = False
        right = True
        lastMove = "right"
    else:
        left = False
        right = False
        animCount = 0
    if not(isJump):
        if keys[pygame.K_SPACE]:
            isJump = True
    else:
        if jumpCount >= - 10: #fly parabolic trajectory
            if jumpCount < 0:
                y += (jumpCount ** 2) / 2
            else:
                y -= (jumpCount ** 2) / 2
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 10
    DrawWindow()
pygame.quit()
print("Your score - ", points)
