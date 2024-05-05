from datetime import date
from typing import Dict
from src.core.StateMachine import StateMachine


def parse_category(data: dict) -> str:
    res = input(
        """
    Press Q/q to Quit
    Enter operation category (1 - income, 2 - outcome): """
    )

    if "q" == res.lower():
        return "quit"

    if res not in ["1", "2"]:
        print("Invalid category. Try again")
        return "category"

    data["category"] = "income" if res == "1" else "outcome"

    return "amount"


def parse_amount(data: dict) -> str:
    res = input(
        """
    Press Q/q to Quit
    Enter operation amount: """
    )

    if "q" == res.lower():
        return "quit"

    try:
        data["amount"] = float(res)
    except ValueError:
        print("Invalid amount. Try again")
        return "amount"

    return "date"


def parse_operation_date(data: dict) -> str:
    res = input(
        """
    Press Q/q to Quit
    Enter operation date (YYYY-MM-DD, default: today): """
    )

    if "q" == res.lower():
        return "quit"

    try:
        data["operation_date"] = date.fromisoformat(res) if res else date.today()
    except ValueError:
        print("Invalid date. Try again")
        return "date"

    return "description"


def parse_description(data: dict) -> str:
    res = input(
        """
    Press Q/q to Quit
    Enter operation description: """
    )

    if "q" == res.lower():
        return "quit"

    data["description"] = res

    return "end"


def get_state_machine(data: Dict = {}) -> StateMachine:
    return StateMachine(
        start_state="category",
        end_states=["quit", "end"],
        states={
            "category": parse_category,
            "amount": parse_amount,
            "date": parse_operation_date,
            "description": parse_description,
        },
        data=data,
    )
