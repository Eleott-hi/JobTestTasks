class StateMachine:
    def __init__(self):
        self.handlers = {}
        self.startState = None
        self.endStates = []

    def add_state(self, name, handler, end_state=False):
        self.handlers[name] = handler
        if end_state:
            self.endStates.append(name)

    def set_start(self, name):
        self.startState = name

    def run(self, cargo):
        try:
            handler = self.handlers[self.startState]
        except:
            raise RuntimeError("must call .set_start() before .run()")
        if not self.endStates:
            raise RuntimeError("at least one state must be an end_state")

        while True:
            (newState, cargo) = handler(cargo)
            if newState in self.endStates:
                print(f"reached {newState}")
                break
            else:
                handler = self.handlers[newState]
