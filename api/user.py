from typing import Optional
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, IntegerIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from database.aiosqlite_connection import get_user_db
from database.models import User
from config import JWT_SECRET
from fastapi_users import exceptions, models, schemas
from typing import Generic
from overrides import override
from fastapi import APIRouter
from .auth import get_auth_router


class CustomFastAPIUsers(FastAPIUsers, Generic[models.UP, models.ID]):

    @override
    def get_auth_router(
        self,
        backend: AuthenticationBackend,
        requires_verification: bool = False
    ) -> APIRouter:
        return get_auth_router(
            backend,
            self.get_user_manager,
            self.authenticator,
            requires_verification,
        )


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = JWT_SECRET
    verification_token_secret = JWT_SECRET

    async def on_after_register(
            self, user: User, request: Optional[Request] = None
            ):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
            ):
        print(
            f"User {user.id} has forgot their password. Reset token: {token}"
        )

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
            ):
        print(
            f"Verification requested for user {user.id}. "
            f"Verification token: {token}"
        )

    @override
    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)
        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop('password')
        user_dict['hashed_password'] = self.password_helper.hash(password)
        user_dict['is_active'] = True
        user_dict['is_superuser'] = False
        user_dict['is_verified'] = False
        created_user = await self.user_db.create(user_dict)
        await self.on_after_register(created_user, request)
        return created_user


async def get_user_manager(
        user_db: SQLAlchemyUserDatabase = Depends(get_user_db)
        ) -> UserManager:
    yield UserManager(user_db)


async def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=JWT_SECRET, lifetime_seconds=3600)


cookie_transport = CookieTransport(
    cookie_max_age=None,
    cookie_name='AniMaunt'
)
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = CustomFastAPIUsers[User, int](get_user_manager, [auth_backend])
current_active_user = fastapi_users.current_user(active=True)

if __name__ == '__main__':
    pass
