from langchain.schema import BaseMessage, ChatMessage


class PlayerMessage(ChatMessage):
    is_user: bool = False
    name: str

    def __init__(self, name: str, **kwargs):
        kwargs.update(role=name)
        super().__init__(**kwargs)

    @property
    def type(self) -> str:
        return self.name
