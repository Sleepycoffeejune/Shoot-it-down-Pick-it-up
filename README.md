# Shoot it down Pick it up

## Project Description

- Project by: W.W. 5913
- Game Genre: Shooter game

**Shoot it down Pick it up** is a simple 2D pixel shooting game where player take the role of a trash collector in a zombie-infested-town in the middle of nowhere.
The player can choose normal mode where they clean up the town and kill the zombie and progress the day as many as possoble, or the story mode where the player 
need to collect all 7 pages around the map in order to win the game and learn the story of this town.

## Requirements
- Python 3.9+
- Pygame

---

## Installation
To Clone this project:
```sh
git clone https://github.com/Sleepycoffeejune/Shoot-it-down-Pick-it-up.git
```

To create and run Python Environment for This project:

Window:
```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Mac:
```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Running Guide
After activate Python Environment of this project, you can process to run the game by:

Window:
```bat
python main.py
```

Mac:
```sh
python3 main.py
```

---

## Tutorial / Usage
## Controls

| KEY | ACTION        |
|-----|---------------|
| W   | Move forward  |
| A   | Move left     |
| S   | Move backward |
| D   | Move right    |
| G   | Gun toggle    |
| E   | Collect trash/zombies remain    |
| Space | Shoot        |
| Shift | Sprint      |
| Esc | Pause    |

How to play: 
- Normal Mode: 
  1. Walk around the map and collect the trash and zombie remain.
  2. Shoot down zombie in your path.
  3. Once the map is clean, go to bed to proceed into the next day.
  4. Your goal is to progress as many day as possible!
- Story mode:
  1. Walk around the map and collect the trash and zombie remain.
  2. Each day, there will be a page of paper you have to find and collect.
  3.  Shoot down zombie in your path, make sure they do not catch you or else you'd be stuck until you kill it.
  4.  Once the map is clean and the page is found, go to bed to proceed into the next day.
  5.  Your goal is to collect all 7 page in order to reach this mode ending.
- Game over:
  1. You HP reaches 0
  2. The infection rate reaches 100%

Tips:
1. You need your hands free to be able to collect the trash
2. The infection rate will increased depends on the amount of uncollected trash and the zombie you left alive from your previous game-day.
3. Make sure the zombies do not catch you or else you'd be stuck until you kill it.
4. Hold down shift while walking to sprint.


---

## Game Features
- **Animated Sprite** for the player and zombie walking animations.
- **Data-logging** every 5 seconds into CSV
- **Health Bars** over the player and zombies
- **Multiple Game Modes**, the normal mode and story mode

---

## Known Bugs
- A bug in story mode ending if the player collected 7 pages but the infection rates reached 100%
- The statistics graphs currently display all elapsed time data on a single x-axis.  
- Because I was unable to implement a scrollable x-axis, the graphs appear squished together when the dataset grows large (over 100 rows).  
- Attempts to make the x-axis scrollable caused the graph window to freeze. This happened because Matplotlib’s interactive window loop conflicted with the main Pygame loop, only one event loop could run at a time, so the graph could not update dynamically without blocking the game.
- In order to view each graph, the current graph window need to be close first before viewing the next one. 



---

## Unfinished Works
- No music nor sound effect installation.
- Story mode ending does not have the story implement into it yet.

---

## External sources
- Code refinement and debugging suggestions provided by Microsoft Copilot.

