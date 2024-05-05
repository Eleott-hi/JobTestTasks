import functools
from typing import Dict, List
from uuid import UUID
from app.storage.IFileManager import IFileManager

from app.models.WalletData import WalletData, OperationWrite, Operation


class Wallet:
    def __init__(self) -> None:
        self.data = WalletData(operations=[])

    def __get_operation_by_id(self, id: UUID) -> tuple[Operation, int]:
        for idx, operation in enumerate(self.data.operations):
            if operation.id == id:
                return operation, idx

        raise Exception(f"Operation with id {id} not found")

    def get_data(self) -> WalletData:
        return self.data.model_copy()

    def set_data(self, data: WalletData) -> None:
        self.data = data.model_copy()

    def add_operation(self, data: OperationWrite) -> None:
        data = Operation(**data.model_copy().model_dump())
        self.data.operations.append(data)

    def delete_operation(self, id: UUID) -> None:
        _, idx = self.__get_operation_by_id(id)
        del self.data.operations[idx]

    def update_operation(self, data: Operation) -> None:
        _, idx = self.__get_operation_by_id(data.id)

        self.data.operations[idx] = Operation(
            **data.model_dump(),
        )

    def get_operations(self, filter: Dict | None = None) -> List[Operation]:
        operations = self.data.model_copy().operations

        if filter is None:
            return operations

        def is_match(operation: Operation) -> bool:
            operation = operation.model_dump()

            for key, value in filter.items():
                if key not in operation:
                    raise Exception(f"Invalid filter key {key}")

                if operation.get(key, None) != value:
                    return False

            return True

        filtered_operations = [i for i in operations if is_match(i)]
        return filtered_operations

    def get_operation_by_id(self, id: UUID) -> Operation:
        operation, _ = self.__get_operation_by_id(id)
        return operation.model_copy()
