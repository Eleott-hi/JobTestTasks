from src.core.Backend import Backend
from src.view.MainMenu import MainMenu


class Application:
    def __init__(self) -> None:
        self.backend = Backend()
        self.view = MainMenu(self.backend)

    def run(self):
        self.view.show()
