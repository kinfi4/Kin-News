from datetime import datetime

from faker import Faker
import pytest

from api.domain.entities import GenerateReportEntity
from kin_news_core.telegram.entities import TelegramChannelEntity

faker = Faker()


@pytest.fixture()
def telegram_channel_entity() -> TelegramChannelEntity:
    return TelegramChannelEntity(
        link=faker.words(0),
        title=faker.words(0),
        description=faker.sentence(),
        participants_count="300 K"
    )


@pytest.fixture()
def generate_report_entity() -> GenerateReportEntity:
    return GenerateReportEntity(
        start_date=datetime.now(),
        end_date=datetime.now(),
        channels=["something", "another"]
    )
