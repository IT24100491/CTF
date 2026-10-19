import re
from typing import Any


def matches(value: Any, condition: Any) -> bool:
    if isinstance(condition, dict):
        for op, operand in condition.items():
            if op == "$ne":
                if value == operand:
                    return False
            elif op == "$eq":
                if value != operand:
                    return False
            elif op == "$gt":
                if value is None or not value > operand:
                    return False
            elif op == "$gte":
                if value is None or not value >= operand:
                    return False
            elif op == "$lt":
                if value is None or not value < operand:
                    return False
            elif op == "$lte":
                if value is None or not value <= operand:
                    return False
            elif op == "$in":
                if value not in operand:
                    return False
            elif op == "$regex":
                if not re.search(operand, value or ""):
                    return False
            elif op == "$exists":
                if (value is not None) != bool(operand):
                    return False
            else:
                return False
        return True

    return value == condition


def find_one(collection: list[dict], query: dict) -> dict | None:
    for document in collection:
        if all(matches(document.get(key), expected) for key, expected in query.items()):
            return document
    return None
