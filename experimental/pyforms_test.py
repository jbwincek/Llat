where = '/usr/local/lib/python3.5/site-packages/'
import sys

if not where in sys.path:
    sys.path.append(where)
import pyforms
from pyforms import BaseWidget
from pyforms.Controls import ControlText
from pyforms.Controls import ControlButton


class SimpleExample6(BaseWidget):
    def __init__(self):
        super(SimpleExample6, self).__init__('Simple example 6')

        # Definition of the forms fields
        self._firstname = ControlText('First name', 'Default value')
        self._middlename = ControlText('Middle name')
        self._lastname = ControlText('Lastname name')
        self._fullname = ControlText('Full name')
        self._button = ControlButton('Press this button')

        self._formset = [{
            'Tab1': ['_firstname', '||', '_middlename', '||', '_lastname'],
            'Tab2': ['_fullname']
        },
            '=', (' ', '_button', ' ')]

        self._fullname.addPopupSubMenuOption('Path',
                                             {
                                                 'Delete': self.__dummyEvent,
                                                 'Edit': self.__dummyEvent,
                                                 'Interpolate': self.__dummyEvent
                                             })

        # Define the window main menu using the property main menu
        self.mainmenu = [
            {'File': [
                {'Open': self.__dummyEvent},
                '-',
                {'Save': self.__dummyEvent},
                {'Save as': self.__dummyEvent}
            ]
            },
            {'Edit': [
                {'Copy': self.__dummyEvent},
                {'Past': self.__dummyEvent}
            ]
            }
        ]

    def __dummyEvent(self):
        print("Menu option selected")


if __name__ == '__main__':
    pyforms.startApp(SimpleExample6)
