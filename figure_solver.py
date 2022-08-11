import requests
from bs4 import BeautifulSoup
import json
import numpy as np
from copy import deepcopy
import math

URL = "https://figure.game/"


def main():
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find("script", id="__NEXT_DATA__")
    props = json.loads(results.string)

    puzzle = props["props"]["pageProps"]

    tiles = np.reshape(puzzle["tiles"], (5, 5))

    solution = solve_puzzle(tiles, 8)
    print(list(reversed(solution)))


def remove_one_tile(x, y, tiles):
    old_color = tiles[y][x]

    tiles[y][x] = -1
    if x < len(tiles[0]) - 1 and tiles[y][x + 1] == old_color:
        remove_one_tile(x + 1, y, tiles)
    if x > 0 and tiles[y][x - 1] == old_color:
        remove_one_tile(x - 1, y, tiles)
    if y < len(tiles) - 1 and tiles[y + 1][x] == old_color:
        remove_one_tile(x, y + 1, tiles)
    if y > 0 and tiles[y - 1][x] == old_color:
        remove_one_tile(x, y - 1, tiles)


def tiles_comes_down(tiles):
    for x in range(len(tiles[0])):
        for y in range(len(tiles) - 1, 0, -1):
            if tiles[y][x] == -1:
                for yy in range(y - 1, -1, -1):
                    if tiles[yy][x] != -1:
                        tiles[y][x] = tiles[yy][x]
                        tiles[yy][x] = -1
                        break


def check_win(tiles):
    for x in range(len(tiles[0])):
        for y in range(len(tiles)):
            if tiles[y][x] != -1:
                return False
    return True


def solve_puzzle(tiles, actions_remaining):
    if actions_remaining < 0:
        return False
    if check_win(tiles):
        return True

    paths = {}
    for x in range(len(tiles[0])):
        tiles_copy = deepcopy(tiles)
        if tiles_copy[len(tiles_copy) - 1][x] != -1:
            remove_one_tile(x, len(tiles_copy) - 1, tiles_copy)
            tiles_comes_down(tiles_copy)
            res = solve_puzzle(tiles_copy, actions_remaining - 1)

            if res is True:
                return [x]
            if isinstance(res, list):
                paths[x] = res

    if not paths:
        return False
    else:
        best_score = math.inf
        best_path = None
        for k, path in paths.items():
            if len(path) < best_score:
                best_score = len(path)
                best_path = k
        return paths[best_path] + [best_path]


if __name__ == "__main__":
    main()
