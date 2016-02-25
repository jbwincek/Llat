from curtsies import FullscreenWindow, Input, FSArray, fsarray, fmtstr, formatstringarray
import time


""" Notes about this file:
        * uses coroutine style generators to create a menu with selectable items
        * if enter is pressed while an item is selected it calls the corresponding callable
            * I say 'callable' because some are generators and some are functions
        * This showed me an issue with input, and trying to figure out how to elegantly pass it
          into deeper and deeper nested things.
        * This is starting to feel very spaghetti
            * but seems worth pursuing still, to find the extreme end of where this style of
              programming can go. As it seems like there's a kernel of goodness here, that just
              perhaps needs refactoring.
        * perhaps having input be a context created for each inner window?
        * I don't like how dependent or nested this all feels, it feels like a tower rather than
          a modular set of blocks to build with, and I wanted the latter.
        * continuing experimentation will go on in a file named menu_test_2.py, because this file is
          already long enough, and iteratively developing worked well for me in generator_test.py
        * In yields_menus(menu_list_of_tuples, window) pass_on_input was a failed attempt at
          using a boolean flag to skip parsing the input event in function and instead pass it to
          the callable. An issue arose with the yields_menus being iterated through on each input
          event, which is like a tick. So each tick the input would have to be passed into the sub
          callable.
            * I think the issue could be worked around by remembering which menu item was selected,
              then passing the input event through send() on that selected callable. And maybe
              with enough state remembering in the sub coroutine/sub window, it would go okay?
        * this all feels very if statement dependent
"""


def produce_box_of_size_height_width(height, width):
    """ Give it height and width, and it'll give you a bordered box as a FSArray.
    """
    top_left = '╒'
    top_right = '╕'
    bottom_left = '╘'
    bottom_right = '╛'
    horizontal = '═'
    vertical = '│'
    box_array = fsarray([' ' * width for _ in range(height)])
    box_array[0, 0] = top_left
    box_array[0, width - 1] = top_right
    box_array[height - 1, 0] = bottom_left
    box_array[height - 1, width - 1] = bottom_right
    if width >= 3:  # fill space between corners if needed
        span = width - 2
        for index in range(span):
            box_array[0, index + 1] = horizontal
            box_array[height - 1, index + 1] = horizontal
    if height >= 3:
        span = height - 2
        for index in range(span):
            box_array[index + 1, 0] = vertical
            box_array[index + 1, width - 1] = vertical
    return box_array


def array_insert(insertable,
                 receives_insertion,
                 offset = (2,2),
                 highlight = False,
                 highlight_color='blue'):
    """ inserts insertable into receives_insertion, where insertable is a string, and
        receives_insertion is an FSArray
        array_insert will insert insertables bigger than receives_insertion can handle

        * offset is (x.y) because that's the only reasonable way
        * highlight kwarg changes the coloring of the char to insert
        * highlight_color sets the color for showing the highlight

        Goes character by character through insertable to add them one at a time to
        receives_insertion since that gets around the complication of making slice sizes with the
        length of strings trying to be inserted.
    """
    y = offset[1]
    for x, char in enumerate(insertable):
        if char in ('\n', '\r'):
            y+=1
        if highlight:
            receives_insertion[y, offset[0] + x] = fmtstr(char, fg=highlight_color)
        else:
            receives_insertion[y, offset[0] + x] = char
    return receives_insertion


def yields_menus(menu_item_list_of_tuples, window, height=20, width=40):
    """ creates an interactive menu coroutine style generator
        * menu-item_list_of_tuples is a list of tuples of the format:
            [('label', callable), (...,...), ...]
        * height, and width are self explanatory

    """
    menu_list = menu_item_list_of_tuples
    active_menu_item = 0  # 0 means top item
    b_o = 2  # border offset
    pass_on_input = False # see notes at top of file
    while True:
        menu_array = produce_box_of_size_height_width(height,width)
        for i, individual_tuple in enumerate(menu_list):
            menu_item = individual_tuple[0]
            if len(menu_item) >= width - 3:
                menu_item = menu_item[0:width-3]
            if i == active_menu_item:
                active = True
            else:
                active = False
            menu_array = array_insert(menu_item,
                                      menu_array,
                                      offset=[b_o, b_o+i],
                                      highlight=active )
        yielded = yield menu_array
        if yielded and isinstance(yielded, str):
            if pass_on_input:
                selected_generator.send(yielded)
            else:
                if yielded == '<DOWN>' and active_menu_item < len(menu_list):
                    active_menu_item +=1
                elif yielded == '<UP>' and active_menu_item >= 0:
                    active_menu_item -=1
                elif yielded == '<Ctrl-j>':  # <Ctrl-j> means enter/return
                    pass_on_input = True
                    selected_generator = menu_list[active_menu_item][1](window)
                    next(selected_generator)
                    next(selected_generator)
                    pass_on_input = False
                else:
                    pass


def go(window):
    """
    coroutine style window popup as an example of what happens when a menu item gets selected
    """
    content_string = ' '
    array = produce_box_of_size_height_width(15, 30)
    array = array_insert('go was called', array)
    window.render_to_terminal(array)
    while True:
        input_event = yield
        if input_event and isinstance(yielded, str):
            if input_event == '<RIGHT>':
                array = array_insert('back of slide', array)
                window.render_to_terminal(array)
            if input_event == 'q':
                break



def help(window):
    pass
def options(window):
    pass
def quitter(window):
    """calling quit directly causes all sorts of errors, so raise an exception instead"""
    raise StopIteration

def run():
    with FullscreenWindow() as win:
        i = 1
        menu_dict = [('go', go), ('help', help), ('options', options), ('quit', quitter)]
        box_generator = yields_menus(menu_dict, win)
        while True:
            with Input() as input:
                array = next(box_generator)
                win.render_to_terminal(array)
                for e in input:
                    try:
                        box_generator.send(e)
                        array = next(box_generator)
                        win.render_to_terminal(array)
                    except StopIteration:
                        print('got StopIteration')
                        break
                break

run()