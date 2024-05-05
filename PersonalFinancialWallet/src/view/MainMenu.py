from pathlib import Path
import sys
from typing import Any, Callable
from uuid import UUID

from consolemenu import MenuFormatBuilder, ConsoleMenu, Screen, SelectionMenu
from consolemenu.format import MenuBorderStyleType
from consolemenu.items import MenuItem, FunctionItem, SubmenuItem
from src.core.Backend import Backend
from src.core.StateMachine import StateMachine
from src.models.Models import Operation, OperationWrite

from src.view.ShowDataMenu import ShowDataMenu
import src.view.StateGroups.AddOperationStateGroup as AddSG
import src.view.StateGroups.UpdateOperationStateGroup as UpdateSG
from src.view.StateGroups.UpdateOperationStateGroup import parse_id
import src.view.StateGroups.DeleteOperationStateGroup as DeleteSG


class MainMenu:
    def __init__(self, backend: Backend):
        self.backend = backend
        self.show_submenu = ShowDataMenu(backend).get_menu()

        menu = ConsoleMenu(
            title="Main Menu",
            subtitle="This is the main menu to perform operations with your wallet.\nCheck it out!",
            prologue_text="Select the operation you want to perform",
            formatter=self.__get_format(),
            clear_screen=False,
            exit_menu_char="q",
        )

        menu.append_item(SubmenuItem("Show wallet data", submenu=self.show_submenu))
        menu.append_item(FunctionItem("Add a new operation", self.add_operation))
        menu.append_item(FunctionItem("Update an operation", self.update_operation))
        menu.append_item(FunctionItem("Delete an operation", self.delete_operation))
        menu.append_item(
            FunctionItem("Load wallet operations from file", self.load_data)
        )
        menu.append_item(FunctionItem("Save wallet operations to file", self.save_data))

        self.menu = menu
        self.update_menu()

    def show(self):
        # self.menu.show()
        self.menu.start()
        self.menu.join()

    def __get_format(self):
        return (
            MenuFormatBuilder()
            .set_border_style_type(MenuBorderStyleType.DOUBLE_LINE_BORDER)
            # .set_prompt("SELECT>")
            .set_title_align("center")
            .set_subtitle_align("center")
            .set_left_margin(4)
            .set_right_margin(4)
            .show_header_bottom_border(True)
        )

    def update_menu(self):
        self.menu.epilogue_text = "Wallet operations: {}".format(
            len(self.backend.wallet.get_operations([]))
        )

    def save_data(self):
        while True:
            screen = self.menu.screen
            file = screen.input("\nq - Quit\nEnter file (default: wallet.json): ")

            if "q" == file.lower():
                print("Cancelled")
                return

            try:
                file = file or "wallet.json"
                self.backend.save(file)
                screen.println("File saved successfully")
                self.update_menu()
                return

            except Exception as e:
                screen.println(f"Error saving file: {e}")

    def load_data(self):
        while True:
            screen = self.menu.screen
            file = screen.input("\nq - Quit\nEnter file (default: wallet.json): ")

            if "q" == file.lower():
                print("Cancelled")
                return

            try:
                file = file or "wallet.json"
                self.backend.load(file)
                screen.println("File loaded successfully")
                self.update_menu()
                return

            except Exception as e:
                screen.println(f"Error loading file: {e}")

    def show_wallet_data(self):
        operations = self.backend.wallet.get_operations()
        screen = self.menu.screen

        for operation in operations:
            screen.println("===============================================")
            screen.println(operation)

    def add_operation(self):
        sm = AddSG.get_state_machine()
        state, data = sm.process()

        if state == "quit":
            print("Cancelled")
            return

        operation = OperationWrite(**data)
        self.backend.wallet.add_operation(operation)

        self.update_menu()
        print("Operation added successfully")

    def update_operation(self):
        sm = UpdateSG.get_state_machine(
            data=dict(get_operation_cb=self.backend.wallet.get_operation)
        )
        state, data = sm.process()

        if state == "quit":
            print("Cancelled")
            return

        del data["get_operation_cb"]

        self.backend.wallet.update_operation(Operation(**data))
        self.update_menu()
        print("Operation updated successfully")

    def delete_operation(self):
        sm = DeleteSG.get_state_machine(dict(id_checker=self.backend.wallet.check_id))

        state, data = sm.process()

        if state == "quit":
            print("Cancelled")
            return

        del data["id_checker"]

        self.backend.wallet.delete_operation(**data)
        self.update_menu()
        print("Operation deleted successfully")

    def parse(s, key: Callable = str, default: Any = None) -> Any:
        return key(s or default)
