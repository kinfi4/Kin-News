from dependency_injector import containers, providers, resources
from pymongo import MongoClient

from api.infrastructure.repositories import (
    ReportsMongoRepository,
    IReportRepository,
    ReportsAccessManagementRepository,
    UserRepository,
)
from api.domain.services import ManagingReportsService, IGeneratingReportsService, GeneratingReportsService, UserService
from kin_news_core.telegram import TelegramClientProxy


class MongodbRepositoryResource(resources.Resource):
    def init(self, connection_string: str) -> ReportsMongoRepository:
        client = MongoClient(connection_string)

        return ReportsMongoRepository(mongo_client=client)


class Repositories(containers.DeclarativeContainer):
    config = providers.Configuration()

    reports_repository: providers.Resource[IReportRepository] = providers.Resource(
        MongodbRepositoryResource,
        connection_string=config.MONGO_DB_CONNECTION_STRING,
    )

    reports_access_management_repository: providers.Singleton[ReportsAccessManagementRepository] = providers.Singleton(
        ReportsAccessManagementRepository,
    )

    user_repository: providers.Singleton[UserRepository] = providers.Singleton(
        UserRepository,
    )


class Clients(containers.DeclarativeContainer):
    config = providers.Configuration()

    telegram_client: providers.Factory[TelegramClientProxy] = providers.Factory(
        TelegramClientProxy,
        session_str=config.TELEGRAM_SESSION_STRING,
        api_id=config.TELEGRAM_API_ID,
        api_hash=config.TELEGRAM_API_HASH,
    )


class Services(containers.DeclarativeContainer):
    config = providers.Configuration()
    repositories = providers.DependenciesContainer()
    clients = providers.DependenciesContainer()

    managing_reports_service: providers.Singleton[ManagingReportsService] = providers.Singleton(
        ManagingReportsService,
        reports_repository=repositories.reports_repository,
        reports_access_management_repository=repositories.reports_access_management_repository,
    )

    generating_reports_service: providers.Factory[IGeneratingReportsService] = providers.Factory(
        GeneratingReportsService,
        telegram_client=clients.telegram_client,
        reports_repository=repositories.reports_repository,
        report_access_repository=repositories.reports_access_management_repository,
    )

    user_service: providers.Singleton[UserService] = providers.Singleton(
        UserService,
        access_repository=repositories.user_repository,
    )


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    repositories: providers.Container[Repositories] = providers.Container(
        Repositories,
        config=config,
    )

    clients: providers.Container[Clients] = providers.Container(
        Clients,
        config=config,
    )

    services: providers.Container[Services] = providers.Container(
        Services,
        config=config,
        repositories=repositories,
        clients=clients,
    )
