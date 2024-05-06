from uuid import UUID, uuid4
from typing import List

from src.models.Models import WalletData, OperationWrite, Operation
from src.core.Comparator import compare

class Wallet:
    def __init__(self) -> None:
        self.data = WalletData(operations=[])

    def __get_operation_by_id(self, id: UUID) -> tuple[Operation, int]:
        for idx, operation in enumerate(self.data.operations):
            if operation.id == id:
                return operation, idx

        raise ValueError(f'Operation with id "{id}" not found')

    def get_data(self) -> WalletData:
        return self.data.model_copy()

    def set_data(self, data: WalletData) -> None:
        self.data = data.model_copy()

    def add_operation(self, data: OperationWrite) -> None:
        data = Operation(id=uuid4(), **data.model_copy().model_dump())
        self.data.operations.append(data)

    def delete_operation(self, id: UUID) -> None:
        _, idx = self.__get_operation_by_id(id)
        del self.data.operations[idx]

    def update_operation(self, data: Operation) -> None:
        _, idx = self.__get_operation_by_id(data.id)

        self.data.operations[idx] = Operation(
            **data.model_dump(),
        )

    def get_operations(self, filters: List | None = None) -> List[Operation]:
        if filters is None:
            filters = []

        def is_match(operation: Operation) -> bool:
            operation = operation.model_dump()

            for filter in filters:
                compare_field = filter.Meta.compare_field
                is_match = compare(
                    operation[compare_field], filter.value, filter.comparator
                )
                if not is_match:
                    return False

            return True

        filtered_operations = [
            op.model_copy() for op in filter(is_match, self.data.operations)
        ]
        return filtered_operations

    def get_operation(self, id: UUID) -> Operation:
        operation, _ = self.__get_operation_by_id(id)
        return operation.model_copy()

    def check_id(self, id: UUID) -> bool:
        try:
            self.__get_operation_by_id(id)
            return True

        except ValueError:
            return False
