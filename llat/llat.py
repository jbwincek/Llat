import npyscreen as ns
import time

class hi_popup(ns.Popup):
    # TODO make this actually work
    def create(self):
        self.add(ns.TitleText, name= 'hi')
        time.sleep(1)
        self.editing =False


class Llat_applications(ns.NPSAppManaged):
    # The main application
    def onStart(self):
        self.registerForm('MAIN', MainMenu())  # registerForm requires the actual function object, rather than the def
        self.registerForm('hi', hi_popup())

    def onCleanExit(self):
        ns.notify_wait("Goodbye!")


class MainMenu(ns.Form):
    # Main Menu consisting of a list of options to choose from
    def create(self):
        self.add(ns.SelectOne, name='Options', max_height=4, values=['train', 'help', 'quit'])
        self.add(ns.TitleText, name='form name')
        self.add_handlers({
                        "^D": exit, })  # for keyboard commands '^' is really just a carrot, and D counts as un-shift-ed

    def after_editing(self):
        # TODO make this actually close the program like it should
        self.parentApp.setNextForm(None)


def main():
   app = Llat_applications().run()  # this is documented two different ways, not sure which way to do it









