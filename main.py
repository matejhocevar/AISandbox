import pygame, sys, math, random, search
from pygame.locals import *

#game engine init
pygame.init()
fpsClock = pygame.time.Clock()

h = 480
w = 640

#create frame
frame = pygame.display.set_mode((w, h))
pygame.display.set_caption('Pygame sandbox')  


def getRandomPosition():
	return [random.randint(0,w),random.randint(0,h)]
	
#constants
white = pygame.Color(255, 255, 255)
blue = pygame.Color(0,0,255)
rand = getRandomPosition()
vel = [0,0]

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

        self.dimension = [15,32]
        self.rect = self.current_direction.get_rect()
        self.current_direction = self.standing
        self.current_position = [w/2,h/2]
        self.speed = speed
        self.vel = vel
        self.animation_interval = 25
        self.solved = False
        self.wounded_position = [0,0]
        self.walls = []

    def updatePosition(self, walls, wounded):
        x,y = self.current_position
        self.current_position[0] += self.vel[0]
        self.current_position[1] += self.vel[1]
        self.walls = walls
        self.wounded_position = wounded

        collision = False
        for wall in walls:
			collision |= self.collisionDetection(wall)

        if collision:
        	self.current_position[0] = x
        	self.current_position[1] = y
		
    def setVelocity(self, vel):
        self.vel[0] += vel[0]
        self.vel[1] += vel[1]
        #self.vel[0] = vel[0]
        #self.vel[1] = vel[1]

    def getDirection(self):
        abs_x = math.fabs(self.vel[0])
        abs_y = math.fabs(self.vel[1])
        
        #print abs_x, abs_y
        if self.vel[0] + self.vel[1] == 0:
            return self.standing

        if abs_x == abs_y: #here somewhere is bug moving up/down and left/right at the same time
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

    def c(self, rx,ry):
        x,y = self.current_position
        self.current_position[0] += rx
        self.current_position[1] += ry

        collision = False
        for wall in self.walls:
			collision |= self.collisionDetection(wall)
        if collision:
        	self.current_position[0] = x
        	self.current_position[1] = y
        return collision
			
    def checkCollision(self, destination):
        x = math.fabs(destination[0] - self.current_position[0])
        y = math.fabs(destination[1] - self.current_position[1])
        return (x + y) > 30

    def collisionDetection(self, wall):
		x,y,width,height = wall.get_info();
		min_x, min_y = self.current_position

		l_x = x - self.dimension[0]
		l_y = y - self.dimension[1]

		h_x = x + width
		h_y = y + height

		if (min_x in range(l_x, h_x)) and (min_y in range(l_y, h_y)):
			return True
		return False

    def save(self, destination):
        x = math.fabs(destination[0] - self.current_position[0])
        y = math.fabs(destination[1] - self.current_position[1])

        a = self.current_position[0]
        b = self.current_position[1]     
        
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

    def GenerateMoves(self):
        rx, ry = self.current_position
        moves = []
        for x in [-10,0,10]:
            for y in [-10,0,10]:
                if (x or y) and \
                   rx+x < w and rx+x >= 0 and \
                   ry+y < h and ry+y >= 0:# and \
                   #not self.c(rx+x,ry+y):
                    moves.append( ([x,y], math.sqrt(x**2+y**2)) )
        return moves	

    def Move(self, move_cost):
        move, cost = move_cost
        self.current_position[0] += move[0]
        self.current_position[1] += move[1]

    def UndoMove(self, move_cost):
        move, cost = move_cost
        self.current_position[0] -= move[0]
        self.current_position[1] -= move[1]

    def Evaluate(self):
        return math.sqrt((self.current_position[0] - self.wounded_position[0]) ** 2 + (self.current_position[1] - self.wounded_position[1]) ** 2)

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
        self.width = width
        self.height = height

    def get_info(self):
		return [self.rect.x,self.rect.y,self.width,self.height]	

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

man = Man(rand,3,vel)
wounded = Wounded()
wounded2 = Wounded()
wounded3 = Wounded()
movingsprites = pygame.sprite.RenderPlain()
movingsprites.add(man)

wall_list=pygame.sprite.RenderPlain()
wall=Wall(0,0,10,600)
wall_list.add(wall)
wall=Wall(10,0,790,10)
wall_list.add(wall)
wall=Wall(10,200,100,10)
wall_list.add(wall)
wall=Wall(w,0,h,10)
wall_list.add(wall)
wall=Wall(h,200,w,10)
wall_list.add(wall)


def ID(Pos):
    # iterative deepening
    depth = 0
    while True:
        Path = DF(Pos, depth)
        if Path != None:
            return Path
        depth += 1

def DF(p, depth):
    # depth-first search
    if depth < 0: return None
    if p.solved: return []
    for move in p.GenerateMoves():
        p.Move(move)
        FoundPath = DF(p, depth-1)
        paint()
        p.UndoMove(move)
        if FoundPath != None:
            FoundPath.insert(0, move)
            return FoundPath
    return None

def DF_basic(Pos):
    # depth-first search
    if Pos.solved: return []
    for move in Pos.GenerateMoves():
        paint()
        Pos.Move(move)
        FoundPath = DF_basic(Pos)
        Pos.UndoMove(move)
        if FoundPath != None:
            FoundPath.insert(0, move)
            return FoundPath
    return None

def paint():
    frame.fill(white)
    man.update(wall_list, wounded.getPosition())
     
    wall_list.draw(frame)
    man.updatePosition(wall_list, wounded.getPosition())

    frame.blit(wounded.getDirection(), wounded.getPosition()) 
    frame.blit(man.getDirection(), man.getPosition())

    #if man.checkCollision(wounded.getPosition()):
	  #man.save(wounded.getPosition())
    #else:
	  #man.stopIt()
	  #wounded.setPosition([random.randint(0,w),random.randint(0,h)])
    #search.ID(man)
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

    pygame.display.flip()
    fpsClock.tick(30) 

DF_basic(man)
