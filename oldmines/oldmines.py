import bisect
import pyxel
import time

from utils import Box, Mines


class App:
    def __init__(self, debug: bool = False):
        pyxel.init(150, 180, title="Oldmines")
        pyxel.mouse(True)
        self.debug = debug
        self.scoreoffset = 15
        self.boxwidth = 10
        self.boxheight = 10
        self._symbolmap = {s: str(s) for s in range(1, 9)}
        self._symbolmap[0] = ""
        self._symbolmap[9] = "*"
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
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self):
        self.m = Mines(9, 10)
        self.start_time = time.time()
        self.time_elapsed = 0
        self.mouse_pos_x = 0
        self.mouse_pos_y = 0

    def clickhandler(self):
        self.mouse_pos_x = pyxel.mouse_x
        self.mouse_pos_y = pyxel.mouse_y

        box_x = bisect.bisect_left(self.box_xlim, self.mouse_pos_x) - 1
        box_y = bisect.bisect_left(self.box_ylim, self.mouse_pos_y) - 1

        if self.box_xlim[box_x] < self.mouse_pos_x < self.boxwidth + self.box_xlim[box_x]:
            if self.box_ylim[box_y] < self.mouse_pos_y < self.boxheight + self.box_ylim[box_y]:
                return box_x, box_y

        return None, None

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_R):
            self.reset()

        if self.m.playable:
            self.time_elapsed = int(time.time() - self.start_time)

            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT, hold=5, repeat=1):
                box_x, box_y = self.clickhandler()
                if box_x is not None:
                    self.m.click((box_x, box_y))
                    if self.debug:
                        print("leftclick", box_x, box_y)

            if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT, hold=5, repeat=1):
                box_x, box_y = self.clickhandler()
                if box_x is not None:
                    self.m.flag((box_x, box_y))
                    if self.debug:
                        print("rightclick", box_x, box_y)

    def draw_box(self, x, y, col):
        pyxel.rect(x, y, self.boxwidth, self.boxheight, col)

    def draw_empty_box(self, x, y, col):
        pyxel.rectb(x, y, self.boxwidth, self.boxheight, col)

    def draw(self):
        pyxel.cls(0)
        for box in self.boxes:
            if self.m.get_layout()[(box[0], box[1])].isopen:
                self.draw_empty_box(
                    self.boxes[box][0], self.boxes[box][1], 7 if not self.m.haswon else 10)

                if self.m.get_layout()[(box[0], box[1])].value > 0:
                    pyxel.text(self.boxes[box][0] + self.boxwidth/2.5, self.boxes[box][1] + self.boxheight/3, self._symbolmap[self.m.get_layout()[
                        (box[0], box[1])].value], self.m.get_layout()[(box[0], box[1])].value+1)
            elif self.m.get_layout()[(box[0], box[1])].isflagged:
                self.draw_empty_box(
                    self.boxes[box][0], self.boxes[box][1], 7)
                pyxel.text(self.boxes[box][0] + self.boxwidth/2.5, self.boxes[box][1] + self.boxheight/3,
                           "F", 9)
            else:
                self.draw_box(self.boxes[box][0], self.boxes[box][1], 7)

        if self.m.haswon:
            f = f"YAY!"
            pyxel.text(10, 4, f, 1)
            pyxel.text(9, 4, f, 10)
        else:
            f = f"FLAG {self.m.flags_available:>4}"
            pyxel.text(10, 4, f, 1)
            pyxel.text(9, 4, f, 7)

        s = f"TIME {self.time_elapsed:>4}"
        pyxel.text(100, 4, s, 1)
        pyxel.text(99, 4, s, 7)

        if not self.m.playable:
            msg = "Press R to reset."
            pyxel.text(10, 170, msg, pyxel.frame_count % 20)


App()
