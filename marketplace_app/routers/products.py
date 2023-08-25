from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.users import current_user
from database import get_db
from models.product import Product
from models.user import User
from schemas import ProductScheme, ProductCreate, ProductUpdate


router = APIRouter(
    tags=['products']
)


@router.get("/products", response_model=list[ProductScheme])
async def read_products(session: AsyncSession = Depends(get_db)):
    async with session.begin():
        products = await session.execute(select(Product))
        return products.scalars().all()


@router.get("/product/{product_id}", response_model=ProductScheme)
async def read_product(product_id: int, session: AsyncSession = Depends(get_db)):
    async with session.begin():
        product = await session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail='Product not found')

        return product


@router.get("/user_products", response_model=list[ProductScheme])
async def read_my_products(user: User = Depends(current_user), session: AsyncSession = Depends(get_db)):
    async with session.begin():
        user_products = await session.execute(
            select(Product).filter(Product.owner_id == user.id)
        )
        return user_products.scalars().all()


@router.post("/create_product", response_model=ProductScheme)
async def create_product(product_data: ProductCreate,
                         user: User = Depends(current_user),
                         session: AsyncSession = Depends(get_db)
                         ):
    try:
        product = Product(
            owner_id=user.id,
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
        )
        session.add(product)

        await session.commit()
        await session.refresh(product)

        return product

    except Exception as err:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f'Failed to create product: {err}')


@router.put('/update_product/{product_id}', response_model=ProductScheme)
async def update_product(product_id: int,
                         product_update: ProductUpdate,
                         user: User = Depends(current_user),
                         session: AsyncSession = Depends(get_db),
                         ):
    async with session.begin():
        product = await session.get(Product, product_id)

        if not product:
            raise HTTPException(status_code=404, detail='Product not found')

        if product.owner_id != user.id:
            raise HTTPException(status_code=403, detail='Youa are not owner to update this product')

        product.name = product_update.name
        product.description = product_update.description
        product.price = product_update.price

        await session.flush()
        return product


@router.post('/delete_product/{product_id}', response_model=ProductScheme)
async def delete_product(product_id: int,
                         session: AsyncSession = Depends(get_db),
                         user: User = Depends(current_user)):
    async with session.begin():
        product = await session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail='Product not found or has been deleted')

        if product.owner_id != user.id:
            raise HTTPException(status_code=403, detail='Not authorized to delete this product')

        await session.delete(product)
        await session.flush()

        return {'message': f'Product deleted successfully'}
