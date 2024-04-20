import datetime
from config import DB_URL, DB_NAME

import motor.motor_asyncio


class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.transaction_col = self.db.transactions

    def new_user(self, id):
        return dict(
            id=id,
            join_date=datetime.date.today().isoformat(),
        )

    async def add_user(self, id):
        user = self.new_user(id)
        await self.col.insert_one(user)

    async def is_user_exist(self, id):
        user = await self.col.find_one({"id": int(id)})
        return True if user else False

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users

    async def delete_user(self, user_id):
        await self.col.delete_many({"id": int(user_id)})
    async def forward_true(self, user_id):
        await DB.col.update_one({"id": user_id}, {"$set": {"forward": True}})
    async def forward_false(self, user_id):
        await DB.col.update_one({"id": user_id}, {"$set": {"forward": False}})

 
    #####################
    #### Transaction ####
    #####################
    def new_transaction(self, id, amount, currency, product):
        return dict(
            id=f'{datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")}-{id}',
            user_id=id,
            amount=amount,
            product=product,
            currency=currency,
            date=datetime.date.today().isoformat(),
        )
    async def add_transaction(self, id, amount, currency, product):
        transaction = self.new_transaction(id, amount, currency, product)
        await self.transaction_col.insert_one(transaction)

DB = Database(DB_URL, DB_NAME)









#         unique_id = "20220318120530123456"  # YYYYMMDDHHMMSSffffff format

# # Parse the unique ID string into a datetime object
# parsed_date = datetime.datetime.strptime(unique_id, "%Y%m%d%H%M%S%f")

# # Extract the date from the datetime object
# date = parsed_date.date()