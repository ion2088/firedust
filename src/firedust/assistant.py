class Assistant:
    "Assistant base class"

    def __init__(self) -> None:
        "Initialize the Assistant"
        raise NotImplementedError()

    def __repr__(self) -> str:
        "Return a string representation of the Assistant"
        return f"<{self.__class__.__name__}>"

    def learn(self) -> None:
        "Add the given memory to the assistant"
        raise NotImplementedError()

    def forget(self) -> None:
        "Remove the given memory from the assistant"
        raise NotImplementedError()

    def decide(self) -> None:
        "Make a decision about the next action based on the given query"
        raise NotImplementedError()

    def chat(self) -> None:
        "Streaming chat with the assistant"
        raise NotImplementedError()

    def complete(self) -> None:
        "Complete the given query"
        raise NotImplementedError()
