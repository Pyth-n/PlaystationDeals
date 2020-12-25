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
    rows_list = []
    character_count = 0

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

        rows += title + "|$" + str(dollars_saved) + "|" + str(discount) + "%|$" + str(sale) + "|$" + str(
            retail) + "|" + str(console) + "\n"

        character_count += len(title + "|$" + str(dollars_saved) + "|" + str(discount) + "%|$" + str(sale) + "|$" + str(retail) + "|" + str(console) + "\n")
        if character_count > 9800:
            text_block = table + '\n' + table_alignment + '\n' + rows
            rows = ""
            character_count = 0
            rows_list.append(text_block)
    return rows_list


def __write_text_table(table_list, has_console=False):
    for p in Path(PATH).glob("table*.txt"):
        os.remove(p)

    for i, table in enumerate(table_list):
        file_name = __get_write_name(i, has_console)
        with open(file_name, "w") as text_file:
            text_file.write("%s" % table)

        print("Saved reddit table at " + file_name)


def __get_write_name(number, hasConsole):
    if hasConsole:
        return PATH + f'/table{number}.txt'
    else:
        return PATH + f'/table_no_console{number}.txt'


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
