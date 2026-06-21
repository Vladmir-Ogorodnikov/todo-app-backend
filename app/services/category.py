from sqlalchemy.orm import Session

from app.repositories.category import CategoryRepository
from app.schemas.category import CategoriesReadSchema, CategoryUpdateSchema, CategoriesCreateSchema


class CategoryNotFound(Exception):
    ...


class CategoryService:

    def __init__(self, db : Session):

        self.db = db
        self.category_repository = CategoryRepository(db = db)

    def read_categories(self) -> list[CategoriesReadSchema]:
        category_orm = self.category_repository.get_all()
        return [CategoriesReadSchema.model_validate(category) for category in category_orm]


    def create_category(self, category : CategoriesCreateSchema) -> CategoriesReadSchema:
        category = self.category_repository.create_category(name = category.name)
        self.db.commit()
        return CategoriesReadSchema.model_validate(category)

    def update_category(self, category_id : str, category : CategoryUpdateSchema) -> CategoriesReadSchema:
        category_for_update = self.category_repository.get_by_id(category_id)
        if not category_for_update:
            raise CategoryNotFound(f"Категория с id {category_id} не найдена")

        if category.name is not None:
            category_for_update.name = category.name
        self.db.commit()

        return CategoriesReadSchema.model_validate(category_for_update)

    def delete_category(self, category_id : str):
        category_for_delete = self.category_repository.get_by_id(category_id = category_id)
        if not category_for_delete:
            raise CategoryNotFound(f"Категория с id {category_id} не найдена")
        self.category_repository.delete(category_for_delete)
        self.db.commit()

