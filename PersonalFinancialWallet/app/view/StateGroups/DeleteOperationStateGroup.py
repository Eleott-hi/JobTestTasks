from typing import Callable, Dict
from uuid import UUID
from app.core.StateMachine import StateMachine


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
        get_operation_cb: Callable = data["id_checker"]
        _ = get_operation_cb(data["id"])

    except Exception as e:
        print(f"Error: {e}")
        return "id"

    return "end"


def get_state_machine(data: Dict = {}) -> StateMachine:
    return StateMachine(
        start_state="id",
        end_states=["quit", "end"],
        states={
            "id": parse_id,
            "check_id": check_id,
        },
        data=data,
    )
