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
gravity = False

pg.init()
pg.display.set_caption("Explosion!")
screen_length = 750
screen = pg.display.set_mode((screen_length, screen_length))

selection_font = pg.font.SysFont("Arial", 30, True)

boom = pg.mixer.Sound("./explosion_sound.wav")
boom.set_volume(.3)
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
        if gravity:
            self.dir[1] += .02
        self.x += self.dir[0] * self.speed
        self.y += self.dir[1] * self.speed
    
    def transparency_update(self, amount):
        if self.color.a >= amount:
            self.color.a -= amount
        else:
            self.color.a = 0
        self.color = self.color.premul_alpha()
    
    def get_spot(self):
        return (self.x, self.y)
    
    def get_color(self):
        return self.color

def write_text(text, x, y):
    to_write = selection_font.render(text, 1, pg.Color("white"))
    screen.blit(to_write, (x - 60, y))




if __name__ == '__main__':
    clock = pg.time.Clock()

    selecting = True
    was_pressed = False
    while selecting:
        screen.fill(color_background)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

        if gravity:
            grav_status = "on"
        else:
            grav_status = "off"
        write_text(f"Gravity: {grav_status}", screen_length//2, screen_length//4)
        write_text("Start", screen_length//2, 3 * screen_length//4)
        pg.draw.line(screen, pg.Color("white"), (0, screen_length//2), (screen_length, screen_length//2))

        if pg.mouse.get_pressed()[0]:
            was_pressed = True
        if not pg.mouse.get_pressed()[0] and was_pressed:
            was_pressed = False

            mouse_x, mouse_y = pg.mouse.get_pos()
            if 0 <= mouse_y <= screen_length//2:
                gravity = not gravity
            else:
                selecting = False
        pg.display.flip()

    while 1:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

        origin = (random.randint(0, screen_length), random.randint(0, screen_length))
        particles = [Particle() for _ in range(NUM_PARTICLES)]

        for particle in particles:
            if gravity:
                angle = 360 - random.randint(30, 150)
            else:
                angle = random.randint(0, 360)
            rad = math.radians(angle)
            vel = [math.cos(math.radians(angle)), math.sin(math.radians(angle))]

            speed = random.random() * MAX_SPEED

            color = pg.Color((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

            particle.set_vals(origin, vel, speed, color)
        
        if sound_on: boom.play(); boom.fadeout(EXPLOSION_TIME_S * 1000)
        for i in range(FPS * EXPLOSION_TIME_S):
            screen.fill(color_background)

            for particle in particles:
                pg.draw.circle(screen, particle.get_color(), particle.get_spot(), radius)
                particle.update()
                if i % 4 == 0:
                    particle.transparency_update(1)
            clock.tick(FPS)


            pg.display.flip()

