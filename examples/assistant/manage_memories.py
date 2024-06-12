import firedust

sam = firedust.assistant.create(name="Sam")
# or load an existing assistant
sam = firedust.assistant.load(name="Sam")

# add some data to the memory
data = [
    "To reach Mordor, follow the path through the Mines of Moria.",
    "The ring must be destroyed in the fires of Mount Doom.",
]
for item in data:
    sam.learn.fast(item)

# list all available memories
memory_ids = sam.memory.list(limit=100, offset=0)

# load memory content
memories = sam.memory.get(memory_ids[:10])

# recall memories by query
query = "Guidance to reach Mordor."
mordor_memories = sam.memory.recall(query)

# add selected memories to another assistant
frodo = firedust.assistant.create(name="Frodo")
frodo.memory.add(mordor_memories)

# share all memories with another assistant, this
# is a full memory sync and applies to existing memories as well
# as the ones created in the future
sam.memory.share(assistant_receiver="Frodo")

# stop sharing memories
sam.memory.unshare(assistant_receiver="Frodo")

# delete memories
sam.memory.delete(memory_ids[:10])
