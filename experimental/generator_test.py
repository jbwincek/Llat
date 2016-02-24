
""" Notes on this document: code chunks are broken up by notes placed above them.
                            Many chunks have a commented out run_x() method, use
                            this to select which one to run.
"""


""" Notes on technique 1:
        * the function print statements skips things
        * each time something is sent into the iterator the code pointer gets advanced to that
        assignment, which is why it skips things
        * perhaps that could be used for control flow stuff?
"""


def gen_test_1():
    result = 1
    other = None
    while True:
        if result <= 20:
            print('in gen result is {}'.format(result))
            other = yield result
            if other:
                print(other)
            result += 1
        else:
            break


def run_1():
    gen = gen_test1()
    # next(gen)
    for item in gen:
        if isinstance(item, int):
            if item % 5 == 0:
                gen.send('can be divided by five')
            else:
                gen.send(None)
        print(item)

#run_1()


""" Notes on technique 2: (trying to use send() methods to control flow in a generator)
        * it works
        * can use the generator as a closure
"""
def gen_test_2():
    value_1 = 1
    value_2 = 2
    while True:
        other = yield
        if isinstance(other,int):
            print('got an integer: {}'.format(other))
        elif isinstance(other,str):
            print('got a string: {}'.format(other))


def run_2():
    gen = gen_test_2()
    next(gen)  # don't forget to initialize the generator to get it up to the yield point
    gen.send(5)
    gen.send('hello')
#  run_2()


""" Notes on technique 3: (trying to use async / await for keyboard input handling)
    * async is hard
    * it seems like it needs to be "async all the way down"
    * DOESN'T WORK CURRENTLY

"""
import asyncio
from curtsies import Input
from collections import deque
#from concurrent.futures import ThreadPoolExecutor as Pool
loop = asyncio.get_event_loop()

output_deque = deque()

@asyncio.coroutine
def wait_for_keystroke():
    print('waiting for keystrokes')
    with Input() as input_generator:
        yield from input_generator

async def gen_test_3():
    print('entering gen_test_3')
    while True:
        key = await wait_for_keystroke()
        print('got: {}'.format(key))
        if key == 'q':
            print('stopping loop')
            loop.stop()




def run_3():
    loop.run_until_complete(gen_test_3())
    loop.close()


# run_3()

""" Notes on technique 4: box drawing
    * render_to_terminal flushes when it renders
    * getting FSArray slices correct is hard:
        * follows format [height,width]
        * the top left corner is [0,0]
        * the bottom right corner is [height-1, width-1]
"""

from curtsies import fmtstr, FSArray, fsarray
from curtsies import FullscreenWindow
import time


def returns_FSArray_boxes(height, width):
    top_left = '╒'
    top_right = '╕'
    bottom_left = '╘'
    bottom_right = '╛'
    horizontal = '═'
    vertical = '│'
    box_array = fsarray([' ' * width for _ in range(height)])
    # FSArrays are height,width <- weird but true
    box_array[0,0] = top_left
    box_array[0,width-1] = top_right
    box_array[height-1,0] = bottom_left
    box_array[height-1,width-1] = bottom_right
    if width>2:
        span = width-2
        for index in range(span):
            box_array[0,index+1] = horizontal
            box_array[height-1, index + 1] = horizontal
    if height>2:
        span = height-2
        for index in range(span):
            box_array[index+1,0] = vertical
            box_array[index+1,width-1] = vertical
    return box_array


def run_4():
    with FullscreenWindow() as win:
        for i in range(1,15):
            win.render_to_terminal(returns_FSArray_boxes(i,i*2))
            time.sleep(.2)

#run_4()



""" Notes on technique 5: like technique 4, but as a generator
    * it works, sorta:
        * sending in (height, width) uses raises a TypeError 'NoneType object is not iterable which
          seems related to the `if height:` check. Well that's how I got around it when just sending
          in height, but `if height and width:` doesn't do it. Maybe an or?
"""

def yields_FSArray_boxes(height, width, max=15):
    top_left = '╒'
    top_right = '╕'
    bottom_left = '╘'
    bottom_right = '╛'
    horizontal = '═'
    vertical = '│'
    for i in range(max):
        if height:
            box_array = fsarray([' ' * width for _ in range(height)])
            # FSArrays are height,width <- weird but true
            box_array[0,0] = top_left
            box_array[0,width-1] = top_right
            box_array[height-1,0] = bottom_left
            box_array[height-1,width-1] = bottom_right
            if width>2:
                span = width-2
                for index in range(span):
                    box_array[0,index+1] = horizontal
                    box_array[height-1, index + 1] = horizontal
            if height>2:
                span = height-2
                for index in range(span):
                    box_array[index+1,0] = vertical
                    box_array[index+1,width-1] = vertical
        height = yield box_array


def run_5():
    with FullscreenWindow() as win:
        i = 1
        box_generator = yields_FSArray_boxes(2,2, max=40)
        for box in box_generator:
            win.render_to_terminal(box)
            i+=1
            box_generator.send(i)
            time.sleep(.2)

# run_5()

""" Notes on technique 6: like technique 5, but trying to get multiple update-able attributes
        * it works, sending in different values of height and width correctly adjusts the height
          and width.
        * has weird NoneType handling since <var> = yield <expr> sometimes sets the <var> to a
          NoneType object, so check for that before assigning to something.
"""


def yields_FSArray_boxes(height = 10, width = 10, max=15):
    top_left = '╒'
    top_right = '╕'
    bottom_left = '╘'
    bottom_right = '╛'
    horizontal = '═'
    vertical = '│'
    i = 0
    while i < max:
        box_array = fsarray([' ' * width for _ in range(height)])
        # FSArrays are height,width <- weird but true
        box_array[0,0] = top_left
        box_array[0,width-1] = top_right
        box_array[height-1,0] = bottom_left
        box_array[height-1,width-1] = bottom_right
        if width>2:
            span = width-2
            for index in range(span):
                box_array[0,index+1] = horizontal
                box_array[height-1, index + 1] = horizontal
        if height>2:
            span = height-2
            for index in range(span):
                box_array[index+1,0] = vertical
                box_array[index+1,width-1] = vertical
        yielded = yield box_array
        if yielded: # handled case when the yield brings back a NoneType
            height, width = yielded[0], yielded[1]
        i += 1


def run_6():
    with FullscreenWindow() as win:
        i = 1
        box_generator = yields_FSArray_boxes(2,2)
        for box in box_generator:
            win.render_to_terminal(box)
            i+=1
            try:
                box_generator.send([i, i*2])
            except StopIteration:
                print('ran past max while trying to send in an item')
            time.sleep(.2)

#run_6()

""" notes on technique 7: trying to get keyboard input rendered into the box
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

def yields_FSArray_boxes(height=40, width=80, contents=''):
    """ A coroutine style generator for creating boxes with borders and content_array
    """
    cursor = [0,0] # used to remember the position in a content_array box
    box_updated = True
    content_string = contents
    content_array = fsarray('')
    while True:
        if box_updated:
            box_array = produce_box_of_size_height_width(height,width)
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
                content_array = string_as_array_of_width(content_string, width - 3) # width-3 because
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
                elif yielded == '<DOWN>' and height >= 3: # don't let the box poof it self
                    height += -1
                elif yielded == '<LEFT>' and width >= 3:
                    width += -1
                elif yielded == '<RIGHT>':
                    width +=1
                else:
                    pass
            box_updated = True


def run_7():
    with FullscreenWindow() as win:
        i = 1
        box_generator = yields_FSArray_boxes()
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

run_7()
