from fastapi import FastAPI, Depends


from auth.schemas import UserCreate
from auth.schemas import UserRead
from auth.users import auth_backend, fastapi_users, current_user

from models.user import User
from routers import products


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

app.include_router(products.router)


app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)


@app.get("/protected-route")
async def protected_route(user: User = Depends(current_user)):
    return user.id
