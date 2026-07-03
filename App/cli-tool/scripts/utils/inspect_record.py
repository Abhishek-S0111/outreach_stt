import asyncio
from src.core.database import db_manager
from bson import ObjectId
import json
from datetime import datetime

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)

async def check_record():
    await db_manager.connect()
    try:
        # ID from previous logs
        iid = "6979edea7ffabab342982afb" 
        record = await db_manager.db.interactions.find_one({"_id": ObjectId(iid)})
        if record:
            print(json.dumps(record, cls=DateTimeEncoder, indent=2))
        else:
            print("Record not found")
    finally:
        await db_manager.disconnect()

if __name__ == "__main__":
    asyncio.run(check_record())
