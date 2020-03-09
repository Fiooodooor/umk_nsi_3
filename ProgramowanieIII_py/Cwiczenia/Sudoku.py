

def check_insert(x: int, y: int, value: int) -> bool:
    x_p = int(x/3)*3  # which 'x' rectangle is it part of. x=x_p+i%3
    y_p = int(y/3)*3  # which 'y' rectangle is it part of. y=y_p+i/3
    for i in range(0, 9):  # go thorough all row, column and square items in one loop looking for value
        if sudoku_map[i][x] == value or sudoku_map[y][i] == value or sudoku_map[y_p+int(i/3)][x_p+(i%3)] == value:
            return False
    return True


def sudoku_solver(x: int, y: int) -> bool:
    if x > 8:
        x = 0
        y += 1
    if y > 8:
        return True
    if sudoku_map[y][x] == 0:
        for it in range(1, 10):
            if check_insert(x, y, it):
                sudoku_map[y][x] = it
                if sudoku_solver(x+1, y):
                    return True
        sudoku_map[y][x] = 0
        return False
    else:
        return sudoku_solver(x+1, y)


def print_sudoku(the_map: []):
    print("(begin map print)")
    for row_it in the_map:
        print(row_it)
    print("(end of map print)")


def print_error(error: str) -> bool:
    print("Error! " + error)
    return False


def sudoku(the_map: []) -> bool:
    # make na deep copy of original map ans basic check, then start solving
    if len(the_map) != 9:
        return print_error("(assert) The sudoku map rows number is not equal 9!")
    for row in the_map:
        if len(row) != 9:
            return print_error("(assert) One of sudoku map rows, has column nr that not equals 9!")
        for nr in row:
            if not isinstance(nr, int):
                return print_error("(assert) One of elements is not an integer!")
        sudoku_map.append(row.copy()) # The row was checked and is ok to deep copy.

    if sudoku_solver(0, 0):
        print_sudoku(sudoku_map)
        return True
    return False


if __name__ == "__main__":
    sudoku_map = []
                                        # y:  y_p:
    origin_map=[[5,3,0, 0,7,0, 0,0,0],  # 1         map[0][0-8]
                [6,0,0, 1,9,5, 0,0,0],  # 2     I   map[1][0-8]
                [0,9,8, 0,0,0, 0,6,0],  # 3         map[2][0-8]

                [8,5,0, 0,6,0, 0,0,3],  # 4         map[3][0-8]
                [4,0,0, 8,0,3, 0,0,1],  # 5    II   map[4][0-8]
                [7,0,0, 0,2,0, 0,0,6],  # 6         map[5][0-8]

                [0,6,0, 0,0,0, 2,8,0],  # 7         map[6][0-8]
                [0,0,0, 4,1,9, 0,0,5],  # 8   III   map[7][0-8]
                [0,0,0, 0,8,0, 0,7,9]]  # 9         map[8][0-8]
#             x: 1 2 3  4 5 6  7 8 9
#           x_p:   I     II     III
#   Indexation, enumeration and all fields described in the same way they are implemented
#   x and y are easy to guess, the column and row selectors. The x_p and y_p are the 'square' selectors
#   sudoku --> main function for validating the supported map and solving the sudoku
#              return True is sudoku can be solved, False if supported data is invalid or sudoku can no be solved.
    if sudoku(origin_map):
        print("Udało się poprawnie rozwiązać sudoku")
    else:
        print("Brak poprawnych rozwiaząń")
    exit(0)
