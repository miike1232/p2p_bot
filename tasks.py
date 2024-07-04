import asyncio

from celery import Celery
from bybit import get_BYBIT_p2p
from celery.schedules import crontab
from database import set_exchange_rate

app = Celery('tasks', broker='redis://localhost')


@app.task
def task_every_30_min():
    asyncio.run(
        set_exchange_rate(
            symbol="USDTUAH",
            value=asyncio.run(get_BYBIT_p2p(
                token="USDT",
                fiat="UAH"
            ))
        )
    )


app.conf.update(
    beat_schedule={
        'task-every-30-min': {
            'task': 'tasks.task_every_30_min',
            'schedule': crontab(minute='*/30'),
        },
    }
)
