# input: array in the following format
# [[N]?, String, String, String, String]
import pickle
import os
from pathlib import Path

PATH = os.getcwd()


def write_list(game_list, has_console=False):
    if has_console:
        name_of_file = PATH + "/game_list"
    else:
        name_of_file = PATH + "/game_list_no_console"

    with open(name_of_file, 'wb') as filehandle:
        pickle.dump(game_list, filehandle)

    print("Saved data file at " + name_of_file)


def read_list(has_console=False):
    game_list = []
    if has_console:
        name_of_file = (PATH + "/game_list")
    else:
        name_of_file = PATH + "/game_list_no_console"
    try:
        with open(name_of_file, 'rb') as filehandle:
            game_list = pickle.load(filehandle)

    except OSError as error:
        raise error

    return game_list


def parse_table(game_list):
    has_console = False
    assert type(game_list) == type([]) and len(game_list) > 0

    if type(game_list[0][0]) == type([]):
        has_console = True

    table = "Title|Dollars Off|%|Sale|Retail|Console"
    table_alignment = ":--|:--|:--|:--|:--|:--"
    rows = ""

    for game in game_list:
        if has_console:
            title = game[1]
            dollars_saved = game[2]
            discount = game[3]
            sale = game[4]
            retail = game[5]
            console = ', '.join(game[0])
        else:
            title = game[0]
            dollars_saved = game[1]
            discount = game[2]
            sale = game[3]
            retail = game[4]
            console = "N/A"

        # = retail - sale
        rows += title + "|$" + str(dollars_saved) + "|" + str(discount) + "%|$" + str(sale) + "|$" + str(retail) + "|" + str(console) + "\n"
    text_block = table + '\n' + table_alignment + '\n' + rows
    return text_block


def __write_text_table(table, has_console=False):
    for p in Path(PATH).glob("table*.txt"):
        os.remove(p)
    if has_console:
        file_to_write = PATH + "/table.txt"
    else:
        file_to_write = PATH + "/table_no_console.txt"

    with open(file_to_write, "w") as text_file:
        text_file.write("%s" % table)

    print("Saved reddit table at " + file_to_write)


def __sort_list_by_percent(game_list, hasConsole=False):
    if hasConsole:
        index = 2
    else:
        index = 1

    return sorted(game_list, key = lambda game_list: game_list[index], reverse=True)


if __name__ == '__main__':
    games = read_list(True)
    sorted = __sort_list_by_percent(games, True)
    table = parse_table(sorted)
    __write_text_table(table, True)
else:
    PATH += "/src"
