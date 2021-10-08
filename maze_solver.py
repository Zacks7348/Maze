import argparse

from maze.maze import Maze, Position
from maze.search_algorithms import solve_maze


def setup_argparser():
    parser = argparse.ArgumentParser(
        description='A Python 3.8+ library for solving mazes')
    parser.add_argument(
        'maze', type=str, help='The text file that stores the maze to solve')
    parser.add_argument('-method', type=str, help='Search algorithm to use')
    parser.add_argument('-heuristic', type=str,
                        help='Heuristic to use with search algorithm')
    #parser.add_argument('-d', '-direction', action='store_true', help='Output path as list of directions')
    return parser


def main():
    parser = setup_argparser()
    args = parser.parse_args()
    maze = Maze.from_file(args.maze)
    solve_maze(maze, method=args.method, heuristic=args.heuristic)


if __name__ == '__main__':
    main()
