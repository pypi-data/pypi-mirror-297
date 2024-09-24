import random
import matplotlib.pyplot as plt
import numpy as np
import csv

class MazeGenerator:
    def __init__(self, width=None, height=None, seed=None):
        """
        Initializes the maze generator.

        Parameters:
        - width (int, optional): The width of the maze (must be odd).
        - height (int, optional): The height of the maze (must be odd).
        - seed (int, optional): A seed value for the random number generator.
        """
        self.maze = None
        self.width = None
        self.height = None
        self.start_pos = None
        self.end_pos = None
        self.seed = seed

        if seed is not None:
            random.seed(seed)

        if width is not None and height is not None:
            # Ensure width and height are odd numbers to maintain maze structure
            self.width = width if width % 2 == 1 else width + 1
            self.height = height if height % 2 == 1 else height + 1
            # Initialize the maze grid with walls (1s)
            self.maze = [[1 for _ in range(self.width)] for _ in range(self.height)]

    def generate_maze(self):
        if self.width is None or self.height is None:
            raise ValueError("Maze dimensions are not set.")

        # Start carving from a random odd coordinate
        start_x = random.randrange(1, self.width, 2)
        start_y = random.randrange(1, self.height, 2)

        # Begin the maze generation using iterative backtracking
        self._carve_path_iterative(start_x, start_y)

        # Define the entrance and exit positions
        self.start_pos = (0, 1)  # Entrance at the top
        self.end_pos = (self.height - 1, self.width - 2)  # Exit at the bottom

        # Carve out the entrance and exit in the maze grid
        self.maze[self.start_pos[0]][self.start_pos[1]] = 0
        self.maze[self.end_pos[0]][self.end_pos[1]] = 0

    def _carve_path_iterative(self, x, y):
        stack = []
        stack.append((x, y))
        self.maze[y][x] = 0  # Mark the starting cell as a path

        while stack:
            x, y = stack[-1]

            # Randomly order directions: up, right, down, left
            directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]
            random.shuffle(directions)

            found = False
            for dx, dy in directions:
                nx, ny = x + dx, y + dy

                if 1 <= nx < self.width - 1 and 1 <= ny < self.height - 1:
                    if self.maze[ny][nx] == 1:
                        # Carve a path between the current cell and the next cell
                        self.maze[y + dy // 2][x + dx // 2] = 0
                        self.maze[ny][nx] = 0
                        # Push the neighbor cell onto the stack
                        stack.append((nx, ny))
                        found = True
                        break  # Continue carving from the new cell

            if not found:
                # Backtrack to the previous cell
                stack.pop()

    def get_maze(self):
        return self.maze

    def set_maze(self, maze_array):
        """
        Sets the maze grid from a given array.

        Parameters:
        - maze_array (list of lists): The maze grid to set.
        """
        if not maze_array:
            raise ValueError("Provided maze array is empty.")

        self.maze = maze_array
        self.height = len(maze_array)
        self.width = len(maze_array[0])

        # Reset start and end positions
        self.start_pos = None
        self.end_pos = None

    def get_start_end_positions(self):
        return self.start_pos, self.end_pos

    def visualize_maze(self, save_path=None):
        """
        Visualizes the maze using Matplotlib.

        Parameters:
        - save_path (str, optional): The file path to save the visualization image.
        """
        if self.maze is None:
            raise ValueError("Maze grid is not set.")

        # Convert maze to a NumPy array for better handling with matplotlib
        maze_array = np.array(self.maze)

        # Create a color map: walls will be black, paths will be white
        cmap = plt.cm.binary  # 'binary' colormap: 0 is white, 1 is black

        # Create the plot
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.imshow(maze_array, cmap=cmap, interpolation='none')

        # Highlight the start and end positions if they are set
        if self.start_pos:
            ax.scatter(self.start_pos[1], self.start_pos[0], c='green', s=100, label='Start')
        if self.end_pos:
            ax.scatter(self.end_pos[1], self.end_pos[0], c='red', s=100, label='End')

        # Remove the axes for clarity
        ax.axis('off')

        # Add a legend for the start and end points if they are set
        if self.start_pos or self.end_pos:
            ax.legend(loc='upper right')

        # Save the visualization if a path is provided
        if save_path:
            plt.savefig(save_path, bbox_inches='tight', pad_inches=0)
            print(f"Maze visualization saved to {save_path}")

        # Display the plot
        plt.show()

    def save_maze_as_csv(self, file_path):
        """
        Saves the maze grid to a CSV file.

        Parameters:
        - file_path (str): The file path to save the maze data.
        """
        if self.maze is None:
            raise ValueError("Maze grid is not set.")

        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in self.maze:
                writer.writerow(row)
        print(f"Maze data saved to {file_path}")

    def load_maze_from_csv(self, file_path):
        """
        Loads the maze grid from a CSV file.

        Parameters:
        - file_path (str): The file path to load the maze data from.
        """
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            maze_array = []
            for row in reader:
                maze_array.append([int(cell) for cell in row])

        self.set_maze(maze_array)
        print(f"Maze data loaded from {file_path}")

    def save_maze_as_text(self, file_path):
        """
        Saves the maze grid to a text file.

        Parameters:
        - file_path (str): The file path to save the maze data.
        """
        if self.maze is None:
            raise ValueError("Maze grid is not set.")

        with open(file_path, 'w') as f:
            for row in self.maze:
                f.write(''.join(str(cell) for cell in row) + '\n')
        print(f"Maze data saved to {file_path}")

    def load_maze_from_text(self, file_path):
        """
        Loads the maze grid from a text file.

        Parameters:
        - file_path (str): The file path to load the maze data from.
        """
        with open(file_path, 'r') as f:
            maze_array = [[int(cell) for cell in line.strip()] for line in f]
        self.set_maze(maze_array)
        print(f"Maze data loaded from {file_path}")