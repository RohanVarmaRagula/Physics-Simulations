from __future__ import annotations
import pygame
import math
from collections import deque
from enum import Enum

import physics
import game_constants

class CelestialBodyType(Enum):
    STAR = 1
    PLANET = 2
    DWARF_PLANET = 3

class CelestialBody: 
    def __init__(self, 
                 name: str, 
                 type: CelestialBodyType, 
                 mass: float, 
                 radius: float, 
                 image_path: str,
                 x: float = game_constants.ORIGIN_X, # heliocentri coords
                 y: float = game_constants.ORIGIN_Y,
                 v_x: float = 0,
                 v_y: float = 0,
                 a_x: float = 0,
                 a_y: float = 0,
                 display_diameter: int = 1
    ):
        self.name = name
        self.type = type
        self.mass = mass
        self.radius = radius
        self.image_path = image_path
        self.display_diameter = display_diameter
        self.image = pygame.image.load(image_path).convert_alpha()
        self.position2D = pygame.Vector2(x, y)
        self.velocity2D = pygame.Vector2(v_x, v_y)
        self.acceleration2D = pygame.Vector2(a_x, a_y)
        
        # cache
        self._prev_scaled_diameter = 0
        self._prev_final_masked_surface = None
        
        # calculations
        if self.type != CelestialBodyType.STAR:
            orbital_velocity_magnitude = game_constants.UNIVERSAL_GRAVITATIONAL_CONSTANT * game_constants.MASS_OF_SUN / self.position2D.magnitude()
            self.velocity2D = pygame.Vector2(0, math.sqrt(orbital_velocity_magnitude)) # 0.i+v_o.j 
    
        # other 
        self.trace_points = deque(
            [self.position2D.copy()],
            maxlen=game_constants.MAX_DEQUE_POINTS_FOR_TRACE,
        )
    
    def move(self, time: float):
        """r_f = r_i + v.t"""
        vt = time * self.velocity2D
        r_f = self.position2D + vt
        self.update_center(r_f.x, r_f.y)
    
    def update_center(self, new_x: float, new_y: float):
        self.position2D.update(new_x, new_y)
        self.trace_points.append(self.position2D.copy())
        
    def update_velocity(self, new_v_x: float, new_v_y: float):
        self.velocity2D.update(new_v_x, new_v_y)
    
    def update_acceleration(self, new_a_x: float, new_a_y: float):
        self.acceleration2D.update(new_a_x, new_a_y)
        
    def resultant_force_of_gravity(self, bodies: list[CelestialBody]) -> pygame.Vector2:
        resultant_f_g = pygame.Vector2()
        
        for body in bodies:
            f_g_body = physics.force_of_gravity(self.mass, body.mass, self.position2D, body.position2D)
            resultant_f_g = resultant_f_g + f_g_body
            
        return resultant_f_g
    
    def calculate_acceleration(self, other_bodies: list[CelestialBody]) -> pygame.Vector2:
        resultant_force = self.resultant_force_of_gravity(other_bodies)
        return physics.acceleration_due_to_force(resultant_force, self.mass)
    
    def getScaledScreenPosition(self, screen: pygame.Surface, position: pygame.Vector2) -> pygame.Vector2:
        return pygame.Vector2(
            screen.get_width() // 2 + 
            round((position.x + game_constants.ORIGIN_X) / game_constants.DISTANCE_FROM_SUN_SCALE),
            screen.get_height() // 2 + 
            round((position.y + game_constants.ORIGIN_Y) / game_constants.DISTANCE_FROM_SUN_SCALE)
        )
    
    def update(self, new_acceleration: pygame.Vector2, dt: float):
        new_velocity = physics.velocity_due_to_acceleration(self.velocity2D, new_acceleration, dt)
        new_position = physics.position_due_to_velocity(self.position2D, new_velocity, dt)
        self.update_acceleration(new_acceleration.x, new_acceleration.y)
        self.update_velocity(new_velocity.x, new_velocity.y)
        self.update_center(new_position.x, new_position.y)

    def blit_body(self, screen: pygame.Surface):
        scaled_diameter = max(
            1,
            round(self.display_diameter * game_constants.BASE_BODY_SCALE_DOWN / game_constants.BODY_SCALE_DOWN)
        )
        scaled_radius = scaled_diameter // 2
        if self._prev_scaled_diameter != scaled_diameter or self._prev_final_masked_surface is None:
            transformed_surface = pygame.transform.scale(self.image, (scaled_diameter, scaled_diameter))
            mask_surface = pygame.Surface((scaled_diameter, scaled_diameter), pygame.SRCALPHA)
            pygame.draw.circle(mask_surface, (255, 255, 255, 255), (scaled_radius, scaled_radius), scaled_radius)
            transformed_surface.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
            
            self._prev_final_masked_surface = transformed_surface
            self._prev_scaled_diameter = scaled_diameter
        else:
            transformed_surface = self._prev_final_masked_surface
        
        if self.type != CelestialBodyType.STAR and len(self.trace_points) > 1:
            trace_screen_points = [self.getScaledScreenPosition(screen, position) for position in self.trace_points]
            pygame.draw.lines(screen, (255, 255, 255), False, trace_screen_points)
        
        blit_coords = self.getScaledScreenPosition(screen, self.position2D)
        screen.blit(transformed_surface, (blit_coords.x - scaled_radius, blit_coords.y - scaled_radius))
        
        
        
# stars
sun = CelestialBody(
    "Sun", CelestialBodyType.STAR, 1.9885e30, 6.957e8, "assets/sun.jpg",
    display_diameter=96,
)

# planets
planets = [   
CelestialBody("Mercury", CelestialBodyType.PLANET, 3.3011e23, 2.4397e6, "assets/planets/mercury.jpg", 5.79e10, display_diameter=12),
CelestialBody("Venus", CelestialBodyType.PLANET, 4.8675e24, 6.0518e6, "assets/planets/venus.jpg", 1.082e11, display_diameter=16),
CelestialBody("Earth", CelestialBodyType.PLANET, 5.9722e24, 6.3710e6, "assets/planets/earth.jpg", 1.496e11, display_diameter=16),
CelestialBody("Mars", CelestialBodyType.PLANET, 6.4171e23, 3.3895e6, "assets/planets/mars.jpg", 2.279e11, display_diameter=14),
CelestialBody("Jupiter", CelestialBodyType.PLANET, 1.8982e27, 6.9911e7, "assets/planets/jupiter.jpg", 7.786e11, display_diameter=48),
CelestialBody("Saturn", CelestialBodyType.PLANET, 5.6834e26, 5.8232e7, "assets/planets/saturn.jpg", 1.434e12, display_diameter=42),
CelestialBody("Uranus", CelestialBodyType.PLANET, 8.6810e25, 2.5362e7, "assets/planets/uranus.jpg", 2.871e12, display_diameter=30),
CelestialBody("Neptune", CelestialBodyType.PLANET, 1.02413e26, 2.4622e7, "assets/planets/neptune.jpg", 4.495e12, display_diameter=30),
]
