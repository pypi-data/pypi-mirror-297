from pydantic import BaseModel


class NodeDescription(BaseModel):
    name: str
    description: str
    inputs: dict[str, str]
