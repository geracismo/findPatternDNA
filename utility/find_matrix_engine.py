from math import sqrt
import numpy as np


class FindMatrixEngine:

    def __init__(self, matrix, row, col):
        self.matrix = matrix
        self.currentPivot = [0, 0]
        self.matrixRow = row
        self.matrixCol = col

    # search pattern in according to the pattern selected
    def search_patter(self, pattern):
        result = [0]
        if pattern.lower() == "a":
            for x in range(4):
                self.currentPivot = [0, 0]
                if x > 0:
                    self.matrix = np.rot90(self.matrix)
                if self.find_lower_left_bit() == 1:
                    firstInclineLine = self.incline_line_bottom_up_right(self.currentPivot[0], self.currentPivot[1])
                    if firstInclineLine[3] == 1:
                        secondInclineLine = self.incline_line_top_down_right(self.currentPivot[0], self.currentPivot[1])
                        if secondInclineLine[3] == 1:
                            thirdLine = self.straight_line_left_to_right(firstInclineLine[1], secondInclineLine[1])
                            if thirdLine[0] == 1:
                                result = [1, firstInclineLine[2] + secondInclineLine[2] + thirdLine[2], x]
                                break
                else:
                    result = [-1]

        elif pattern == "i":
            for x in range(4):
                self.currentPivot = [len(self.matrix) - 1, len(self.matrix[0]) - 1]
                if x > 0:
                    self.matrix = np.rot90(self.matrix)
                if self.find_higher_left_bit() == 1:
                    firstInclineLine = self.straight_line_top_down(self.currentPivot[0], self.currentPivot[1])
                    if firstInclineLine[3] == 1:
                        result = [1, firstInclineLine[2], x]
                        break
                else:
                    result = [-1]

        elif pattern == "l":
            for x in range(4):
                self.currentPivot = [len(self.matrix) - 1, len(self.matrix[0]) - 1]
                if x > 0:
                    self.matrix = np.rot90(self.matrix)
                if self.find_higher_left_bit() == 1:
                    firstInclineLine = self.straight_line_top_down(self.currentPivot[0], self.currentPivot[1])
                    if firstInclineLine[3] == 1:
                        secondLine = self.straight_line_left_to_right(firstInclineLine[2], None)
                        if len(secondLine) > 1 and secondLine[1] < firstInclineLine[0]:
                            result = [1, firstInclineLine[2] + secondLine[2], x]
                        break
                else:
                    result = [-1]

        elif pattern.lower() == "v":
            for x in range(4):
                self.currentPivot = [len(self.matrix) - 1, len(self.matrix[0]) - 1]
                if x > 0:
                    self.matrix = np.rot90(self.matrix)
                if self.find_higher_left_bit() == 1:
                    firstInclineLine = self.incline_line_top_down_right(self.currentPivot[0], self.currentPivot[1])
                    if firstInclineLine[3] == 1:
                        secondInclineLine = self.incline_line_bottom_up_right(self.currentPivot[0], self.currentPivot[1])
                        if secondInclineLine[3] == 1:
                            result = [1, firstInclineLine[2] + secondInclineLine[2], x]
                            break
                else:
                    result = [-1]

        return result

    def straight_line_top_down(self, px, py):
        lengthLine = 1
        set = [[px, py]]
        while True:
            if px + 1 < len(self.matrix) and self.matrix[px + 1][py] == "1":
                lengthLine += 1
                px += 1
                set.append([px, py])
            else:
                if lengthLine > 2:
                    self.currentPivot[0] = px
                    self.currentPivot[1] = py
                    return [lengthLine, [], set, 1]
                else:
                    return [lengthLine, [], set, 0]

    def incline_line_bottom_up_right(self, px, py):
        lengthLine = 1
        middleSet = []
        set = [[px, py]]
        while True:
            if px - 1 > 0 and py + 1 < len(self.matrix[0]) and self.matrix[px - 1][py + 1] == "1":
                if lengthLine != 1:
                    middleSet.append([px, py])
                lengthLine += 1
                px -= 1
                py += 1
                set.append([px, py])
            else:
                if lengthLine > 2:
                    self.currentPivot[0] = px
                    self.currentPivot[1] = py
                    return [lengthLine, middleSet, set, 1]
                else:
                    return [lengthLine, middleSet, set, 0]

    def incline_line_top_down_right(self, px, py):
        lengthLine = 1
        set = [[px, py]]
        while True:
            if px + 1 < len(self.matrix) and py + 1 < len(self.matrix[0]) and self.matrix[px + 1][py + 1] == "1":
                lengthLine += 1
                px += 1
                py += 1
                set.append([px, py])
            else:
                if lengthLine > 2:
                    self.currentPivot[0] = px
                    self.currentPivot[1] = py
                    return [lengthLine, [], set, 1]
                else:
                    return [lengthLine, [], set, 0]

    def straight_line_left_to_right(self, firstInclineLine, secondInclineLine):
        lengthLine = 1
        set = []
        for x in firstInclineLine:
            if secondInclineLine is None and x != firstInclineLine[-1]:
                continue
            set.clear()
            px = x[0]
            py = x[1]
            set.append([px, py])
            while True:
                if py + 1 < len(self.matrix[0]) and self.matrix[px][py + 1] == "1":
                    lengthLine += 1
                    py += 1
                    set.append([px, py])
                elif lengthLine > 2:
                    if secondInclineLine is not None:
                        for y in set:
                            for z in secondInclineLine:
                                if y == z:
                                    self.currentPivot[0] = px
                                    self.currentPivot[1] = py
                                    return [1, lengthLine, set]

                    return [1, lengthLine, set]
                else:
                    break

        return [0]

    def find_lower_left_bit(self):
        result = 0
        for j in range(len(self.matrix)):
            for i in range(len(self.matrix[0])):
                if self.matrix[j][i] == "1":
                    result = 1
                    if self.distance_from_corner(j, i, len(self.matrix) - 1, 0) < self.distance_from_corner(
                            self.currentPivot[0], self.currentPivot[1], len(self.matrix) - 1, 0):
                        self.currentPivot[0] = j
                        self.currentPivot[1] = i

        return result

    def find_higher_left_bit(self):
        result = 0
        for j in range(len(self.matrix)):
            for i in range(len(self.matrix[0])):
                if self.matrix[j][i] == "1":
                    result = 1
                    if self.distance_from_corner(j, i, 0, 0) < self.distance_from_corner(self.currentPivot[0],
                                                                                         self.currentPivot[1], 0, 0):
                        self.currentPivot[0] = j
                        self.currentPivot[1] = i

        return result

    def distance_from_corner(self, px, py, dx, dy):
        if px == dx:
            if py > dy:
                return py - dy
            else:
                return dy - py
        elif py == dy:
            if px > dx:
                return px - dx
            else:
                return dx - px
        else:
            # pythagoras theorem
            supportPoint = [dx, py]
            distance1 = self.distance_from_corner(px, py, supportPoint[0], supportPoint[1])
            distance2 = self.distance_from_corner(supportPoint[0], supportPoint[1], dx, dy)
            return sqrt(distance1 ** 2 + distance2 ** 2)
