from fastapi import FastAPI

from src.admin.admin import CustomAdmin
from src.admin.auth import AdminAuth
from src.admin.config import get_admin_config
from src.admin.views import APIUrlsAdmin, LogAdmin, UserAdmin, VendorAdmin
from src.db.database import engine


def init_admin(app: FastAPI):
    authentication_backend = AdminAuth(secret_key=get_admin_config().admin_secret_key)
    admin = CustomAdmin(
        app=app, engine=engine, authentication_backend=authentication_backend, templates_dir="src/templates"
    )
    admin.add_view(UserAdmin)
    admin.add_view(VendorAdmin)
    admin.add_view(APIUrlsAdmin)
    admin.add_view(LogAdmin)