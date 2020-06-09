import numpy as np
import cv2
import random

class Pile:
    def __init__(self):
        self.screen=np.zeros((500, 500, 3))
        self.junks=random.choices(range(10, 40), k=50)

    def render_frame(self):
        self.screen = np.zeros((500, 500, 3))
        for pos, junk in enumerate(self.junks):
            self.screen[0:junk*10, pos*10:(pos+1)*10, :] = 255
        cv2.imshow("Simulation",self.screen)
        cv2.waitKey(10)

    def simulate_bubble(self):
        for iteration in range(len(self.junks) - 1):
            for pos in range(len(self.junks) - 1 - iteration):
                if self.junks[pos + 1] < self.junks[pos]:
                    self.junks[pos + 1], self.junks[pos] = self.junks[pos], self.junks[pos + 1]
                    self.render_frame()

    def show_junk(self):
        self.screen = np.zeros((500, 500, 3))
        for pos, junk in enumerate(self.junks):
            self.screen[0:junk * 10, pos * 10:(pos + 1) * 10, :] = 255
        cv2.imshow("Bubble Sort Simulation", self.screen)
        print(self.junks)
        cv2.waitKey()


Pile_of_junk=Pile()
Pile_of_junk.show_junk()
Pile_of_junk.simulate_bubble()
Pile_of_junk.show_junk()
cv2.destroyAllWindows()
