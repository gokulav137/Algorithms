import numpy as np
import cv2


class Grid:

    def __init__(self, h, w):
        self.h = h
        self.w = w
        self.grid = np.ones((h, w, 6)) * -1
        self.grid[:, :, 2] = 0
        self.starting_point = [-1, -1]
        self.end_point = [-1, -1]
        self.map_grid_2_screen(25)
        self.make_grid()

    def make_grid(self):
        print("Select a starting point using left mouse click and press Enter")
        cv2.setMouseCallback("Path_finding", self.get_start_point)
        cv2.waitKey(0)
        print("\nSelect a ending point using left mouse click and press Enter")
        cv2.setMouseCallback("Path_finding", self.get_end_point)
        cv2.waitKey(0)
        print(
            "\nDraw the maze using left mouse click and erase using right mouse click , click and drag is supported "
            ".Press Enter after drawing")
        cv2.setMouseCallback("Path_finding", self.add_wall_points)
        cv2.waitKey(0)
        cv2.setMouseCallback("Path_finding", self.stop_callback)

    def add_wall_points(self, event, x, y, flags, params):
        try:
            if event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON or event == cv2.EVENT_LBUTTONDOWN:
                if [int(x / 25), int(y / 25)] != self.starting_point and [int(x / 25), int(y / 25)] != self.end_point:
                    self.grid[int(x / 25), int(y / 25), 0] = 0
                    self.map_grid_2_screen(25)
        except IndexError:
            pass
        try:
            if event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_RBUTTON or event == cv2.EVENT_RBUTTONDOWN:
                if [int(x / 25), int(y / 25)] != self.starting_point and [int(x / 25), int(y / 25)] != self.end_point:
                    self.grid[int(x / 25), int(y / 25), 0] = -1
                    self.map_grid_2_screen(25)
        except IndexError:
            pass

    def get_start_point(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.starting_point = [int(x / 25), int(y / 25)]
            self.map_grid_2_screen(25)
            print(self.starting_point, "Starting Point Set")

    def get_end_point(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            if [int(x / 25), int(y / 25)] != self.starting_point:
                self.end_point = [int(x / 25), int(y / 25)]
                self.map_grid_2_screen(25)
                print(self.end_point, "Ending Point Set")

    def stop_callback(self, event, x, y, flags, params):
        pass

    def solve_grid(self, simulate):
        best = self.starting_point
        cell_pos = np.array([best[0], best[1]])
        check_list = []
        self.grid[best[0], best[1], 1] = self.score_cell(cell_pos)
        self.get_check_list(best, check_list)
        while best != self.end_point and check_list != []:
            best = self.get_best_cell(check_list)
            self.get_check_list(best, check_list)
            if simulate:
                self.show_grid()
        if best == self.end_point:
            screen = self.map_grid_2_screen(25)
            self.get_best_path(self.end_point, screen, 25)
            cv2.imshow("Path_finding", screen)
        else:
            print("Path Doesnot Exist")
        cv2.waitKey(0)
        self.grid[:, :, 1:] = -1
        self.grid[:, :, 2] = 0

    def get_best_path(self, current_point, screen, k):
        screen[int(current_point[1] * k):int((current_point[1] + 1) * k) - 1,
               int(current_point[0] * k):int((current_point[0] + 1) * k) - 1, 0:2] = 255
        if self.grid[int(current_point[0]), int(current_point[1]), 4] != self.starting_point[0] or \
                self.grid[int(current_point[0]), int(current_point[1]), 5] != self.starting_point[1]:
            self.get_best_path(self.grid[int(current_point[0]), int(current_point[1]), 4:], screen, k)

    def show_grid(self):
        self.map_grid_2_screen(25)
        cv2.waitKey(20)

    def map_grid_2_screen(self, k):
        screen = np.zeros((self.h * k, self.w * k, 3))
        for row in range(self.h):
            for col in range(self.w):
                if self.grid[col, row, 3] == 0:
                    screen[int(row * k):int((row + 1) * k) - 1, int(col * k):int((col + 1) * k) - 1, 0] = 255
                elif self.grid[col, row, 1] != -1:
                    screen[int(row * k):int((row + 1) * k) - 1, int(col * k):int((col + 1) * k) - 1, 1] = 255
                elif self.grid[col, row, 0] != -1:
                    screen[int(row * k):int((row + 1) * k) - 1, int(col * k):int((col + 1) * k) - 1, 2] = 255
                if [col, row] == self.starting_point or [col, row] == self.end_point:
                    screen[int(row * k):int((row + 1) * k) - 1, int(col * k):int((col + 1) * k) - 1, :] = 255
        cv2.imshow("Path_finding", screen)
        return screen

    def score_cell(self, cell_pos):
        return self.grid[cell_pos[0], cell_pos[1], 2] + np.sum(np.absolute(cell_pos - self.end_point))

    def get_check_list(self, best_cell, check_list):
        least_step = self.grid[best_cell[0], best_cell[1], 2]
        self.grid[best_cell[0], best_cell[1], 3] = 0
        for new_cell in [[best_cell[0] + 1, best_cell[1]], [best_cell[0], best_cell[1] + 1],
                         [best_cell[0], best_cell[1] - 1], [best_cell[0] - 1, best_cell[1]]]:
            try:
                if new_cell[0] >= 0 and new_cell[1] >= 0:
                    if (self.grid[new_cell[0], new_cell[1], 1] != 0 and self.grid[new_cell[0], new_cell[1], 3] != 0 and
                            self.grid[new_cell[0], new_cell[1], 0] != 0):
                        if self.grid[new_cell[0], new_cell[1], 1] == -1:
                            self.grid[new_cell[0], new_cell[1], 2] = least_step + 1
                            cell_pos = np.array([new_cell[0], new_cell[1]])
                            self.grid[new_cell[0], new_cell[1], 1] = self.score_cell(cell_pos)
                            self.grid[new_cell[0], new_cell[1], 4:] = best_cell
                            check_list.append(new_cell)
                        elif self.grid[new_cell[0], new_cell[1], 2] >= least_step + 1:
                            self.grid[new_cell[0], new_cell[1], 2] = least_step + 1
                            cell_pos = np.array([new_cell[0], new_cell[1]])
                            self.grid[new_cell[0], new_cell[1], 1] = self.score_cell(cell_pos)
                            self.grid[new_cell[0], new_cell[1], 4:] = best_cell
            except IndexError:
                pass
    def get_best_cell(self, check_list):
        cell = check_list[0]
        least_score = self.grid[cell[0], cell[1], 1]
        most_walk = 0
        best_cell = check_list[0]
        for cell in check_list:
            if least_score >= self.grid[cell[0], cell[1], 1]:
                if least_score == self.grid[cell[0], cell[1], 1] and most_walk > self.grid[cell[0], cell[1], 2]:
                    pass
                else:
                    best_cell = cell
                    most_walk = self.grid[cell[0], cell[1], 2]
                    least_score = self.grid[cell[0], cell[1], 1]
        check_list.remove(best_cell)
        return best_cell


Simulation = Grid(30, 30)
print("\nSimulating A* algorithm")
Simulation.solve_grid(simulate=True)
cv2.destroyAllWindows()
print("\nA* algorithm Without simulation")
Simulation.show_grid()
print("\nPress Enter to Run Algorithm")
cv2.waitKey(0)
Simulation.solve_grid(simulate=False)
cv2.destroyAllWindows()
