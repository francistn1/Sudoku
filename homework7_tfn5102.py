############################################################
# CMPSC442: Homework 7
############################################################

student_name = "Timothy Nicholl"
homework2 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""


############################################################
# Imports
############################################################

# Include your imports here, if any are used.


############################################################
# Section 1: Sudoku
############################################################

def sudoku_cells():
    cells = []
    for i in range(9):
        for j in range(9):
            cells.append((i, j))
    return cells


def sudoku_arcs():
    #  9 x 9 grid,
    # blocks.
    arcs = set()
    # columns and rows
    for i in range(9):
        for j in range(9):
            for k in range(9):
                if k != j:
                    # generate arcs
                    arc1 = ((i, j), (i, k))
                    arc2 = ((j, i), (k, i))
                    arcs.add(arc2)
                    arcs.add(arc1)
    # grouped into a 3 x 3 grid of 3 x 3
    for i in range(9):
        for j in range(9):
            for k in range(3):
                for m in range(3):
                    x = int(i / 3) * 3 + k
                    y = int(j / 3) * 3 + m
                    if i != x or j != y:
                        arc3 = ((i, j), (x, y))
                        arcs.add(arc3)
    return arcs


def read_board(path):
    board = []
    zero_check = "0"
    # assume board is initially empty
    with open(path) as infile:
        for row, line in enumerate(infile, start=1):
            board.append([])
            for col, char in enumerate(line.strip(), start=1):
                if char == "*":
                    # cell is empty
                    board[-1].append('0')
                elif char > zero_check:
                    board[-1].append(char)
                else:
                    print("Unrecognized character '%s' at line %d, column %d" %
                          (char, row, col))
    if len(board) < 1:
        print("Board must have at least one row")
        return None
        # NOTE: no else if since we need to check all of these parameters
    if len(board[0]) < 1:
        print("Board must have at least one row")
        return None
    if not all(len(row) == len(board[0]) for row in board):
        print("All rows in board must be of equal length")
        return None

    return board


