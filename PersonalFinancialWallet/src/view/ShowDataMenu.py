from pathlib import Path
import sys
from typing import Any, Callable, List
from uuid import UUID

from consolemenu import MenuFormatBuilder, ConsoleMenu, Screen, SelectionMenu
from consolemenu.format import MenuBorderStyleType
from consolemenu.items import MenuItem, FunctionItem
from src.core.Backend import Backend
from src.core.StateMachine import StateMachine
from src.models.Models import Operation, OperationWrite

import src.view.StateGroups.AddOperationStateGroup as AddSG
import src.view.StateGroups.FilterStateGroup as FilterSG
import src.view.StateGroups.UpdateOperationStateGroup as UpdateSG
from src.view.StateGroups.UpdateOperationStateGroup import parse_id


class ShowDataMenu:
    def __init__(self, backend: Backend):
        self.backend = backend
        self.filters = []

        menu = ConsoleMenu(
            title="Show Menu",
            subtitle="Here you can see all your wallet operations or filter them by category, date, amount, etc.",
            prologue_text="Set the operation you want to perform",
            formatter=self.__get_format(),
            clear_screen=False,
            exit_menu_char="q",
        )

        menu.append_item(
            FunctionItem("Show without filters", self.show_without_filters)
        )
        menu.append_item(FunctionItem("Show with filters", self.show_with_filters))
        menu.append_item(FunctionItem("Add filter", self.add_filter))
        menu.append_item(FunctionItem("Reset filters", self.reset_filters))

        self.menu = menu

        self.update_menu()

    def get_menu(self):
        return self.menu

    def update_menu(self):
        filters = list(map(str, self.filters))
        self.menu.epilogue_text = f"Current filters: {filters}"

    def show_without_filters(self):
        operations = self.backend.get_wallet().get_operations()
        self.show_data(operations)

    def show_with_filters(self):
        operations = self.backend.get_wallet().get_operations(self.filters)
        self.show_data(operations)

    def show_data(self, operations: List[Operation]):
        if len(operations) == 0:
            print("No operations found")

        for operation in operations:
            print("===============================================")
            print(operation)

    def reset_filters(self):
        self.filters = []
        self.update_menu()

    def add_filter(self):
        sm = FilterSG.get_state_machine()
        state, data = sm.process()

        if state == "quit":
            print("Cancelled")
            return

        self.filters.append(data["filter"])

        self.update_menu()

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
            # .show_epilogue_top_border(True)
        )
