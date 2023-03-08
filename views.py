

class Report:
    SHORTCUT = 'r'
    DESCRIPTION = 'RAPORTY'

    def raport_month(self, month, year):
        pass

    def raport_recent(self):
        pass

    @staticmethod
    def get_timeframe():
        year = input('Podaj z którego roku chcesz wyświetlić statystyki [YYYY]')
        month = input('Podaj z którego roku chcesz wyświetlić statystyki [MM]: ')
        return (month, year)

    def print_report_menu(self):
        print('Jaki raport chcesz wyświetlić?')
        print('[M] - z konkretnego miesiąca')
        print('[R] - ostatnio dodane produkty')
        self.get_report_option()

    def get_report_option(self):
        option = input('Wybierz opcje: ')
        while True:
            if option.lower() == 'm':
                self.get_timeframe()
                break
            elif option.lower() == 'r':
                self.raport_recent()
                break
            else:
                print('Niepoprawna opcja. Spróbuj ponownie.')



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