class Sudoku(object):
    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()

    def __init__(self, board):
        self.board = board
        # self.rLength = len(board) - 1
        # self.cLength = len(board[0]) - 1
        self.board_map = {}
        self.confirm = 0

        # initialize 9 X 9 board
        for i in range(9):
            for j in range(9):
                _char = board[i][j]
                if _char == '0':
                    self.board_map.update({(i, j): self.turn_1_tuple(range(1, 10))})
                else:
                    tp = set()
                    tp.add(int(_char))
                    self.board_map.update({(i, j): tp})
                    self.confirm += 1

    def get_values(self, cell):
        # values_list = list(self.board_map[cell])
        return set(self.board_map[cell])

    def remove_inconsistent_values(self, cell1, cell2):
        temp_cell1 = self.get_values(cell1)
        temp_cell2 = self.get_values(cell2)
        result = set()
        temp_list = list(temp_cell2)[0]

        for i in temp_cell1:
            if i != temp_list:
                result.add(i)

        if len(result):
            self.board_map.update({cell1: result})
            if len(result) == 1:
                self.confirm += 1
            return True
        return False

    def infer_ac3(self):
        ac3_set = []
        for arc in self.ARCS:
            ac3_set.append(arc)
        while ac3_set:
            arc = ac3_set.pop()
            if len(self.board_map[arc[0]]) > 1 and len(self.board_map[arc[1]]) == 1:
                if self.remove_inconsistent_values(arc[0], arc[1]):
                    for x in self.find_neighbor(arc[0]):
                        ac3_set.append(x, arc[0])
        return 1

    def infer_improved(self):
        # check within cube:
        self.infer_ac3()
        # while not self.is_solves():
        while self.confirm < 81:

            if self.update_cell_1():
                self.infer_ac3()
            if self.update_cell_2():
                self.infer_ac3()
            if self.update_cell_0():
                self.infer_ac3()

        return 1

    def infer_with_guessing(self):
        que = []

        self.helper(que)
        return 1

    # ########### HELPER FUNCTIONS ############
    def set_store(self):
        return {1: [0], 2: [0], 3: [0], 4: [0], 5: [0], 6: [0], 7: [0], 8: [0], 9: [0]}

    def update_cell_0(self):
        changed = False
        store = self.set_store()
        for i in range(3):
            for j in range(3):

                for ci in range(3):
                    for cj in range(3):
                        cell = (i * 3 + ci, j * 3 + cj)
                        if len(self.board_map[cell]) == 1:
                            continue
                        else:
                            key = self.board_map[cell]
                            for every_key in key:
                                store[every_key][0] += 1
                                store[every_key].append(cell)
                for _key in store.keys():
                    if store[_key][0] == 1:
                        changed = True
                        rst = set()
                        rst.add(_key)
                        c_cell = store[_key][1]
                        self.board_map.update({c_cell: rst})
                        if len(rst) == 1:
                            self.confirm += 1
                        break
                store = self.set_store()
        return changed

    def update_cell_1(self):
        changed = False
        store_r = self.set_store()
        for i in range(9):
            for j in range(9):
                cell_r = (i, j)
                if len(self.board_map[cell_r]) == 1:
                    continue
                else:
                    key_r = self.board_map[cell_r]
                    for every_key_r in key_r:
                        store_r[every_key_r][0] += 1
                        store_r[every_key_r].append(cell_r)
            for _key_r in store_r.keys():
                if store_r[_key_r][0] == 1:
                    changed = True
                    rst_r = set()
                    rst_r.add(_key_r)
                    c_cell_r = store_r[_key_r][1]
                    self.board_map.update({c_cell_r: rst_r})
                    if len(rst_r) == 1:
                        self.confirm += 1
                    break
            store_r = self.set_store()
        return changed

    def update_cell_2(self):
        changed = False
        store_c = self.set_store()
        for i in range(9):
            for j in range(9):
                cell_c = (j, i)
                if len(self.board_map[cell_c]) == 1:
                    continue
                else:
                    key_c = self.board_map[cell_c]
                    for every_key_c in key_c:
                        store_c[every_key_c][0] += 1
                        store_c[every_key_c].append(cell_c)
            for _key_c in store_c.keys():
                if store_c[_key_c][0] == 1:
                    changed = True
                    rst_c = set()
                    rst_c.add(_key_c)
                    c_cell_c = store_c[_key_c][1]
                    self.board_map.update({c_cell_c : rst_c})
                    if len(rst_c) == 1:
                        self.confirm += 1
                    break
            store_c = self.set_store()
        return changed

    def copy(self):
        map = {i: self.board_map[i] for i in self.board_map}
        s = Sudoku(self.board)
        s.board_map = map

        return s

    def turn_1_tuple(self, a):
        result = set()
        for item in a:
            result.add(item)
        return result

    def find_neighbor(self, cell):
        neighbor = set()
        for row in range(9):
            if row != cell[0]:
                neighbor.add((row, cell[1]))
        for col in range(9):
            if col != cell[1]:
                neighbor.add((cell[0], col))
        for i in range(3):
            for j in range(3):
                x = int(cell[0] / 3) * 3 + i
                y = int(cell[1] / 3) * 3 + j
                if x != cell[0] or y != cell[1]:
                    neighbor.add((x, y))
        return neighbor

    def find_cell_neighbor_in_row(self, cell):
        if len(self.board_map[cell]) == 1:
            return False
        neighbor = set()
        for i in range(9):
            if i != cell[1]:
                it = self.board_map[(cell[0], i)]
                if len(it) == 1:
                    return False
                for ttt in it:
                    neighbor.add(ttt)
        if len(neighbor) == 9:
            return False
        for itm in self.board_map[cell]:
            if itm not in neighbor:
                return itm
        return False

    def find_cell_neighbor_in_col(self, cell):
        if len(self.board_map[cell]) == 1:
            return False
        neighbor = set()
        for i in range(9):
            if i != cell[0]:
                it = self.board_map[(i, cell[1])]
                if len(it) == 1:
                    return False
                for ttt in it:
                    neighbor.add(ttt)
        if len(neighbor) == 9:
            return False
        for itm in self.board_map[cell]:
            if itm not in neighbor:
                return itm
        return False

    def find_cell_neighbor_in_cube(self, cell):

        if len(self.board_map[cell]) == 1:
            return False
        neighbor = set()
        for ci in range(3):
            for cj in range(3):
                x1 = int(cell[0] / 3) * 3 + ci
                x2 = int(cell[1] / 3) * 3 + cj
                if x1 == cell[0] and x2 == cell[1]:
                    continue
                else:
                    a = (x1, x2)
                    it = self.board_map[a]
                    if len(it) == 1:
                        continue
                    for ttt in it:
                        neighbor.add(ttt)
        if len(neighbor) == 9:
            return False
        for itm in self.board_map[cell]:
            if itm in neighbor:
                continue
            else:
                return itm
        return False

    def com_solve(self):
        explored1 = []
        explored2 = []
        count = 0
        for i in range(9):
            for j in range(9):
                cell1 = (i, j)
                cell2 = (j, i)
                value1 = self.board_map[cell1]
                value2 = self.board_map[cell2]
                if len(value1) == 1:
                    count += 1
                    if list(value1)[0] in explored1:
                        return False, 0
                    else:
                        explored1.append(list(value1)[0])
                if len(value2) == 1:

                    if list(value2)[0] in explored2:
                        return False, 0
                    else:
                        explored2.append(list(value2)[0])
            explored1 = []
            explored2 = []
        explored3 = []
        for i in range(3):
            for j in range(3):
                for ci in range(3):
                    for cj in range(3):
                        cell3 = (i * 3 + ci, j * 3 + cj)
                        value3 = self.board_map[cell3]
                        if len(value3) == 1:

                            if list(value3)[0] in explored3:
                                return False, 0
                            else:
                                explored3.append(list(value3)[0])
                explored3 = []
        return True, count

    def pre_deal(self):
        improve_finish = True
        self.infer_ac3()
        while improve_finish:
            a = 0
            if self.update_cell_0():
                self.infer_ac3()
                a += 1
            if self.update_cell_1():
                self.infer_ac3()
                a += 1
            if self.update_cell_2():
                self.infer_ac3()
                a += 1
            if a == 0:
                improve_finish = False

    def helper(self, que):

        self.pre_deal()
        s = self.com_solve()
        if s == (True, 81):
            return self

        if not self.com_solve()[0]:
            return False

        for i in range(9):
            for j in range(9):
                cell = (i, j)

                if len(self.board_map[cell]) > 1:
                    f2 = set()
                    fi_set = set()
                    cc = 0
                    for _ii in self.board_map[cell]:
                        if not cc:
                            fi_set.add(_ii)
                        else:
                            f2.add(_ii)
                        cc += 1

                    future_board = {i2: self.board_map[i2] for i2 in self.board_map}
                    future_board.update({cell: f2})

                    self.board_map.update({cell: fi_set})

                    que.append(future_board)
                    result = self.helper(que)

                    if result:
                        return True
                        # que0.append(current)
                        # return que0

                    while not result:
                        self.board_map = que.pop()
                        result = self.helper(que)
                        if result:
                            return True


############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
Approximately how long did you spend on this assignment?

15 - 20 hours 
"""

feedback_question_2 = """
Which aspects of this assignment did you find most challenging? Were there any
significant stumbling blocks?

This was by far the most difficult homework I had done for this class by far, every aspect of this assignment was 
challenging especially the final function I had to do. I had to consult hours of tutorials and refer to previous 
assignments for aid in this particular assignment. It still doesn't work properly but enough to hopefully gain some
points
"""

feedback_question_3 = """
Which aspects of this assignment did you like? Is there anything you would have
changed?

I liked the fact that this was optional. That is all
"""
