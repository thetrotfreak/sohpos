from enum import StrEnum, auto


class SohposTopics(StrEnum):
    """
    Topics to be used in Flet's default implementation of PubSub
    """

    SOHPOS_TOPIC_AUTHENTICATED = auto()
    SOHPOS_TOPIC_MODE_CHANGED = auto()
