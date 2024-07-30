from tkinter import Tk, BOTH, Canvas
import math
import time
import random
class Window:
    def __init__(self, width, height):
        self.root = Tk()
        self.root.title("Maze Solver")
        self.canvas = Canvas(self.root, bg="white", height=height, width=width)
        self.canvas.pack()
        self.window_running = False
        self.root.protocol("VM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.root.update()
        self.root.update_idletasks()

    def wait_for_close(self):
        self.window_running = True
        while(self.window_running):
            self.redraw()
           

        
    def close(self):
        self.window_running = False

    def draw_line(self, Line, fill_color):
        Line.draw(self.canvas, fill_color)

    def draw_dot(self, Line):
        Line.draw_dot(self.canvas)





class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, point1, point2):
        self.__point1 = point1
        self.__point2 = point2
    
    def draw(self, canvas, fill_color):
        canvas.create_line(self.__point1.x, self.__point1.y, self.__point2.x, self.__point2.y, fill=fill_color, width=2)


class Cell:
    def __init__(self, window=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._win = window
        self._visited = False

    def draw(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        p1 = Point(x1, y1)
        p2 = Point(x2, y1)
        line = Line(p1, p2)
        if self._win:
            self._win.draw_line(line,  "black" if self.has_top_wall else "white")
        
        p1 = Point(x1, y1)
        p2 = Point(x1, y2)
        line = Line(p1, p2)
        if self._win:
            self._win.draw_line(line, "black" if self.has_left_wall else "white")

        p1 = Point(x2, y1)
        p2 = Point(x2, y2)
        line = Line(p1, p2)
        if self._win:
            self._win.draw_line(line, "black" if self.has_right_wall else "white")

        p1 = Point(x1, y2)
        p2 = Point(x2, y2)
        line = Line(p1, p2)
        if self._win:
            self._win.draw_line(line, "black" if self.has_bottom_wall else "white")
    def draw_move(self, to_cell, undo=False):
        cur_x = math.floor(self.x1 + (self.x2 - self.x1)/2)
        cur_y = math.floor(self.y1 + (self.y2 - self.y1)/2)
        cur = Point(cur_x, cur_y)
        des_x = math.floor(to_cell.x1 + (to_cell.x2 - to_cell.x1)/2)
        des_y = math.floor(to_cell.y1 + (to_cell.y2 - to_cell.y1)/2)
        des = Point(des_x, des_y)
        line = Line(cur, des)
        if undo:
            if self._win:
                self._win.draw_line(line, "gray")
        else:
            if self._win:
                self._win.draw_line(line, "red")
        
    
dirs = {
    "left": (0, -1),
    "top": (-1, 0),
    "bottom": (1, 0),
    "right": (0, 1)
    }
dirs_ops = {
    (0, -1): "has_left_wall",
    (-1, 0): "has_top_wall",
    (1, 0): "has_bottom_wall",
    (0, 1): "has_right_wall"
        }
class Maze:
    def __init__(self, x1, y1, num_cols, num_rows, cell_size_x, cell_size_y, win=None, seed=None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._cells = []
        self._visited_cells = []
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._rest_cells_visited()
        if seed:
            random.seed(seed)
        else:
            random.seed()
    
    def _create_cells(self):
        for  i in range(0, self.num_cols):
            row_cells = []
            for j in range(0, self.num_rows):
                row_cells.append(Cell(self.win))
            self._cells.append(row_cells)
        for i in range(0, self.num_cols):
            for j in range(0, self.num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        cell = self._cells[i][j]
        cur_x1 = self.cell_size_x * j + self.x1
        cur_y1 = self.cell_size_y * i + self.y1
        cur_x2 = cur_x1 + self.cell_size_x
        cur_y2 = cur_y1 + self.cell_size_y
        # print(f"x1:{cur_x1}, y1: {cur_y1}, x2: {cur_x2}, y2: {cur_y2}")
        cell.draw(cur_x1, cur_y1, cur_x2, cur_y2)
        self._animate()
        return cell

    def _draw_line(self, i, j):
        cell = self._cells[i][j]
        cur_x1 = self.cell_size_x * j + self.x1
        cur_y1 = self.cell_size_y * i + self.y1
        cur_x2 = cur_x1 + self.cell_size_x
        cur_y2 = cur_y1 + self.cell_size_y
        cell.draw_point(cur_x1, cur_y1, cur_x2, cur_y2)


    def _animate(self):
        if self.win:
            self.win.redraw()
            time.sleep(0.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_left_wall = False
        self._draw_cell(0, 0)
        self._cells[self.num_cols - 1][self.num_rows - 1].has_right_wall = False
        self._draw_cell(self.num_cols - 1,  self.num_rows - 1)

    def _break_walls_r(self, i, j, count=0):
        count +=1 
        self._cells[i][j]._visited = True
        self._visited_cells.append((self._cells[i][j], (i, j)))
        possible_direction = []
        for dir in dirs: 
            new_i = i + dirs[dir][0]
            new_j = j + dirs[dir][1]
            if self._is_valid_dir(new_i, new_j) and self._cells[new_i][new_j]._visited == False:
                possible_direction.append((new_i, new_j))
        if i == self.num_cols -1 and j == self.num_rows - 1:
            self._draw_cell(i, j)
            return True
        if len(possible_direction) < 2:
            self._draw_cell(i, j)
            return False
        rand_pos = random.randrange(0, len(possible_direction))
        (end_i, end_j) = possible_direction[rand_pos]
        dir_from_start = dirs_ops[(end_i - i, end_j - j)]
        dir_from_end = dirs_ops[(i - end_i, j - end_j)]
        setattr(self._cells[i][j], dir_from_start, False)
        setattr(self._cells[end_i][end_j], dir_from_end, False)
        self._draw_cell(i, j)
        # if count  > 5:
        #     return
        result = self._break_walls_r(end_i, end_j, count)
        while result == False :
            temp_possible_direction = []
            if len(possible_direction) == 1:
                return False
            for index in range(0, len(possible_direction)):
                if index != rand_pos:
                    temp_possible_direction.append(possible_direction[index])
            possible_direction = temp_possible_direction
            rand_pos = random.randrange(0, len(possible_direction))
            (end_i, end_j) = possible_direction[rand_pos]
            dir_from_start = dirs_ops[(end_i - i, end_j - j)]
            dir_from_end = dirs_ops[(i - end_i, j - end_j)]
            setattr(self._cells[i][j], dir_from_start, False)
            setattr(self._cells[end_i][end_j], dir_from_end, False)
            self._draw_cell(i, j)
            result = self._break_walls_r(end_i, end_j, count)
    def _rest_cells_visited(self):
        for row in self._cells:
            for cell in row:
                cell._visited = False

    def solve(self):
        return self._solve_r(0, 0)
    def _solve_r(self, i , j):
        self._cells[i][j]._visited = True
        if i == self.num_cols -1 and j == self.num_rows - 1:
            return True
        possible_directions = []
        for dir in dirs:
            (add_i, add_j) = dirs[dir]
            new_i = i + add_i
            new_j = j +  add_j
            possible_to_go = getattr(self._cells[i][j], dirs_ops[(add_i, add_j)])
            if self._is_valid_dir(new_i, new_j) and self._cells[new_i][new_j]._visited == False and possible_to_go == False:
                possible_directions.append((new_i, new_j))

        for new_item in possible_directions:
            self._cells[i][j].draw_move(self._cells[new_item[0]][new_item[1]], False)
            self._animate()
            result = self._solve_r(new_item[0], new_item[1])
            self._animate()
            if result == True:
                return True
            self._cells[i][j].draw_move(self._cells[new_item[0]][new_item[1]], True)
        return False








    def _is_valid_dir(self, i ,j):
        if i < 0 or j < 0 or i >= len(self._cells) or j >= len(self._cells[0]): 
            return False
        return True
    
    def print_visited(self):
        print("visited cells info about wall")
        for item in self._visited_cells:
                if item[0]._visited:
                    print(f"cell: ({item[1][0]}, {item[1][1]}), top: {item[0].has_top_wall}, left: {item[0].has_left_wall}, right : {item[0].has_right_wall}, bottom: {item[0].has_bottom_wall}")

def main():
    win = Window(800, 600)
    # p1 = Point(10, 20)
    # p2 = Point(10, 200)
    # line = Line(p1, p2)
    # win.draw_line(line, "red")
    # p1 = Point(10, 10)
    # p2 = Point(50, 200)
    # line = Line(p1, p2)
    # win.draw_line(line, "blue")
    # cell1 = Cell(win)
    # cell1.draw(10, 10, 50, 50)
    # cell2 = Cell(win)
    # cell2.draw(50, 10, 100, 50)
    # cell1.draw_move(cell2, True)

    maze = Maze(10, 10, 10, 10, 40, 40, win, 0)
    print(maze.solve())
    win.wait_for_close()

if __name__ == "__main__":
    main()



