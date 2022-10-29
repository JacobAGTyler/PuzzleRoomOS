

class Interface:
    def __init__(self, trigger_references: list[str]):
        self._trigger_references = trigger_references
        self.actions = []
