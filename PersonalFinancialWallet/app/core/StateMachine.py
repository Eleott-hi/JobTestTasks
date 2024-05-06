from typing import Callable, Dict, List


class StateMachine:
    def __init__(
        self,
        start_state: str,
        end_states: List[str],
        states: Dict[str, Callable],
        data: Dict = {},
    ):
        self.states = states
        self.start_state = start_state
        self.end_states = end_states
        self.data = data

    def process(self) -> tuple[str, Dict]:
        current_state = self.start_state

        while current_state not in self.end_states:
            cb = self.states[current_state]
            current_state = cb(self.data)

        return current_state, self.data
