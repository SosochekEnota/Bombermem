from tiles import Iron, Grass, Wood, PlayerOne, PlayerTwo, Enemy


def generate_level_(level):
    new_player_1, new_player_2, x, y = None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            Grass("grass", x, y)
            if level[y][x] == "#":
                Wood("wall", x, y)
            elif level[y][x] == "*":
                Iron("iron", x, y)
            elif level[y][x] == "1":
                new_player_1 = PlayerOne("player_1", x, y)
            elif level[y][x] == "2":
                new_player_2 = PlayerTwo("player_2", x, y)
            elif level[y][x] == "E":
                new_player_2 = Enemy("enemy", x, y)
    return new_player_1, new_player_2
