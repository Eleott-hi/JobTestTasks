from typing import Callable


class MenuItem:
    def __init__(self, description: str, action: Callable) -> None:
        self.description = description
        self.action = action

    def __str__(self) -> str:
        return self.description


class Menu:
    def __init__(self, title: str,stack : list["Menu"], data: dict = None) -> None:
        self.items = {}
        
        stack.append(self)
        self.stack = stack

        self.title = title
        self.data = data or {}

    def add_item(self, items: MenuItem, trigger: str = None) -> None:
        self.items[trigger] = items

    def show(self) -> None:
        print()
        print(self.title)
        print()
        for trigger, item in self.items.items():
            print(f"{trigger}. {item}")
        print()

    def process_input(self, char: str, stack: list["Menu"]) -> None:
        if char == "q":
            stack.clear()
        elif char == "b":
            stack.pop()
        elif char in self.items:
            self.items[char].action()
        else:
            print("Invalid input")
