import argparse
from blessings import Terminal
import json
import random
import sys
import pycuber as pc
from pyfiglet import Figlet

term = Terminal()


def load_algs(filename):
    """Accepts filename of json data, returns encoded object
    alg file should follow the format: 
        'alg_name: [list of algs]
        :param filename: name of the file to load algs from, with extension """
    try:
        with open(filename, 'r') as j:
            raw_data = j.read()
    except FileNotFoundError:
        exit('file not found, quitting...')
    return json.loads(raw_data)


def reverse_alg(alg):
    return pc.Formula(alg).reverse()


def format_alg_for_speech(alg):
    splitted = alg.split()


def display_alg(alg):
    pass


def display_title():
    title_text = 'Last Layer algorithm trainer'
    with term.location(term.width // 2 - len(title_text) // 2, 1):
        print(term.reverse + title_text + term.normal)
        print('─' * term.width)


def ascii_title():
    with term.location(0, 0):
        title_text = 'Last  Layer  Algorithm  Trainer'
        f = Figlet(font='small', width=term.width)
        print(term.white(f.renderText(title_text)))
    with term.location(0, 5):
        print('─' * term.width)
    print(term.move_y(6))


def box_draw(width, height, mode='center'):
    """ Draws a box of width and height, returns the coordinate of the upper 
        left corner for future location adjustments.
        """
    top_left = '╒'
    top_right = '╕'
    bottom_left = '╘'
    bottom_right = '╛'
    horizontal = '═'
    vertical = '┆'
    left_bound = term.width // 2 - width // 2
    top_bound = term.height // 2 - height // 2
    if mode == 'center':
        with term.location(left_bound, top_bound):  # move to upperleft corner of the box
            print(top_left + horizontal * (width - 2) + top_right)
            for row in range(height):
                print(term.move_right * left_bound + vertical + term.move_right * (width - 2) + vertical)
                # print(term.move_down)
            print(term.move_right * left_bound + bottom_left + horizontal * (width - 2) + bottom_right)
    return left_bound + 1, top_bound + 1


def card_draw(current_alg, algs):
    print(term.clear)
    ascii_title()
    card_width = (3 * term.width) // 4
    card_height = term.height // 2
    cords = box_draw(card_width, card_height)
    with term.location(*cords):
        print('\n' + term.move_x(cords[0] + (card_width // 3)) + 'The shuffle is: \n')
        print(term.move_x(cords[0] + 4) + str(reverse_alg(algs[current_alg][0])))
        print(term.move_y((cords[1] + (term.height // 2) - 1)) + term.move_x(
            cords[0] + 16) + 'press enter to see back of card')
        key = input()
        if key == 'q':
            print(term.exit_fullscreen())
            exit()
        print(term.clear)
    ascii_title()
    with term.location(*cords):
        box_draw(card_width, card_height)
        print('\n' + term.move_x(cords[0] + (card_width // 3)) + 'This is {0} perm\n'.format(current_alg))
        for vertical_offset, alg in enumerate(algs[current_alg]):
            print(term.move_x(cords[0] + 4) + '{0}: {1}'.format(vertical_offset + 1, alg))
        else:
            print(term.move_y((cords[1] + (term.height // 2) - 1)) + term.move_x(
                cords[0] + 16) + 'press enter to continue')
        key = input()
        if key == 'q':
            print(term.exit_fullscreen())
            exit()


def main():
    algs = load_algs('PLL_algs.json')
    print(term.enter_fullscreen())
    ascii_title()
    for i in range(10):
        possible_algs = list(algs.keys())
        card_draw(random.choice(possible_algs), algs)
    print(term.exit_fullscreen())


if __name__ == '__main__':
    main()
