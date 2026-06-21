from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import CategoriesORM


class CategoryRepository:

    def __init__(self, db : Session):
        self.db = db

    def get_all(self) -> list[CategoriesORM]:
        return self.db.scalars(select(CategoriesORM)).all()

    def get_by_id(self, category_id: str) -> CategoriesORM:
        return self.db.get(CategoriesORM, category_id)

    def create_category(self, name : str) -> CategoriesORM:
        new_category = CategoriesORM(name = name)

        self.db.add(new_category)

        return new_category

    def delete(self, CategoriesORM):
        self.db.delete(CategoriesORM)