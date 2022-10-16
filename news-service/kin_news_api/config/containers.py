from dependency_injector import containers, providers

from api.infrastructure.repositories import UserRepository, ChannelRepository
from api.domain.services import UserService, ChannelService


class Repositories(containers.DeclarativeContainer):
    user_repository: providers.Singleton[UserRepository] = providers.Singleton(UserRepository)
    channel_repository: providers.Singleton[ChannelRepository] = providers.Singleton(ChannelRepository)


class Services(containers.DeclarativeContainer):
    config = providers.Configuration()

    repositories = providers.DependenciesContainer()

    user_service = providers.Singleton(
        UserService,
        user_repository=repositories.user_repository,
    )

    channel_service = providers.Singleton(
        ChannelService,
        user_repository=repositories.user_repository,
        channel_repository=repositories.channel_repository,
    )


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    repositories: providers.Container[Repositories] = providers.Container(
        Repositories
    )

    services: providers.Container[Services] = providers.Container(
        Services,
        config=config,
        repositories=repositories,
    )
