## Ben Carroll's CYOA Game

### TODO list

- ~~Scan enemies in from the maze, similar to keys, etc.~~
  - Done!
  - When a new maze is loaded in, enemies are also loaded in from the maze, and added to the list of enemies with their co-ordinates
  - Their positions on the maze are then cleared.
  - Around lines 140-149 in `main.py`


- ~~Make a tutorial page to explain mechanics of game~~
  - Done!
  - Tutorial maze is played as the first maze, and from then on random mazes are selected.
  - Tutorial maze includes instructions on how to move, how gates and enemies work, etc.
  - Integrated all through `main.py`
  - Around lines 4-26 in `mazes.py`
