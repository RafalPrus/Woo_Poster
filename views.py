

class Report():
    SHORTCUT = 'r'
    DESCRIPTION = 'RAPORTY'

    def raport_month(self, month, year):
        pass

    def raport_recent(self):
        pass

class Exit():
    SHORTCUT = 'x'
    DESCRIPTION = 'ZAKOŃCZ PROGRAM'


    @staticmethod
    def say_goodbye():
        print('Do zobaczenia!')

class Validator_Screen():
    SHORTCUT = 's'
    DESCRIPTION = 'SPRAWDŹ POPRAWNOŚĆ FOLDERÓW'

class MainApp_Screen():
    SHORTCUT = 'd'
    DESCRIPTION = 'DODAJ PRODUKTY NA STRONĘ'


class MainMenu():
    MENU = {
        Validator_Screen.SHORTCUT: Validator_Screen(),
        MainApp_Screen.SHORTCUT: MainApp_Screen(),
        Report.SHORTCUT: Report(),
        Exit.SHORTCUT: Exit()
    }
    def __init__(self):
        self.draw_menu()


    def draw_menu(self):
        print("Powiedz co chcesz zrobić: ")
        for shortcut, screen in MainMenu.MENU.items():
            print(f"[{shortcut}] - {screen.DESCRIPTION}")

    @staticmethod
    def get_screen():
        option = None
        while option not in MainMenu.MENU:
            option = input("Wybierz opcję: ")
        return MainMenu.MENU[option]









