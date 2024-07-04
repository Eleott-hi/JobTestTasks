import asyncio
import configs.config
from database.database import init_db, fill_db

from models.QueueRequest import QueueRequest

test_data = [
    QueueRequest(
        method="GET",
        uri="/wiki",
        params='{"q": "Python"}',
        headers='{"Accept": "text/html"}',
    )
    for _ in range(10)
]


async def main():
    await init_db()
    await fill_db(QueueRequest, test_data)


if __name__ == "__main__":
    asyncio.run(main())
