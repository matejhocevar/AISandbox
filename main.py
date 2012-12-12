import pygame, sys, math, random
from pygame.locals import *

#game engine init
pygame.init()
fpsClock = pygame.time.Clock()

h = 480
w = 640
#create frame
frame = pygame.display.set_mode((w, h))
pygame.display.set_caption('Pygame sandbox')

#class
class Man(pygame.sprite.Sprite):
    def __init__(self, position, speed, vel):
        pygame.sprite.Sprite.__init__(self)
        self.current_direction = pygame.Surface([15, 15])
        self.standing = pygame.image.load('assets/m_standing.png')
        self.left = pygame.image.load('assets/m_left.png')
        self.walkingLeft = pygame.image.load('assets/m_walking_left.png')
        self.up = pygame.image.load('assets/m_up.png')
        self.walkingUp = pygame.image.load('assets/m_walking_up.png')
        self.down = pygame.image.load('assets/m_down.png')
        self.walkingDown = pygame.image.load('assets/m_walking_down.png')
        self.right = pygame.image.load('assets/m_right.png')
        self.walkingRight = pygame.image.load('assets/m_walking_right.png')

        self.rect = self.current_direction.get_rect()
        self.current_direction = self.standing
        self.current_position = [w/2,h/2]
        self.speed = speed
        self.vel = vel
        self.animation_interval = 25
        self.solve = False

    def updatePosition(self, walls):
        x,y = self.current_position
        self.current_position[0] += self.vel[0]

        #collide = pygame.sprite.spritecollide(self, walls, False)
        #if collide:
            #self.current_position[0] = x
            #print walls

        self.current_position[1] += self.vel[1]

        #collide = pygame.sprite.spritecollide(self, walls, False)
        #if collide:
            #self.current_position[1] = y
            #print walls

    def setVelocity(self, vel):
        self.vel[0] += vel[0]
        self.vel[1] += vel[1]
        #self.vel[0] = vel[0]
        #self.vel[1] = vel[1]

    def getDirection(self):
        abs_x = math.fabs(self.vel[0])
        abs_y = math.fabs(self.vel[1])

        if self.vel[0] + self.vel[1] == 0:
            return self.standing

        elif abs_x == abs_y: #here somewhere is bug moving up/down and left/right at the same time
su
            if self.vel[1] > 0:
                if self.vel[0] < 0:
                    if self.current_position[0] % self.animation_interval < self.animation_interval/2:
                        return self.walkingLeft
                    return self.left
                else:
                     if self.current_position[0] % self.animation_interval < self.animation_interval/2:
                        return self.walkingRight
                     return self.right
            elif self.vel[1] < 0:
                if self.vel[0] < 0:
                    if self.current_position[0] % self.animation_interval < self.animation_interval/2:
                        return self.walkingLeft
                    return self.left
                else:
                     if self.current_position[0] % self.animation_interval < self.animation_interval/2:
                        return self.walkingRight
                     return self.right

        elif self.vel[0] < 0:
            if self.current_position[0] % self.animation_interval < self.animation_interval/2:
                return self.walkingLeft
            return self.left

        elif self.vel[0] > 0:
            if self.current_position[0] % self.animation_interval < self.animation_interval/2:
                return self.walkingRight
            return self.right

        elif self.vel[1] < 0:
            if self.current_position[1] % self.animation_interval < self.animation_interval/2:
                if vel[1] < vel[0]:
                    return self.walkingUp
            return self.up

        elif self.vel[1] > 0:
            if self.current_position[1] % self.animation_interval < self.animation_interval/2:
                return self.walkingDown
            return self.down                

    def getPosition(self):
        return self.current_position

    def stopIt(self):
        self.vel[0] = 0
        self.vel[1] = 0

    def get_rect():
        return self.rect

    def getSpeed(self):
        return self.speed

    def checkCollision(self, destination):
        x = math.fabs(destination[0] - self.current_position[0])
        y = math.fabs(destination[1] - self.current_position[1])
        return (x + y) > 30

    def save(self, destination):
        x = math.fabs(destination[0] - self.current_position[0])
        y = math.fabs(destination[1] - self.current_position[1])

        a = self.current_position[0]
        b = self.current_position[1]     

        #print a,destination[0]
        
        if a != destination[0] or x > 50:
            if self.current_position[0] - destination[0] > 0:
                    self.setVelocity([-1 * self.getSpeed(),0])
            else:
                    self.setVelocity([1 * self.getSpeed(),0])
        else:
            if b != destination[1]:
                if self.current_position[1] - destination[1] > 0:
                        self.setVelocity([0,-1 * self.getSpeed()])
                else:
                        self.setVelocity([0,1 * self.getSpeed()])   
    
class Wounded(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.wounded = pygame.Surface([20, 20])
        self.wounded = pygame.image.load('assets/m_wounded.png')
        self.position = [random.randint(0,w),random.randint(0,h)]
        self.rect = self.wounded.get_rect()

    def getPosition(self):
        return self.position

    def getDirection(self):
        return self.wounded

    def get_rect(self):
        return self.rect

    def setPosition(self, new):
        self.position[0] = new[0]
        self.position[1] = new[1]

class Wall(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height):
        pygame.sprite.Sprite.__init__(self)

        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(blue)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

#constants
white = pygame.Color(255, 255, 255)
blue = pygame.Color(0,0,255)
rand = [random.randint(0,w),random.randint(0,h)]
vel = [0,0]

man = Man(rand,2,vel)
wounded = Wounded()
wounded2 = Wounded()
wounded3 = Wounded()
movingsprites = pygame.sprite.RenderPlain()
movingsprites.add(man)

# Make the walls. (x_pos, y_pos, width, height)
wall_list=pygame.sprite.RenderPlain()
wall=Wall(0,0,10,600)
wall_list.add(wall)
wall=Wall(10,0,790,10)
wall_list.add(wall)
wall=Wall(10,200,100,10)
wall_list.add(wall)

while True:
    frame.fill(white)
    man.update(wall_list)
     
    #movingsprites.draw(frame)
    wall_list.draw(frame)
    #pygame.display.flip()
    man.updatePosition(wall_list)

    frame.blit(wounded.getDirection(), wounded.getPosition()) 
    frame.blit(man.getDirection(), man.getPosition())

    #if man.checkCollision(wounded.getPosition()):
        #man.save(wounded.getPosition())
    #else:
        #man.stopIt()
        #wounded.setPosition([random.randint(0,w),random.randint(0,h)])

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYUP and event.type != KEYDOWN:
            if event.key in (K_LEFT, K_RIGHT, K_UP, K_DOWN):
                if event.key == K_LEFT:
                    man.setVelocity([1 * man.getSpeed(),0])
                elif event.key == K_RIGHT:
                    man.setVelocity([-1 * man.getSpeed(),0])
                elif event.key == K_UP:
                    man.setVelocity([0,1 * man.getSpeed()])
                elif event.key == K_DOWN:
                    man.setVelocity([0,-1 * man.getSpeed()])
        elif event.type == KEYDOWN:
            if event.key in (K_LEFT, K_RIGHT, K_UP, K_DOWN):
                if event.key == K_LEFT:
                    man.setVelocity([-1 * man.getSpeed(),0])
                elif event.key == K_RIGHT:
                    man.setVelocity([man.getSpeed(),0])
                elif event.key == K_UP:
                    man.setVelocity([0,-1 * man.getSpeed()])
                elif event.key == K_DOWN:
                    man.setVelocity([0,man.getSpeed()])
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))
    #wall_list.draw(frame)
    #movingsprites.draw(frame)
    pygame.display.flip()
    fpsClock.tick(30) 
