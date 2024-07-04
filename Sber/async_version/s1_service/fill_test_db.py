import asyncio
import json
import configs.config
from database.database import init_db, fill_db

from models.QueueRequest import QueueRequest

test_data = [
    QueueRequest(
        method="GET",
        uri="/posts/1",
        headers=json.dumps({"Accept": "application/json"}),
    ),
    QueueRequest(
        method="POST",
        uri="/posts",
        params=json.dumps({"title": "foo", "body": "bar", "userId": 1}),
        headers=json.dumps({"Content-Type": "application/json"}),
    ),
    QueueRequest(
        method="PUT",
        uri="/posts/1",
        params=json.dumps({"id": 1, "title": "Updated Title"}),
        headers=json.dumps({"Content-Type": "application/json"}),
    ),
    QueueRequest(
        method="DELETE",
        uri="/posts/1",
        headers=json.dumps({"Authorization": "Bearer token"}),
    ),
    QueueRequest(
        method="GET",
        uri="/users",
        params=json.dumps({"_page": 1, "_limit": 10}),
        headers=json.dumps({"Accept": "application/json"}),
    ),
    QueueRequest(
        method="POST",
        uri="/comments",
        params=json.dumps(
            {
                "postId": 1,
                "name": "John Doe",
                "email": "johndoe@example.com",
                "body": "Nice post!",
            }
        ),
        headers=json.dumps({"Content-Type": "application/json"}),
    ),
]


async def main():
    await init_db()
    await fill_db(QueueRequest, test_data)


if __name__ == "__main__":
    asyncio.run(main())
