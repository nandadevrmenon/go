# Go Game using Python and PyQt

## Overview

This project is a Go board game developed using Python and PyQt, featuring both Normal and Speed Go modes. The game includes a sleek dark-themed interface with intuitive design elements, animations for smoother user interaction, and meaningful feedback mechanisms to enhance the overall experience. The game flow is user-driven, allowing control over resigning, passing, and undoing/redoing moves.

## Features

- **Two Game Modes**: 
  - **Normal Mode**: Traditional Go gameplay.
  - **Speed Go Mode**: Each player has a total of 2 minutes to play.
  
- **Game Controls**:
  - Undo/Redo moves (with restrictions in Speed Go mode).
  - Pass, resign, and pause options.
  
- **Animations**:
  - Pieces placed on the board are animated.
  - Invalid moves show visual feedback with a red flash.
  - Captured pieces fade out.
  
- **Game End**:
  - The game ends after two consecutive passes, or if a player resigns.
  - A winner dialog box is displayed with the final score.

- **Keyboard Shortcuts**: Designed for ease of use, with shortcuts tied to the actions' initial letters. Irreversible actions require two-key combinations.

## Installation

1. Clone this repository.
2. Ensure you have `PyQt5` installed.
    ```bash
    pip install pyqt5
    ```
3. Run the game by executing the main Python script:
    ```bash
    python main.py
    ```

## Instructions

1. Start the game by entering player names and choosing the desired game mode on the Start Screen.
2. Play Go with the rules and interface provided, including undo, redo, and reset options.
3. The game ends upon resignation or two consecutive passes, after which the winner is displayed.

## Screenshots
- Start Screen: ![Start Screen](/images/startscreenSS.png)
- Game Board: ![Game Board](/images/gameplaySS.png)
