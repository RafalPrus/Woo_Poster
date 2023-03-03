from main import Application

class Exit():
    SHORTCUT = 'x'
    DESCRIPTION = 'ZAKOŃCZ PROGRAM'

    def __init__(self):
        Exit.say_goodbye()

    @staticmethod
    def say_goodbye(self):
        print('Do zobaczenia!')



class MainMenu():
    MENU = {
        Application.SHORTCUT: Application(),
        '[w] WYŚWIETL RAPORT': RAPORTS,
        Exit.SHORTCUT: Exit()
    }
    def __init__(self):
        self.draw_menu()
        self.get_screen()


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



