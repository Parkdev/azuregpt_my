from motor.motor_asyncio import AsyncIOMotorClient

import os

# db 연결 및 저장
db_client = AsyncIOMotorClient(os.environ["DB_CONNECTION_URL"])
db = db_client["mygpt"]
