import blessings

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


run_2()