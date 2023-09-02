from fastapi import FastAPI


from marketplace_app.auth.schemas import UserCreate
from marketplace_app.auth.schemas import UserRead
from marketplace_app.auth.users import auth_backend, fastapi_users

from marketplace_app.routers import products


app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)


app.include_router(products.router)
