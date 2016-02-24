""" notes coroutine box handler: using a coroutine to save state for repeated box rendering
    * Box renders input, rolls over to new lines when it hits the end.
    * Box uses arrow keys to update size
        * the box_updated flag exists so that when in the loop, the box only gets redrawn
        when the size changes
        * text flow inside the box updates after a new character is hit
    * ``with curtsies.Input() as input:`` makes input be a generator, perhaps further
    optimization could be done with calling next on it, instead of using it in a for loop
    * the double break is to get out of the for loop, and then the ``while True:`` loop
    * exceptions propagate out from the generator, hence the raise stop iteration error
"""
from curtsies import fsarray, FSArray, Input, FullscreenWindow


def string_as_array_of_width(string, width):
    """take a string, and break it into a list of strings,
       each of maximum length width, return that list as an FSArray"""
    lines = ['']
    line_number = 0
    for i, character in enumerate(string):
        lines[line_number] = lines[line_number] + character
        if i > 2 and i % width == 0:
            line_number += 1
            lines.append('')
    return fsarray(lines)


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


def box_handler(height=10, width=20, contents=''):
    """ A coroutine style generator for creating boxes with borders and contents
    """
    cursor = [0, 0]  # used to remember the position in a content_array box
    box_updated = True
    content_string = contents
    content_array = fsarray('')
    while True:
        if box_updated:
            box_array = produce_box_of_size_height_width(height, width)
            box_array[1:content_array.height + 1, 1: content_array.width + 1] = content_array
            box_updated = False
        yielded = yield box_array
        if yielded and isinstance(yielded, str):
            if yielded == 'q':
                raise StopIteration
            elif len(yielded) == 1 or yielded == '<SPACE>':
                if yielded == '<SPACE>':
                    yielded = ' '
                content_string += yielded
                content_array = string_as_array_of_width(content_string,
                                                         width - 3)  # width-3 because
                #  2 columns get used up on the frame
                if cursor[1] >= width - 2:
                    cursor[1] = 1
                    cursor[0] += 1
                else:
                    cursor[1] += 1
            # This is how curtsies represents arrow keys:
            elif yielded in ('<UP>', '<DOWN>', '<RIGHT>', '<LEFT>'):
                if yielded == '<UP>':
                    height += 1
                elif yielded == '<DOWN>' and height >= 3:  # don't let the box poof it self
                    height += -1
                elif yielded == '<LEFT>' and width >= 3:
                    width += -1
                elif yielded == '<RIGHT>':
                    width += 1
                else:
                    pass
            box_updated = True


def run():
    with FullscreenWindow() as win:
        i = 1
        box_generator = box_handler()
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
