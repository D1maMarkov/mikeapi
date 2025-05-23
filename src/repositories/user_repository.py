from sqlalchemy import select

from src.db.models.models import UserOrm
from src.repositories.base_reposiotory import BaseRepository


class UserRepository(BaseRepository):
    async def get(self, email: str) -> UserOrm:
        result = await self.db.execute(select(UserOrm).where(UserOrm.email == email))
        return result.scalar()

    async def create(self, username: str, email: str, hashed_password: str, is_superuser: bool = False) -> UserOrm:
        user = UserOrm(username=username, email=email, hash_password=hashed_password, is_superuser=is_superuser)
        self.db.add(user)
        await self.db.commit()
        return user
