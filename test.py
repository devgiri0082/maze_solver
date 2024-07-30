import unittest
from main import Maze
class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 10
        num_rows = 12
        m1 = Maze(0, 0, num_cols,num_rows, 10, 10)
        print(len(m1._cells))
        self.assertEqual(len(m1._cells), num_cols)
        self.assertEqual(len(m1._cells[0]), num_rows)

    def test_maze_entrance_exit(self):
        num_cols = 10
        num_rows = 12
        m1 = Maze(0, 0, num_cols,num_rows, 10, 10)
        self.assertEqual(m1._cells[0][0].has_left_wall, False)
        self.assertEqual(m1._cells[-1][-1].has_right_wall, False)
    
    def test_break_wall(self):
        Maze(0, 0, 10, 10, 40, 40)

    def test_visitted_status(self):
        maze = Maze(0, 0, 10, 10, 40, 40)
        for row in maze._cells:
            for cell in  row:
                self.assertEqual(cell._visited, False)
    
    def test_maze_solve(self):
        maze = Maze(0, 0, 10, 10, 40, 40)
        maze.solve()
         


if __name__ == "__main__":
    unittest.main()

