
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


@asyncio.coroutine
def wait_for_keystroke():
    with Input() as input_generator:
        yield from input_generator

async def gen_test_3():
    while True:
        key = await wait_for_keystroke()
        print('got: {}'.format(key))
        if key == 'q':
            break


def run_3():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(gen_test_3())
    loop.close()
#  run_3()



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

run_5()