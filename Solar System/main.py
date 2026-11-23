import math
import pygame

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_size = screen.get_size()
pygame.display.set_caption("Solar System Simulation")

import game_constants
import celestial_body as bodies

clock = pygame.time.Clock() 

background_image_surface = pygame.image.load('assets/background.jpg').convert_alpha()
background_image_surface = pygame.transform.scale(background_image_surface, screen_size)

running = True
dragging = False

while running:
    frame_dt = clock.tick(game_constants.FPS) / 1000.0
    simulation_dt = frame_dt * game_constants.SIMULATION_TIME_SCALE
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            running = False
            
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0: # zoom in
                a = game_constants.TARGET_BODY_SCALE_DOWN - game_constants.ZOOM_BODY_SCALE
                b = game_constants.TARGET_DISTANCE_FROM_SUN_SCALE - game_constants.ZOOM_DISTANCE_FROM_SUN_SCALE
                c = game_constants.TARGET_DRAG_FACTOR - game_constants.ZOOM_DRAG_FACTOR
                if a > 0 and b > 0 and c > 0:
                    game_constants.TARGET_BODY_SCALE_DOWN = a
                    game_constants.TARGET_DISTANCE_FROM_SUN_SCALE = b
                    game_constants.TARGET_DRAG_FACTOR = c
                    
            elif event.y < 0: # zoom out
                game_constants.TARGET_BODY_SCALE_DOWN += game_constants.ZOOM_BODY_SCALE            
                game_constants.TARGET_DISTANCE_FROM_SUN_SCALE += game_constants.ZOOM_DISTANCE_FROM_SUN_SCALE
                game_constants.TARGET_DRAG_FACTOR += game_constants.ZOOM_DRAG_FACTOR
                
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            dragging = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            dragging = False
        elif event.type == pygame.MOUSEMOTION and dragging:
            dx, dy = event.rel
            game_constants.ORIGIN_X += dx * game_constants.DRAG_FACTOR
            game_constants.ORIGIN_Y += dy * game_constants.DRAG_FACTOR

    alpha = 1 - math.exp(-game_constants.ZOOM_SMOOTHING_RATE * frame_dt)
    game_constants.BODY_SCALE_DOWN += (game_constants.TARGET_BODY_SCALE_DOWN - game_constants.BODY_SCALE_DOWN) * alpha
    game_constants.DISTANCE_FROM_SUN_SCALE += (game_constants.TARGET_DISTANCE_FROM_SUN_SCALE - game_constants.DISTANCE_FROM_SUN_SCALE) * alpha
    game_constants.DRAG_FACTOR += (game_constants.TARGET_DRAG_FACTOR - game_constants.DRAG_FACTOR) * alpha
    
    screen.blit(background_image_surface, (0, 0))
    bodies.sun.blit_body(screen)

    accelerations = []
    for planet in bodies.planets:
        other_bodies = [body for body in bodies.planets if body is not planet]
        other_bodies.append(bodies.sun)
        accelerations.append(planet.calculate_acceleration(other_bodies))

    for planet, acceleration in zip(bodies.planets, accelerations):
        planet.update(acceleration, simulation_dt)
        planet.blit_body(screen)

    pygame.display.flip()
    
pygame.quit()


