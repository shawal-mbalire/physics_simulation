import pygame
import pygame
import math
import pymunk.pygame_util

pygame.init()

WIDTH, HEIGHT = 1000, 800
window = pygame.display.set_mode((WIDTH,HEIGHT))

def calculate_distance(p1,p2):
    return math.sqrt((p2[1]-p1[1])**2 + (p2[0]-p1[0])**2)

def calculate_angle(p1,p2):
    return math.atan2(p2[1]-p1[1],p2[0]-p1[0])

def draw(space, window, draw_options):
    window.fill("black")
    space.debug_draw(draw_options)
    pygame.display.update()
    return True

def create_boundaries(space, width, height):
    rectangles = [
        [(width/2, height-10),(width,20)],
        [(width/2, 10), (width, 20)],
        [(10, height/2),(20,height)],
        [(width - 10, height/2),(20,height)],
    ]

    for pos, size in rectangles:
        body = pymunk.Body(body_type = pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 0.4
        shape.friction = 0.5
        shape.color = (0,255,255,255)
        space.add(body,shape)

def create_ball(space, radius, mass, position):
    body = pymunk.Body()
    body.position = (300,300)
    shape = pymunk.Circle(body,radius)
    shape.mass = mass
    shape.color = (255,0,0,255) # rgba
    shape.elasticity = 0.9
    shape.friction = 0.4
    shape.position = position
    space.add(body, shape)
    return shape


def run(window, width, height):
    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1 / fps

    space = pymunk.Space()
    space.gravity = (0, 981)

    create_boundaries(space,width,height)
    # ball = create_ball(space, 40,10)
    pressed_position = None
    ball = None
    draw_options = pymunk.pygame_util.DrawOptions(window)

    while run:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not ball:
                    pressed_position = pygame.mouse.get_pos()
                    ball = create_ball(space,40,10,pressed_position)
                elif pressed_position:
                    ball.body.apply_impulse_at_local_point((10000,0),(0,0))
                    pressed_position = None
                else:
                    space.remove(ball, ball.body)
                    ball = None

        draw(space,window,draw_options)
        space.step(dt)
        clock.tick(fps)

    pygame.quit()

    return True

if __name__ == "__main__":
    run(window,WIDTH,HEIGHT)
