#  Функция загрузки карты из текстового файла
def load_level(filename):
    filename = "data/" + filename
    with open(filename, "r") as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))
    mapFile.close()
    return list(map(lambda x: x.ljust(max_width, "."), level_map))