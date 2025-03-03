from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from src.dependencies.base_dependencies import get_user_repository
from src.auth.jwt_processor import JwtProcessor
from src.password_hasher import PasswordHasher
from src.admin.config import AdminConfig
from src.repositories.user_repository import UserRepository
from src.schemas.login import LoginResponse


class AdminAuth(AuthenticationBackend):    
    def __init__(self, secret_key: str, password_hasher: PasswordHasher, config: AdminConfig, jwt_processor: JwtProcessor) -> None:
        super().__init__(secret_key)
        self.password_hasher = password_hasher
        self.jwt_processor = jwt_processor
        self.config = config

    async def login(self, request: Request, user_repository: UserRepository = get_user_repository()) -> LoginResponse:
        if self.config.debug:
            return True

        form = await request.form()
        email, password = form["email"], form["password"]

        user = await user_repository.get(email=email)
        if not user:
            return LoginResponse(ok=False, email_error_message=f"нет пользователя с email адресом {email}")

        if not user.is_superuser:
            return LoginResponse(ok=False, email_error_message="Недостаточно прав для входа в панель администратора")

        if not self.password_hasher.verify(password, user.hash_password):
            return LoginResponse(ok=False, password_error_message="Неверный пароль")

        access_token = self.jwt_processor.create_access_token(user.email, user.id)
        request.session.update({"token": access_token})
        return LoginResponse(ok=True)

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        if self.config.debug:
            return True

        token = request.session.get("token")

        if token and self.jwt_processor.validate_token(token):
            return True

        return False
