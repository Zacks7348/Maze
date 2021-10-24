# Maze
This project was developed to visualize the process of different maze generation and
search algorithms. This project is built with Python 3.8 and Tkinter.

## Getting Started

### Requirements
* Python 3.8+

### Installation and Use
To use the maze program, clone it to your system using the following command
``` bash
git clone https://github.com/Zacks7348/Maze.git
```

Once you have the project downloaded you can launch the program by running 
the maze_app.py file.

The project GUI is really simple to use. To generate a maze you can click on 
the "Generate" ribbon button, where you will be prompted to input different parameters 
like heigh, width, and method. Right now this project only implements Randomized
Depth-First Search and Randomized Prim's Algorithm. 

You can also run different search algorithms by clicking on the "Solve" ribbon button. 
Like the generate button, you will be prompted to choose which search algorithm to use to 
solve the maze. Right now this project implements Depth-First, Breadth-First, Uniform-Cost, 
and A* search algorithms.

## Table of Contents
**[Maze Implementation](#maze-implementation)**<br>

**[Maze Generation](#maze-generation)**<br>
* **[Randomized Depth-First Search](#randomized-depth-first-search)**<br>
* **[Randomized Prim's Algorithm](#randomized-prim's-algorithm)**<br>

**[Maze Solving](#maze-solving)**<br>
* **[Depth-First Search](#depth-first-search)**<br>
* **[Breadth-First Search](#breadth-first-search)**<br>
* **[Uniform-Cost Search](#uniform-cost-search)**<br>
* **[A* Search](#a*-search)**<br>

**[TODO][#todo]**<br>

## Maze Implementation
At its core, a maze is simply a n-dimensional list of cells, usually a 2D 
list, of walls and passages. However, there are two main ways walls are implemented:
1. Each cell is either a passage or wall
2. The borders between adjacent cells represent walls

In this project I implement the maze as a 2D Python list where each cell is either a 
passage or wall. Cells are denoted by its row and column in the 2D list and store an 
Enum value from the CellType class, which looks like this:
``` Python
class CellType(Enum):
    WALL = 0
    PASSAGE = 1
    START = 2
    FINISH = 3
```

For ease of use, cells in the maze can be accessed with a Cell object that stores
the row and column information. This Cell object is implemented as a 
[namedtuple][namedtuple]

The 2D array is neatly wrapped inside of a Maze class, which provides many utility 
functions for interacting with the maze. One important function in this class is
the get_neighboring_cells(c) function, which returns a list of all the cells 
adjacent to cell c. Since search algorithms work with graph-like structures, we can
treat cells as graph nodes where instead of storing children cells in the Cell object 
itself, the children can accessed through this function. You can look at the
Maze class [here][maze/maze.py] to learn more.

## Maze Generation
The following are quick summaries of the implemented maze generation algorithms.
Each algorithm will generate a perfect maze, which is a maze where there is only
1 path between any two cells.

### Randomized Depth-First Search
For maze generation, we use a randomized verision of DFS 
called [Randomized Depth-First Search (RDFS)][rdfs]. The maze is initialized as
all walls and starts at a randomnly selected cell. 

In the same fashion as DFS, the algorithm chooses a random neighboring wall to turn 
into a passage and adds the cell to the stack. If there are no neighboring walls,
then the algorithm backtracks until a cell is popped with available space or the
stack is empty.

This algorithm is biased towards long passages, which results in mazes with long
corridors instead of many branches.

### Randomized Prim's Algorithm
[Randomized Prim's Algorithm][rpa] starts of with a maze of all walls and randomly
selects a starting point like RDFS. The walls of the starting point are added to a
list and the algorithm continues while this list is not empty.

A wall is randomly popped from the list and converted to a passage if it is between
a passage and another wall. The neighboring walls of the wall that was popped from
the list are added to the list.

## Maze Solving
The following are quick summaries of the implemented search algorithms used to solve 
mazes. Essentially the algorithms all work as follows:
1. Start at the starting cell of the maze
2. Traverse the maze until the finish is found or all cells have been traversed
3. If the finish was found, perform [backtracking][backtracking] to determine the path 
found.

### Depth-First Search
[Depth-First Search (DFS)][dfs] starts at the root node (or the start
cell of the maze in this case) and explores as far as possible along each path 
before [backtracking][backtracking]. 

This algorithm uses a stack to keep track of all the possible cells it can traverse
to. While there are cells in the stack the algorithm will pop off a cell, mark it as 
visited, and add it's adjacent passage cells to the stack. 

### Breadth-First Search
[Breadth-First Search (BFS)][bfs] starts at the root node (or the start cell 
of the maze in this case) and explores all cells at the current depth prior to
moving on to the next level of nodes.

This algorithm uses a FIFO queue to keep track of all the possible cells it can 
traverse to. While the queue is not empty the algorithm removes a cell from
the queue and adds its neighbors back to the queue. 

### Uniform-Cost Search
[Uniform-Cost Search (UCS)][ucs] starts at the starting cell of the maze and
traverses to the cell with the cheapest cost.

This algorithm works similarly to BFS but uses a Priority Queue instead, where 
the priority of a cell is the cost of travelling to that cell from the starting
cell. Since the cost of travelling from a cell to an adjacent cell is always 1
in a maze, this algorithm behaves similarly to BFS.

### A* Search
[A* Search][astar] works the same as UCS but uses a [heuristic][heuristic] on top 
of the travel cost between cells. There are two different heuristic methods 
implemented in this project:
* Euclidian
* Manhattan

The heuristic allows for this algorithm to traverse through cells in the general 
direction of the finish cell.

## TODO
* Add Images and GIFS to the README
* Add option to choose heuristic for A* Search Algorithm in GUI
* Implemented more algorithms:
* * Randomized Kruskals Algorithm
* * Wilson's Algorithm
* * Aldous-Broder Algorithm

<!-- References -->
[rdfs]: https://en.wikipedia.org/wiki/Maze_generation_algorithm
[rpa]: https://en.wikipedia.org/wiki/Maze_generation_algorithm
[dfs]: https://en.wikipedia.org/wiki/Depth-first_search
[bfs]: https://en.wikipedia.org/wiki/Breadth-first_search
[ucs]: https://www.educative.io/edpresso/what-is-uniform-cost-search
[astar]: https://en.wikipedia.org/wiki/A*_search_algorithm
[backtracking]: https://en.wikipedia.org/wiki/Backtracking#:~:text=Backtracking%20is%20a%20general%20algorithm,completed%20to%20a%20valid%20solution.
[namedtuple]: https://docs.python.org/3/library/collections.html#collections.namedtuple
[heuristic]: https://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html#:~:text=For%20example%2C%20if%20most%20of,not%20have%20to%20be%20global.