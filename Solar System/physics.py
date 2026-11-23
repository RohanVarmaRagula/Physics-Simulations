import pygame
import game_constants

def position_due_to_velocity(r_i: pygame.Vector2, v: pygame.Vector2, time: float):
    """r_f = r_i + v.t"""
    vt = v * time
    r_f = r_i + vt
    return r_f

def velocity_due_to_acceleration(v_i: pygame.Vector2, a: pygame.Vector2, time: float) -> pygame.Vector2:   
    """v = u + a.t
    """
    at = a * time
    v = v_i + at
    return v

def acceleration_due_to_force(F: pygame.Vector2, m: float) -> pygame.Vector2:   
    """Given F and m in, returns acceleration vector of the body.
        a = F/m
    """
    a = F / m
    return a

def force_of_gravity(m1: float, m2: float, r1: pygame.Vector2, r2: pygame.Vector2) -> pygame.Vector2:
    """Given masses of two bodies in SI units and their positions, returns the force of gravity acting on m1 due to m2.
        F = G.m1.m2/(r2-r1)^2
    Args:
        m1 (float): mass of first object (kg)
        m2 (float): mass of second object (kg)
        r1 (float): position of center of first object (m)
        r2 (float): position of center of second object (m)
    """
    r = r2 - r1
    r_unit_vector = r.normalize()
    if r.magnitude() == 0:
        raise ZeroDivisionError("Distance between two objects can't be 0")
    
    PRODUCT_OF_MASSES = m1 * m2
    DISTANCE_SQUARED = r.dot(r)
    F_G = game_constants.UNIVERSAL_GRAVITATIONAL_CONSTANT * PRODUCT_OF_MASSES / DISTANCE_SQUARED
    
    return F_G * r_unit_vector
