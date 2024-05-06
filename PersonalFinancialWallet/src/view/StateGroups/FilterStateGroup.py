from typing import Dict, Union
from src.core.StateMachine import StateMachine
from src.models.Filters import AmountFilter, CategoryFilter, DateFilter, DescriptionFilter


FILTER_PROTMPT = """
Usage: 
                <Filter by> <Comporator> <Value>
Filter by: 
                1 - category, 2 - amount, 3 - date, 4 - description
Comporators:
                For category: == , !=
                For amount and date: == , !=, <, >, <=, >=
                For string: == , !=, includes, excludes
<Value>: 
                number or string to compare with
Example: 
                1 != income
                2 > 100
                3 >= 2022-01-01
                4 == description
                4 includes description1 

Press Q/q to Quit

"""


def parse_filter(data: dict) -> str:
    res = input(FILTER_PROTMPT + "Enter filter: ")

    if "q" == res.lower():
        return "quit"

    tokens = res.strip().split()

    if len(tokens) != 3:
        print("Invalid filter. Should be: <Filter by> <Comporator> <Value>")
        return "filter"

    field, comp, value = tokens
    fields = {
        "1": CategoryFilter,
        "2": AmountFilter,
        "3": DateFilter,
        "4": DescriptionFilter,
    }

    if field not in fields:
        print(f'Invalid filter by value: "{field}". Should be between 1 - 4')
        return "filter"

    try:
        filter_class = fields[field]

        filter: Union[CategoryFilter, AmountFilter, DateFilter, DescriptionFilter] = (
            filter_class(comparator=comp, value=value)
        )
        data["filter"] = filter

    except ValueError as e:
        print(f"Invalid filter: {e}")
        return "filter"

    return "end"


def get_state_machine(data: Dict = {}) -> StateMachine:
    return StateMachine(
        start_state="filter",
        end_states=["quit", "end"],
        states={"filter": parse_filter},
        data=data,
    )