# Snake Game

A simple Snake game built with Python and Pygame.

## How to run

1. Open a terminal in the project folder.
2. Create a virtual environment:

```powershell
python -m venv .venv
```

3. Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

4. Install the dependency:

```powershell
python -m pip install --upgrade pip
pip install pygame
```

5. Start the game:

```powershell
python snake_game.py
```

## Controls

- Arrow keys or WASD: move
- P: pause
- R: restart after game over
- Esc: quit

## Project files

- `snake_game.py` — game logic and rendering
- `.gitignore` — ignores the virtual environment and cache files

## Notes

This project intentionally does not track the `.venv` folder in Git. Others can recreate it by running the install steps above.
