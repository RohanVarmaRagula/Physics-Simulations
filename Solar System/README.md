# Solar System Simulation

A 2D solar-system simulation built with Python and Pygame. It models gravity between the Sun and planets, displays orbital traces, and lets you zoom and pan around the scene.

## Requirements

- Python 3.9 or later
- Pygame

Install Pygame:

```powershell
python -m pip install pygame
```

## Run

From the project directory, run:

```powershell
python main.py
```

Run it from the project directory so the relative paths to `assets/` resolve correctly. The simulation opens fullscreen; press **Esc** to exit.

## Controls

- **Mouse wheel:** Zoom in or out
- **Left mouse button + drag:** Pan the view
- **Esc:** Exit

## Project structure

```text
assets/
  background.jpg
  sun.jpg
  planets/             Planet images
celestial_body.py      Celestial body model and rendering
game_constants.py      Simulation, display, and zoom settings
main.py                Pygame application loop and input handling
physics.py             Gravity and motion calculations
```

## Simulation notes

Positions, velocities, masses, and gravitational calculations use SI units. The simulation advances faster than real time; adjust `SIMULATION_TIME_SCALE` in `game_constants.py` to change the rate. Gravity is calculated for the Sun and planets, and each frame updates the planets using a semi-implicit Euler step. This is a learning/visualization simulation, not a precision ephemeris; large time steps can cause orbital drift.
