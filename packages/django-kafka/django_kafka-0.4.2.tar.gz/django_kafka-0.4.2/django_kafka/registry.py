from typing import TYPE_CHECKING, Type

from django_kafka.exceptions import DjangoKafkaError

if TYPE_CHECKING:
    from django_kafka.consumer import Consumer


class ConsumersRegistry:
    def __init__(self):
        self.__consumers: dict[str, Type[Consumer]] = {}

    def __call__(self):
        def add_to_registry(consumer_cls: Type["Consumer"]) -> Type["Consumer"]:
            self.register(consumer_cls)
            return consumer_cls

        return add_to_registry

    def __getitem__(self, key: str):
        try:
            return self.__consumers[key]
        except KeyError as error:
            raise DjangoKafkaError(f"Consumer `{key}` is not registered.") from error

    def __iter__(self):
        yield from self.__consumers.keys()

    def get_key(self, consumer_cls: Type["Consumer"]) -> str:
        return f"{consumer_cls.__module__}.{consumer_cls.__name__}"

    def register(self, consumer_cls: Type["Consumer"]):
        from django_kafka.retry.consumer import RetryConsumer

        key = self.get_key(consumer_cls)
        self.__consumers[key] = consumer_cls
        if retry_consumer_cls := RetryConsumer.build(consumer_cls):
            self.__consumers[f"{key}.retry"] = retry_consumer_cls
