from pydantic import BaseModel, Field

from api.models import PossibleRating


class ChannelRateEntity(BaseModel):
    channel_link: str = Field(..., alias='channelLink')
    rating: PossibleRating

    class Config:
        allow_population_by_field_name = True


class Rating(BaseModel):
    channel_link: str = Field(..., alias='channelLink')
    my_rate: PossibleRating = Field(..., alias='myRate')
    total_rates: int = Field(..., alias='totalRates')
    average_rating: float = Field(..., alias='averageRating')

    class Config:
        allow_population_by_field_name = True
