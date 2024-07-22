import random


class Box:
    value: int
    isopen: bool
    isflagged: bool

    def __init__(self, value: int, isopen: bool = False, isflagged: bool = False):
        self.value = value
        self.isopen = isopen
        self.isflagged = isflagged

    def __repr__(self) -> str:
        return f"Box({self.value}, {self.isopen})"

    def __eq__(self, other) -> bool:
        if isinstance(other, int):
            return self.value == other
        else:
            return self.value == other.value

    def __str__(self) -> str:
        if self.isopen:
            return f"[{self.value}]"
        if self.isflagged:
            return f"[F]"
        else:
            return f"[X]"


class Mines:
    ndim: int
    nmines: int
    flags_available: int
    playable: bool
    haswon: bool
    boxes_left_to_open: int
    layout: dict[tuple[int, int], Box]
    _neighbors = {(1, 0), (-1, 0), (0, 1), (0, -1),
                  (1, 1), (-1, -1), (1, -1), (-1, 1)}

    def __init__(self, ndim: int, nmines: int) -> None:
        self.ndim = ndim
        self.nmines = nmines
        self.flags_available = nmines
        self.playable = True
        self.haswon = False
        self.boxes_left_to_open = ndim**2
        self.layout = self._generate_layout()

    def _generate_layout(self) -> dict[tuple[int, int], Box]:
        layout = {(i, j): Box(0) for i in range(self.ndim)
                  for j in range(self.ndim)}
        mines = random.sample(list(layout.keys()), k=self.nmines)
        for mine in mines:
            layout[mine] = Box(9)

        for loc in layout:
            if layout[loc] == 9:
                continue

            num_neighbor_mines = 0
            for neighbor in self._neighbors:
                neighbor_loc = (loc[0]+neighbor[0], loc[1]+neighbor[1])
                if neighbor_loc in layout:
                    if layout[neighbor_loc] == 9:
                        num_neighbor_mines += 1

            if num_neighbor_mines > 0:
                layout[loc] = Box(num_neighbor_mines)

        return layout

    def _open(self, loc) -> None:
        if self.layout[loc].isopen:
            return

        self.layout[loc].isopen = True
        self.boxes_left_to_open -= 1

        if self.layout[loc] == 9:
            self.playable = False
            for loc in self.layout:
                self.layout[loc].isopen = True
            return

        if self.layout[loc].isflagged:
            self.layout[loc].isflagged = False
            self.flags_available += 1

        if self.layout[loc] == 0:
            for neighbor in self._neighbors:
                neighbor_loc = (loc[0]+neighbor[0], loc[1]+neighbor[1])
                if neighbor_loc in self.layout:
                    self._open(neighbor_loc)

        if self.boxes_left_to_open == self.nmines:
            self.playable = False
            self.haswon = True

    def click(self, loc: tuple[int, int]) -> int:
        if (not self.playable) or (loc not in self.layout):
            return -1
        elif self.layout[loc].isopen or self.layout[loc].isflagged:
            return 0
        else:
            self._open(loc)
            return 1

    def flag(self, loc: tuple[int, int]) -> int:
        if (not self.playable) or (loc not in self.layout):
            return -1
        elif self.layout[loc].isopen or not self.flags_available:
            return 0
        else:
            if self.layout[loc].isflagged:
                self.layout[loc].isflagged = False
                self.flags_available += 1
            else:
                self.layout[loc].isflagged = True
                self.flags_available -= 1
            return 1

    def get_layout(self) -> dict[tuple[int, int], Box]:
        return self.layout

    def __repr__(self) -> str:
        return f"Mines({self.ndim}, {self.nmines}, {self.flags_available}, {self.playable}, {self.haswon})"

    def __str__(self) -> str:
        _return_str = ""
        for i in range(self.ndim):
            for j in range(self.ndim):
                _return_str += str(self.layout[(i, j)])
            _return_str += "\n"

        return _return_str
