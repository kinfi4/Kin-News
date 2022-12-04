from unittest.mock import MagicMock

import pytest

from api.tests.fakes import FakePredictor, FakeTelegramClient


@pytest.fixture()
def mock_reports_repo(application):
    with application.repositories.reports_repository.override(MagicMock()):
        yield application.repositories.reports_repository

    application.repositories.reports_repository.reset_override()


@pytest.fixture()
def mock_iam_repo(application):
    with application.repositories.reports_access_management_repository.override(MagicMock()):
        yield application.repositories.reports_access_management_repository

    application.repositories.reports_access_management_repository.reset_override()


@pytest.fixture()
def mock_telegram_client(application):
    with application.clients.telegram_client.override(FakeTelegramClient()):
        yield application.clients.telegram_client

    application.clients.telegram_client.reset_override()


@pytest.fixture()
def mock_predictor(application):
    with application.predicting.predictor.override(FakePredictor()):
        yield application.predicting.predictor

    application.predicting.predictor.reset_override()


@pytest.fixture()
def generate_report_service(application, mock_reports_repo, mock_iam_repo, mock_telegram_client, mock_predictor):
    yield application.services.generating_reports_service


@pytest.fixture()
def report_service(application, mock_reports_repo, mock_iam_repo, mock_telegram_client, mock_predictor):
    yield application.services.managing_reports_service
