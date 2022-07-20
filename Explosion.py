import sys, pygame as pg
import random
import math

DEBUG = False
MAX_SPEED = 3
NUM_PARTICLES = 500
FPS = 30
EXPLOSION_TIME_S = 4

color_background = pg.Color('black')
radius = 2

pg.init()
pg.display.set_caption("Explosion!")
screen_length = 750
screen = pg.display.set_mode((screen_length, screen_length))

boom = pg.mixer.Sound("./explosion_sound.wav")
sound_on = True

class Particle():
    def __init__(self):
        pass

    def set_vals(self, origin, dir, speed, color):
        self.x = origin[0] #(x, y)
        self.y = origin[1]
        self.dir = dir #(vel_x, vel_y)
        self.speed = speed
        self.color = color
    
    def update(self):
        self.x += self.dir[0] * self.speed
        self.y += self.dir[1] * self.speed
    
    def transparency_update(self, amount):
        if self.color.a >= amount:
            self.color.a -= amount
        self.color = self.color.premul_alpha()
    
    def get_spot(self):
        return (self.x, self.y)
    
    def get_color(self):
        return self.color

def color_str(color):
    return f"({color.r}, {color.g}, {color.b})"

def two_dec(num):
    return "{:.2f}".format(num)

if __name__ == '__main__':
    clock = pg.time.Clock()
    screen.fill(color_background)
    print("TEST")

    while 1:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

        origin = (random.randint(0, screen_length), random.randint(0, screen_length))
        particles = [Particle() for _ in range(NUM_PARTICLES)]

        for particle in particles:
            angle = random.randint(0, 360)
            rad = math.radians(angle)
            vel = (math.cos(math.radians(angle)), math.sin(math.radians(angle)))

            speed = random.random() * MAX_SPEED

            color = pg.Color((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

            particle.set_vals(origin, vel, speed, color)
        
        if sound_on: boom.play()
        for i in range(FPS * EXPLOSION_TIME_S):
            screen.fill(color_background)

            for particle in particles:
                pg.draw.circle(screen, particle.get_color(), particle.get_spot(), radius)
                particle.update()
                if i % 4 == 0:
                    particle.transparency_update(1)
            clock.tick(FPS)


            pg.display.flip()

