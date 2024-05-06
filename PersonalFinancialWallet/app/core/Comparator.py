from typing import Any

def compare(original_value: Any, compared_value: Any, comparator: str) -> bool:
    match comparator:
        case "==":
            return original_value == compared_value
        case "!=":
            return original_value != compared_value
        case "<":
            return original_value < compared_value
        case ">":
            return original_value > compared_value
        case "<=":
            return original_value <= compared_value
        case ">=":
            return original_value >= compared_value
        case "includes":
            return compared_value in original_value
        case "excludes":
            return compared_value not in original_value
        case _:
            raise ValueError(f"Comparator {comparator} not supported")
