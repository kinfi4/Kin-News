from typing import Optional

from pydantic import BaseModel, validator

from kin_news_core.telegram.entities import ChannelEntity
from api.domain.utils import truncate_channel_link_to_username


class ChannelPostEntity(BaseModel):
    link: str

    _extract_link = validator('link', pre=True, allow_reuse=True)(truncate_channel_link_to_username)


class ChannelGetEntity(ChannelEntity):
    profile_photo_url: Optional[str]

    _extract_link = validator('link', pre=True, allow_reuse=True)(truncate_channel_link_to_username)
