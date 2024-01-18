from qdrant_client import QdrantClient

QDRANT: QdrantClient | None = None


def cloud(host: str, api_key: str) -> None:
    "Connect to a Qdrant cloud instance"
    global QDRANT
    QDRANT = QdrantClient(host=host, api_key=api_key)


def premise(host: str, port: int) -> None:
    "Connect to a Qdrant premise instance"
    global QDRANT
    QDRANT = QdrantClient(host=host, port=port)
