from src.dependencies.repos_container import ReposContainer
from repositories.deal_repository import DealRepository
from time import time
import asyncio

async def get_lots_deals():
    deal_repository: DealRepository = await ReposContainer.deal_repository()
    print("start")
    print("get all deals...")
    all_deals = await deal_repository.all()

    print("filter deals...")
    start = time()
    for _ in range(5):
        deals = [deal for deal in all_deals if deal.user_id==779049]
    print(time() - start)

    print("filter deals list...")
    start = time()
    for _ in range(5):
        deals = await deal_repository.filter(trader_id=779049)
    print(time() - start)


if __name__ == "__main__":
    asyncio.run(get_lots_deals())