from pydantic import BaseModel

from kin_news_core.telegram.entities import ChannelEntity


class ChannelPostEntity(BaseModel):
    link: str


class ChannelGetEntity(ChannelEntity):
    pass
