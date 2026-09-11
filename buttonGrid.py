from colors import Colors


class ButtonGrid:
    def __init__(self):
        self.length = 3
        self.__grid = [Colors.GRAY]*9

    def __str__(self):
        return str(self.__grid)

    def get_color(self, pos: tuple[int, int]):
        if pos[0] > self.length or pos[0] < 0:
            raise IndexError(f"X value ({pos[0]}) is out of range")
        if pos[1] > self.length or pos[1] < 0:
            raise IndexError(f"Y value ({pos[1]}) is out of range")


        index = pos[0] + pos[1]*self.length
        return self.__grid[index]

    def set_color(self, pos: tuple[int, int], color: Colors):
        index = pos[0] + pos[1]*self.length
        self.__grid[index] = color

    def get_grid(self) -> list[Colors]:
        return list(self.__grid)

    def set_grid(self, grid: list[Colors]):
        self.__grid = list(grid)


    def press(self, pos: tuple[int, int]):
        def swap(pos1, pos2):
            c1 = self.get_color(pos1)
            c2 = self.get_color(pos2)

            self.set_color(pos1, c2)
            self.set_color(pos2, c1)

        def addVectors(pos1: tuple[int, int], pos2: tuple[int, int]):
            return (pos1[0] + pos2[0], pos1[1] + pos2[1])

        def isInRange(n: int, min: int, max: int) -> bool:
            return min <= n and n <= max


        def gray():
            pass # does nothing.

        def black():
            row = pos[1]

            swap((0, row), (2, row))
            swap((1, row), (2, row))

        def yellow():
            if pos[1] == 0: return

            posAbove = (pos[0], pos[1] - 1)
            swap(pos, posAbove)

        def violet():
            if pos[1] == 2: return

            posBelow = (pos[0], pos[1] + 1)
            swap(pos, posBelow)

        def green():
            invertedPos = list(pos)
            if pos[0] == 0: invertedPos[0] = 2
            if pos[0] == 2: invertedPos[0] = 0
            if pos[1] == 0: invertedPos[1] = 2
            if pos[1] == 2: invertedPos[1] = 0

            swap(pos, tuple(invertedPos))

        def pink():
            rotationPath = (
                (-1, -1),
                (0, -1),
                (1, -1),
                (1, 0),
                (1, 1),
                (0, 1),
                (-1, 1),
                (-1, 0)
            )
            filteredPath = []

            # remove invalid positions (will naturally wrap around).
            for offset in rotationPath:
                sum = addVectors(pos, offset)
                if not isInRange(sum[0], 0, 2):
                    continue
                if not isInRange(sum[1], 0, 2):
                    continue

                filteredPath.append(offset)

            # the logic here is a bit unintuitive,
            # rework it if necessary.
            c1 = addVectors(pos, filteredPath[0])
            for i in range(1, len(filteredPath)):
                ci = addVectors(pos, filteredPath[i])
                swap(c1, ci)

        def red():
            for y in range(self.length):
                for x in range(self.length):
                    button = self.get_color((x, y))
                    if button == Colors.WHITE:
                        self.set_color((x, y), Colors.BLACK)
                    elif button == Colors.BLACK:
                        self.set_color((x, y), Colors.RED)

        def orange():
            neighbors = (
                (0, -1),
                (0, 1),
                (-1, 0),
                (1, 0)
            )
            neighborColors = []

            # get neighboring buttons.
            for nbrOffset in neighbors:
                nbrPos = addVectors(pos, nbrOffset)

                isInBounds = isInRange(nbrPos[0], 0, 2) and isInRange(nbrPos[1], 0, 2)
                if isInBounds:
                    neighborColors.append(self.get_color(nbrPos))

            # find most numerous color (if any).
            while len(neighborColors) > 1:
                i = 0
                removedColors = set()

                while i < len(neighborColors):
                    if neighborColors[i] not in removedColors:
                        removedColors.add(neighborColors.pop(i))
                        continue
                    i += 1
            if len(neighborColors) == 0:
                return

            mostNumerousColor = neighborColors[0]
            self.set_color(pos, mostNumerousColor)

        def white():
            colorOff = Colors.GRAY
            colorOn = self.get_color(pos)
            neighbors = (
                (0, -1),
                (0, 1),
                (-1, 0),
                (1, 0)
            )

            self.set_color(pos, colorOff)

            for nbrOffset in neighbors:
                nbrPos = addVectors(pos, nbrOffset)

                isInBounds = isInRange(nbrPos[0], 0, 2) and isInRange(nbrPos[1], 0, 2)
                if isInBounds:
                    # toggle between on and off colors.
                    nbrColor = self.get_color(nbrPos)
                    if nbrColor == colorOff:
                        self.set_color(nbrPos, colorOn)
                    elif nbrColor == colorOn:
                        self.set_color(nbrPos, colorOff)

        def blue():
            centralColor = self.get_color((1, 1))
            if centralColor == Colors.BLUE:
                return

            match centralColor:
                case Colors.GRAY: gray()
                case Colors.BLACK: black()
                case Colors.YELLOW: yellow()
                case Colors.VIOLET: violet()
                case Colors.GREEN: green()
                case Colors.PINK: pink()
                case Colors.RED: red()
                case Colors.ORANGE: orange()
                case Colors.WHITE: white()

        pressedColor = self.get_color(pos)
        match pressedColor:
            case Colors.GRAY: gray()
            case Colors.BLACK: black()
            case Colors.YELLOW: yellow()
            case Colors.VIOLET: violet()
            case Colors.GREEN: green()
            case Colors.PINK: pink()
            case Colors.RED: red()
            case Colors.ORANGE: orange()
            case Colors.WHITE: white()
            case Colors.BLUE: blue()
