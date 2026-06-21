from fastapi import APIRouter, Depends, status, HTTPException

from app.api.dependecies import get_category_service
from app.schemas.category import CategoriesReadSchema, CategoryUpdateSchema, CategoriesCreateSchema
from app.services.category import CategoryService, CategoryNotFound

router = APIRouter(prefix = "/categories")


@router.get("", status_code = status.HTTP_200_OK)
def read_categories(category_service : CategoryService = Depends(get_category_service)) -> list[CategoriesReadSchema]:
    return category_service.read_categories()


@router.post("", status_code = status.HTTP_201_CREATED)
def create_categories(payload : CategoriesCreateSchema,
                      category_service : CategoryService = Depends(get_category_service)) -> CategoriesReadSchema:
    return category_service.create_category(category = payload)


@router.patch("/{category_id}")
def update_category(category_id : str, payload : CategoryUpdateSchema, category_service : CategoryService = Depends(get_category_service)) -> CategoriesReadSchema:
    try:
        return category_service.update_category(category_id = category_id, category = payload)
    except CategoryNotFound:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)



@router.delete("/{category_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_category(category_id : str, category_service : CategoryService = Depends(get_category_service)):
    try:
        category_service.delete_category(category_id = category_id)
    except CategoryNotFound:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
