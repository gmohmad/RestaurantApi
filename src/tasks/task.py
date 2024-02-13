import asyncio

from celery import Celery

from src.config import (
    RABBITMQ_DEFAULT_PASS,
    RABBITMQ_DEFAULT_PORT,
    RABBITMQ_DEFAULT_USER,
    RABBITMQ_HOST,
)
from src.tasks.parser import Parser
from src.tasks.synchronizer import SynchronizerRepo

celery = Celery(
    'task',
    broker=(
        f'amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@{RABBITMQ_HOST}:{RABBITMQ_DEFAULT_PORT}'
    ),
)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs) -> None:
    """Добавление периодичной задачи для Celery worker"""
    sender.add_periodic_task(
        15.0, sync_database, name='synchronize sheet and db every 15s'
    )


async def task_setup() -> None:
    """Настройка для Celery задачи"""
    parser = Parser()
    parsed_data = await parser.parser()
    synchronizer = SynchronizerRepo(parsed_data)
    await synchronizer.run_synchronization()


@celery.task(default_retry_delay=15)
def sync_database() -> None:
    """Задача синхронизации бд с google таблицей"""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(task_setup())
