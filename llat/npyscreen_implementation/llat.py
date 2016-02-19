import npyscreen as ns
import time


class MainMenu(ns.Form):
    # Main Menu consisting of a list of options to choose from
    def create(self):
        self.how_exited_handers[ns.wgwidget.EXITED_ESCAPE] = self.exit_application
        self.add(ns.TitleText, name='form name')
        self.add(ns.SelectOne, name='Options', max_height=4, values=['train', 'help', 'quit'])
        # self.add_handlers({
        #                 "^d": self.exit_application(), })

    def after_editing(self):
        pass

    def exit_application(self):
        self.parentApp.setNextForm(None)
        self.editing = False


class LlatApplication(ns.NPSAppManaged):
    # The main application
    def onStart(self):
        self.addForm('MAIN', MainMenu, name='Llat: Last layer Algorithm Trainer - Main Menu')

    def onCleanExit(self):
        ns.notify_wait("Goodbye!")


def main():
    LlatApplication().run(fork=False)  # this is documented two different ways, not sure which way to do it









