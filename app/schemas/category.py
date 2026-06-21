from pydantic import BaseModel, ConfigDict

class CategoriesReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id : str
    name: str

class CategoriesCreateSchema(BaseModel):
    name : str

class CategoryUpdateSchema(BaseModel):

    name : str | None = None