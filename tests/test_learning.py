import os

import pytest

from firedust.assistant import Assistant


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
def test_learn_fast() -> None:
    text = """
    Demand for our data center systems and products has surged over the last three quarters and our demand visibility extends into next year. To
    meet this expected demand, we have increased our purchase obligations with existing suppliers, added new suppliers, and entered into prepaid
    supply and capacity agreements. These increased purchase volumes, the number of suppliers, and the integration of new suppliers into our
    supply chain, may create more supply chain complexity and execution risk. We expect to continue to enter into supplier and capacity
    arrangements and expect our supply to increase each quarter through next year. We may incur inventory provisions or impairments if our
    inventory or supply or capacity commitments exceed demand for our products or demand declines.
    Our customer orders and longer-term demand estimates may change or may not be correct, as we have experienced in the past. Product
    transitions are complex and can impact our revenue as we often ship both new and prior architecture products simultaneously and we and our
    channel partners prepare to ship and support new products. Due to our product introduction cycles, we are almost always in various stages of
    transitioning the architecture of our Data Center, Professional Visualization, and Gaming products. We will have a broader and faster Data
    Center product launch cadence to meet a growing and diverse set of AI opportunities. The increased frequency of these transitions may magnify
    the challenges associated with managing our supply and demand due to long manufacturing lead times. Qualification time for new products,
    customers anticipating product transitions and channel partners reducing channel inventory of prior architectures ahead of new product
    introductions can create reductions or volatility in our revenue. We have experienced and may in the future experience reduced demand for
    current generation architectures when customers anticipate transitions, and we may be unable to sell multiple product architectures at the same
    time for current and future architecture transitions. If we are unable to execute our architectural transitions as planned for any reason, our
    financial results may be negatively impacted. In addition, the bring up of new product architectures is complex due to functionality challenges
    and quality concerns not identified in manufacturing testing. These product quality issues may incur costs, increase our warranty costs, and
    delay further production of our architecture. Deployment of new products to customers creates additional challenges due to the complexity of our
    technologies, which has impacted and may in the future impact the timing of customer purchases or otherwise impact our demand. While we
    have managed prior product transitions and have previously sold multiple product architectures at the same time, these transitions are difficult,
    may impair our ability to predict demand and impact our supply mix, and we may incur additional costs.
    """

    # test learning
    assistant = Assistant.create()
    assistant.learn.fast(text)

    # test memories recall
    memories = assistant.memory.recall("Info about purchase obligations.", limit=10)
    expected_recall = "we have increased our purchase obligations with existing suppliers, added new suppliers, and entered into prepaid supply and capacity agreements."
    assert any(
        expected_recall in memory.context.replace("\n   ", "") for memory in memories
    )

    # remove test assistant
    Assistant.delete(assistant_id=assistant.config.id, confirm_delete=True)


def test_learn_pdf() -> None:
    pass


def test_learn_url() -> None:
    pass


def test_learn_image() -> None:
    pass


def test_learn_audio() -> None:
    pass


def test_learn_video() -> None:
    pass


def test_learn_fast_large_text() -> None:
    text = """

    """
    # assistant = firedust.assistant.create()

    # firedust.assistant.delete(assistant.config.id)
    pass
