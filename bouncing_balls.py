import pygame, math, random, sys
from pygame.locals import *
import numpy as np

pygame.init()

window_width = 600
window_height = 600

DISPLAYSURF = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Bouncing Balls')

FPS = 60
fpsClock = pygame.time.Clock()

BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)

class Ball():
    def __init__(self, position, velocity):
        self.pos = np.array(position, dtype=np.float64)
        self.rad = random.random() + 4.5
        self.vel = np.array(velocity, dtype=np.float64)
        self.elastic = random.randint(70, 100) / 100
        self.mass = 150 + self.rad * 50
        self.col = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.inside = True

class gamePlay():
    def __init__(self):
        self.circle_center = np.array([window_width / 2, window_height / 2], dtype=np.float64)
        self.circle_radius = 150

        self.gravity = 0.2
        self.spinning_speed = 0.01
        self.arc_mass = 1_000_000_000

        self.arc_deg = 60
        self.start_angle = math.radians(-self.arc_deg / 2)
        self.end_angle = math.radians(self.arc_deg / 2)

        self.ball_velocity = np.array([0, 0], dtype=np.float64)
        self.balls = [Ball([window_width // 2, window_height // 2 - 120], self.ball_velocity)]

    def draw(self):
        p1 = self.circle_center + (self.circle_radius + 1000) * np.array([math.cos(self.start_angle), math.sin(self.start_angle)])
        p2 = self.circle_center + (self.circle_radius + 1000) * np.array([math.cos(self.end_angle), math.sin(self.end_angle)])
        pygame.draw.polygon(DISPLAYSURF, BLACK, [self.circle_center, p1, p2], 0) 

        for ball in self.balls:
            pygame.draw.circle(DISPLAYSURF, ball.col, ball.pos, ball.rad) 

    def check_inside(self, ball_pos):
        dx = ball_pos[0] - self.circle_center[0]
        dy = ball_pos[1] - self.circle_center[1]
        ball_angle = math.atan2(dy, dx)

        self.end_angle %= (2 * math.pi)
        self.start_angle %= (2 * math.pi)

        if self.start_angle > self.end_angle:
            self.end_angle += 2 * math.pi

        return (self.start_angle <= ball_angle <= self.end_angle) or (self.start_angle <= ball_angle + 2 * math.pi <= self.end_angle)

    def check_ball_collides_arc(self):
        for ball in self.balls:
            if ball.pos[1] > window_height or ball.pos[0] < 0 or ball.pos[0] > window_width or ball.pos[1] < 0:
                self.balls.remove(ball)
                self.balls.append(Ball([window_width // 2, window_height // 2 - 120], [random.uniform(-4, 4), random.uniform(-1, 1)]))
                if len(self.balls) < 40:
                    self.balls.append(Ball([window_width // 2, window_height // 2 - 120], [random.uniform(-4, 4), random.uniform(-1, 1)]))
            
            ball.vel[1] += self.gravity 
            ball.pos += ball.vel
            dist = np.linalg.norm(ball.pos - self.circle_center)
            if dist + ball.rad > self.circle_radius:
                if self.check_inside(ball.pos):
                    ball.inside = False

                if ball.inside:
                    normal = ball.pos - self.circle_center
                    normal = normal / np.linalg.norm(normal)
                    spinning_velocity = np.dot(ball.vel, normal)
                    ball.pos = self.circle_center + (self.circle_radius - ball.rad) * normal
                    ball.vel = (ball.vel * (ball.mass - self.arc_mass)) / (ball.mass + self.arc_mass)
                    ball.vel += spinning_velocity * self.spinning_speed
                    ball.vel *= ball.elastic
    
    def check_ball_collides_ball(self):
        for i in range(len(self.balls)):
            for j in range(i+1, len(self.balls)):
                ball1 = self.balls[i]
                ball2 = self.balls[j]
                dist = np.linalg.norm(ball1.pos - ball2.pos)
                if dist <= ball1.rad + ball2.rad:
                    normal = ball2.pos - ball1.pos
                    normal = normal / np.linalg.norm(normal)

                    relative_velocity = np.dot(ball2.vel - ball1.vel, normal)

                    if relative_velocity > 0:
                        restitution = 0.1  
                        impulse = -(1 + restitution) * relative_velocity / (1 / ball1.mass + 1 / ball2.mass)

                        ball1.vel += impulse * normal / ball1.mass
                        ball2.vel -= impulse * normal / ball2.mass
                        ball1.vel *= ball1.elastic
                        ball2.vel *= ball2.elastic
    
    def check_collisions(self):
        self.check_ball_collides_arc()
        self.check_ball_collides_ball()

def Bouncing_Balls():
    play = gamePlay()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        play.start_angle += play.spinning_speed
        play.end_angle += play.spinning_speed

        play.check_collisions()

        DISPLAYSURF.fill(BLACK)  
        pygame.draw.circle(DISPLAYSURF, ORANGE, play.circle_center, play.circle_radius, 3)  
        play.draw() 
        
        pygame.display.update()
        fpsClock.tick(FPS)

if __name__ == '__main__':
    Bouncing_Balls()