from random import randint as r
import os

FIELD_SIZE = 19


#  Функция создания уровня
def create_level():
    field = [["#" if r(0, 1) else "." for _ in range(FIELD_SIZE)] for _ in range(FIELD_SIZE)]

    for i in range(FIELD_SIZE):
        for j in range(FIELD_SIZE):
            if i % 2 == 0 and j % 2 == 0:
                field[i][j] = "*"

    for i in range(4):
        for j in range(4):
            if i == 3 or j == 3:
                field[i][j], field[FIELD_SIZE - 1 - i][FIELD_SIZE - 1 - j] = "#", "#"
            else:
                field[i][j], field[FIELD_SIZE - 1 - i][FIELD_SIZE - 1 - j] = ".", "."

    for elem in field:
        elem[0], elem[-1] = "*", "*"

    field[0], field[-1] = ["*" * FIELD_SIZE], ["*" * FIELD_SIZE]

    field[1][1], field[FIELD_SIZE - 2][FIELD_SIZE - 2] = "1", "2"
    os.remove("data\\map.txt")
    file = open("data\\map.txt", 'w+')
    for elem in field:
        file.writelines("".join(elem) + "\n")
    file.close()
