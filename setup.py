# Llat Setup file
from setuptools import setup

setup(
    name='Llat',
    packages=['llat'],
    version='0.0.1',
    desciption='Speedcubing last layer algorithm trainer',
    long_description=open('README.rst').read(),
    author='Jessie Wincek',
    url='https://github.com/jbwincek/Llat',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 1 - Planning',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Education :: Computer Aided Instruction (CAI)',
        'Topic :: Games/Entertainment',
        'Topic :: Games/Entertainment :: Puzzle Games',
        'Natural Language :: English',
    ],
    keywords='speedcubing cubing tools TUI',
    install_requires=[
        'npyscreen',
        'SpeechRecognition>=3.1',
        'pycuber',
    ],
)
