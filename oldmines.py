import bisect
import pyxel
import time

from utils import Box, Mines


class App:
    def __init__(self, debug: bool = False):
        pyxel.init(150, 180, title="OldMines")
        pyxel.mouse(True)
        self.m = Mines(9, 10)
        self.score = 200
        self.boxwidth = 10
        self.boxheight = 10
        self.debug = debug

        self.start_time = time.time()
        self.time_elapsed = 0
        self.mouse_pos_x = 0
        self.mouse_pos_y = 0
        self.scoreoffset = 15
        self.boxes = {}
        self.box_gap = 15
        self.box_xlim = []
        self.box_ylim = []
        for i in range(9):
            self.box_xlim.append(self.boxwidth + i * self.box_gap)
        for j in range(9):
            self.box_ylim.append(self.scoreoffset +
                                 self.boxheight + j * self.box_gap)
        for i in range(9):
            for j in range(9):
                self.boxes[(i, j)] = (
                    self.box_xlim[i],
                    self.box_ylim[j]
                )
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if self.m.playable:
            self.time_elapsed = int(time.time() - self.start_time)

            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT, hold=2, repeat=4):
                self.mouse_pos_x = pyxel.mouse_x
                self.mouse_pos_y = pyxel.mouse_y

                box_x = bisect.bisect_left(self.box_xlim, self.mouse_pos_x) - 1
                box_y = bisect.bisect_left(self.box_ylim, self.mouse_pos_y) - 1

                try:
                    if self.box_xlim[box_x] < self.mouse_pos_x < self.boxwidth + self.box_xlim[box_x]:
                        if self.box_ylim[box_y] < self.mouse_pos_y < self.boxheight + self.box_ylim[box_y]:
                            if self.debug:
                                print(box_x, box_y)
                except:
                    if self.debug:
                        print("clicked empty")

    def draw_box(self, x, y, col):
        pyxel.rect(x, y, self.boxwidth, self.boxheight, col)

    def draw_empty_box(self, x, y, col):
        pyxel.rect(x, y, self.boxwidth, self.boxheight, col)

    def draw(self):
        if self.m.playable:
            pyxel.cls(0)

            for box in self.boxes:
                self.draw_box(self.boxes[box][0], self.boxes[box][1], 7)

            # Draw score (using the template from example)
            s = f"TIME {self.time_elapsed:>4}"
            pyxel.text(10, 4, s, 1)
            pyxel.text(9, 4, s, 7)


App(debug=True)
