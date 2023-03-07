

class Report:
    SHORTCUT = 'r'
    DESCRIPTION = 'RAPORTY'

    def raport_month(self, month, year):
        pass

    def raport_recent(self):
        pass


class Exit:
    SHORTCUT = 'x'
    DESCRIPTION = 'ZAKOŃCZ PROGRAM'

    @staticmethod
    def say_goodbye():
        print('Do zobaczenia!')


class ValidatorScreen:
    SHORTCUT = 's'
    DESCRIPTION = 'SPRAWDŹ POPRAWNOŚĆ FOLDERÓW'


class MainAppScreen:
    SHORTCUT = 'd'
    DESCRIPTION = 'DODAJ PRODUKTY NA STRONĘ'


class MainMenu:
    MENU = {
        ValidatorScreen.SHORTCUT: ValidatorScreen(),
        MainAppScreen.SHORTCUT: MainAppScreen(),
        Report.SHORTCUT: Report(),
        Exit.SHORTCUT: Exit()
    }

    def __init__(self):
        self.draw_menu()

    @staticmethod
    def draw_menu():
        print("Powiedz co chcesz zrobić: ")
        for shortcut, screen in MainMenu.MENU.items():
            print(f"[{shortcut}] - {screen.DESCRIPTION}")

    @staticmethod
    def get_screen():
        option = None
        while option not in MainMenu.MENU:
            option = input("Wybierz opcję: ")
        return MainMenu.MENU[option]
