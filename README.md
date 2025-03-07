
# Olive's Peculiar Dream

A fun 2D platformer game created with Pygame featuring a cat on a quest to collect kibble and find a special toy.

## Game Overview

In "Olive's Peculiar Dream," you control a cat character who must navigate platforms, collect kibble, and find a special toy near the end of the level.

## Game Controls

- **Left Arrow Key**: Move left
- **Right Arrow Key**: Move right  
- **Space**: Jump
- **Mouse Click**: Toggle the digital rain effect (click the "Rain" button in the top-left corner)

## Game Elements

- **Kibble**: Collect these golden treats for points
- **Platforms**: Jump on these to navigate upward
- **Mouse Toy**: Reach this at the top of the level to complete the game
- **Digital Rain Effect**: Toggle this feature on/off for a different visual experience

## Project Organization

The code is organized into these main directories:
- `Game/` - Contains the main game code
- `Game/Assets/` - Contains all game assets and asset loading code
- `run_game.py` - The main entry point to run the game

## How to Run the Game

### Local

1. Download the game files:
   - Go to [https://github.com/artisticmedic/olive-peculiar-dream](https://github.com/artisticmedic/olive-peculiar-dream)
   - Click the green "Code" button
   - Click "Download ZIP"
   - Find the downloaded file on your computer and unzip it:
     - On Windows: Right-click the ZIP file and select "Extract All"
     - On Mac: Double-click the ZIP file

2. Install Python:
   - Go to [https://www.python.org/downloads/](https://www.python.org/downloads/)
   - Download Python 3.10 or newer
   - Open the downloaded folder, and open the file named "Install Certificates.command"
   - IMPORTANT: On Windows, check "Add Python to PATH" during installation

3. Install Pygame:
   - Open a command window:
     - On Windows: Press Win+R, type "cmd" and press Enter
     - On Mac: Open Spotlight (Cmd+Space), type "terminal" and press Enter
   - Type this command and press Enter:
     ```
     pip install pygame
     ```
     If these returns an error, try running:
     ```
     pip3 install pygame
     ```

4. Prep the game:
   - Navigate to the game folder in your command window by...
      - Right clicking the unzipped game folder
      - While the menu is open, hold down the opt key, and select the "Copy olives-peculiar-dreamm as pathname" option
      - In Terminal, type cd and then paste the path name and enter.
        ```
        cd the-pasted-path-name
        ```
5. Run the game by typing:
     ```
     python run_game.py
     ```
     If you installed using pip3, you will need to use python3 instead of python

## Game Objective

Navigate your cat character through the platforms, collect all the kibble, and find a special toy near the end of the level!

## Development Notes

This game was developed using:
- Python 3.10+
- Pygame 2.1.2

Enjoy the game!
