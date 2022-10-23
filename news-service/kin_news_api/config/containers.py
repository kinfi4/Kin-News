from typing import Optional

from dependency_injector import containers, providers, resources

from api.domain.services.ratings import RatingsService
from api.infrastructure.repositories import UserRepository, ChannelRepository
from api.domain.services import UserService, ChannelService
from api.infrastructure.repositories.ratings import RatingsRepository
from kin_news_core.telegram.client import TelegramClientProxy, telegram_client_proxy_creator
from kin_news_core.cache import RedisCache, AbstractCache


class RedisResource(resources.Resource):
    def init(self, host: str, port: int = 6379, password: Optional[str] = None) -> RedisCache:
        return RedisCache.from_settings(host, port, password)


class Repositories(containers.DeclarativeContainer):
    user_repository: providers.Singleton[UserRepository] = providers.Singleton(UserRepository)
    channel_repository: providers.Singleton[ChannelRepository] = providers.Singleton(ChannelRepository)
    ratings_repository: providers.Singleton[RatingsRepository] = providers.Singleton(RatingsRepository)


class Clients(containers.DeclarativeContainer):
    config = providers.Configuration()

    cache_client: providers.Resource[AbstractCache] = providers.Resource(
        RedisResource,
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
    )

    telegram_client: providers.Resource[TelegramClientProxy] = providers.Factory(
        telegram_client_proxy_creator,
        session_sting=config.TELEGRAM_SESSION_STRING,
        api_id=config.TELEGRAM_API_ID,
        api_hash=config.TELEGRAM_API_HASH,
    )


class DomainServices(containers.DeclarativeContainer):
    config = providers.Configuration()

    repositories = providers.DependenciesContainer()
    clients = providers.DependenciesContainer()

    user_service = providers.Singleton(
        UserService,
        user_repository=repositories.user_repository,
    )

    channel_service = providers.Singleton(
        ChannelService,
        user_repository=repositories.user_repository,
        channel_repository=repositories.channel_repository,
        telegram_client=clients.telegram_client,
        cache_client=clients.cache_client,
    )

    rating_service = providers.Singleton(
        RatingsService,
        ratings_repository = repositories.ratings_repository,
    )


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    repositories: providers.Container[Repositories] = providers.Container(
        Repositories
    )

    clients: providers.Container[Clients] = providers.Container(
        Clients,
        config=config,
    )

    domain_services: providers.Container[DomainServices] = providers.Container(
        DomainServices,
        config=config,
        repositories=repositories,
        clients=clients,
    )
