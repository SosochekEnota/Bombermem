from tiles import Iron, Grass, Wood, PlayerOne, PlayerTwo, Enemy

enemy = []
def generate_level_(level):
    new_player_1, new_player_2, x, y = None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            Grass("grass", x, y)
            if level[y][x] == "#":  # Wood tile creation
                Wood("wall", x, y)
            elif level[y][x] == "*":  # Iron tile creation
                Iron("iron", x, y)
            elif level[y][x] == "1":
                new_player_1 = PlayerOne("player_1", x, y)  # Player 1 tile creation
            elif level[y][x] == "2":
                new_player_2 = PlayerTwo("player_2", x, y)  # Player 2 tile creation
            elif level[y][x] == "E":
                new_enemy = Enemy("enemy", x, y)  # Enemy tile creation
                enemy.append(new_enemy)
    return new_player_1, new_player_2, enemy
