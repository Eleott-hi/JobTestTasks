from datetime import date
from typing import Dict
from uuid import UUID
from src.core.StateMachine import StateMachine
from src.models.Models import Operation, OperationCategory


def parse_id(data: dict) -> str:
    res = input(
        """
    Press Q/q to Quit
    Enter operation id (format: 00000000-0000-0000-0000-000000000000): """
    )

    if "q" == res.lower():
        return "quit"

    try:
        data["id"] = UUID(res)

    except ValueError:
        print("Invalid id. Try again")
        return "id"

    return "check_id"


def check_id(data: dict) -> str:
    try:
        get_operation_cb = data["get_operation_cb"]
        operation: Operation = get_operation_cb(data["id"])

        data["category"] = operation.category
        data["amount"] = operation.amount
        data["operation_date"] = operation.operation_date
        data["description"] = operation.description

    except Exception as e:
        print(f"Error: {e}")
        return "id"

    return "category"


def parse_category(data: dict) -> str:
    default: OperationCategory = data["category"]

    res = input(
        """
    Press Q/q to Quit
    Enter operation category (1 - income, 2 - outcome, default: {default}): """.format(
            default=default.value
        )
    )

    if "q" == res.lower():
        return "quit"

    if not res:
        return "amount"

    if res not in ["1", "2"]:
        print("Invalid category. Try again")
        return "category"

    data["category"] = "income" if res == "1" else "outcome"

    return "amount"


def parse_amount(data: dict) -> str:
    default = data["amount"]

    res = input(
        """
    Press Q/q to Quit
    Enter operation amount (default: {default}): """.format(
            default=default
        )
    )

    if "q" == res.lower():
        return "quit"

    try:
        data["amount"] = float(res) if res else default
    except ValueError:
        print("Invalid amount. Try again")
        return "amount"

    return "date"


def parse_operation_date(data: dict) -> str:
    default = data["operation_date"]
    res = input(
        """
    Press Q/q to Quit
    Enter operation date (YYYY-MM-DD, default: {default}): """.format(
            default=default
        )
    )

    if "q" == res.lower():
        return "quit"

    try:
        data["operation_date"] = date.fromisoformat(res) if res else default
    except ValueError:
        print("Invalid date. Try again")
        return "date"

    return "description"


def parse_description(data: dict) -> str:
    default = data["description"]

    output = default if len(default) < 50 else default[:50] + "..."

    res = input(
        """
    Press Q/q to Quit
    Enter operation description (default: {output}): """.format(
            output=output
        )
    )

    if "q" == res.lower():
        return "quit"

    data["description"] = res if res else default

    return "end"


def get_state_machine(data: Dict = {}) -> StateMachine:
    return StateMachine(
        start_state="id",
        end_states=["quit", "end"],
        states={
            "id": parse_id,
            "check_id": check_id,
            "category": parse_category,
            "amount": parse_amount,
            "date": parse_operation_date,
            "description": parse_description,
        },
        data=data,
    )
