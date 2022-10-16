from typing import Optional

from pydantic import BaseModel


class ChannelPostEntity(BaseModel):
    link: str


class ChannelGetEntity(ChannelPostEntity):
    display_name: Optional[str] = None
