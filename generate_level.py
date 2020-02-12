from tiles import Iron, Grass, Wood, PlayerOne, PlayerTwo, StandingEnemy, SmartEnemy, MovingEnemy, \
    GhostEnemy

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
                new_enemy = StandingEnemy("enemy", x, y)  # Enemy tile creation
                enemy.append(new_enemy)
            elif level[y][x] == "M":
                new_moving_enemy = MovingEnemy("moving_enemy", x, y)
                enemy.append(new_moving_enemy)
            elif level[y][x] == "S":
                new_smart_enemy = SmartEnemy("smart_enemy", x, y)
                enemy.append(new_smart_enemy)
            elif level[y][x] == "G":
                new_ghost_enemy = GhostEnemy("ghost_enemy", x, y, new_player_1)
    return new_player_1, new_player_2, enemy
