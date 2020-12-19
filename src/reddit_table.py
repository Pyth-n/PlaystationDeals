# input: array in the following format
# [[N]?, String, String, String, String]
import pickle
import os
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

    table = "Title|Discount %|Sale $|Retail $|Console"
    table_alignment = ":--|:--|:--|:--|:--"
    rows = ""

    for game in game_list:
        if has_console:
            title = game[1]
            discount = game[2]
            sale = game[3]
            retail = game[4]
            console = ', '.join(game[0])
        else:
            title = game[0]
            discount = game[1]
            sale = game[2]
            retail = game[3]
            console = "N/A"

        rows += title + "|" + discount + "|" + sale + "|" + retail + "|" + console + "\n"
    text_block = table + '\n' + table_alignment + '\n' + rows
    return text_block


def __write_text_table(table, has_console=False):
    if has_console:
        file_to_write = PATH + "/table.txt"
    else:
        file_to_write = PATH + "/table_no_console.txt"

    with open(file_to_write, "w") as text_file:
        text_file.write("%s" % table)

    print("Saved reddit table at " + file_to_write)


if __name__ == '__main__':
    games = read_list(True)
    table = parse_table(games)
    __write_text_table(table, True)
else:
    PATH += "/src"
