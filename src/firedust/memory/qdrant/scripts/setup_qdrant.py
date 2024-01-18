"Sets up a QDRANT to work with firedust."
import firedust.memory.qdrant.connect as connect_qdrant


def create_memories_collection() -> None:
    ...


def create_assistants_collection() -> None:
    ...


if __name__ == "__main__":
    connect_qdrant.premise("localhost", 6333)
    create_memories_collection()
    create_assistants_collection()
