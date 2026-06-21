from sqlalchemy.orm import Session

from app.repositories.task import TaskRepository
from app.schemas.task import TaskReadSchema, TaskCreateSchema, TaskUpdateSchema

class TaskNotFound(Exception):
    ...


class TaskService:

    def __init__(self, db : Session):

        self.db = db
        self.task_repository = TaskRepository(db = db)

    def list_tasks(self) -> list[TaskReadSchema]:
        tasks_orm = self.task_repository.get_all()
        return [TaskReadSchema.model_validate(task) for task in tasks_orm]

    def create_task(self, task_create: TaskCreateSchema) -> TaskReadSchema:
        task_orm = self.task_repository.create_task(title = task_create.title)
        self.db.commit()

        return TaskReadSchema.model_validate(task_orm)


    def update_task(self, task_id : str, task_update : TaskUpdateSchema) -> TaskReadSchema:
        task_for_update = self.task_repository.get_by_id(task_id=task_id)
        if not task_for_update:
            raise TaskNotFound(f"Задача с id {task_id} не найдена")

        if task_update.title is not None:
            task_for_update.title = task_update.title
        if task_update.completed is not None:
            task_for_update.completed = task_update.completed

        self.db.commit()
        return TaskReadSchema.model_validate(task_for_update)


    def delete_task(self, task_id : str) -> TaskReadSchema:
        task_for_delete = self.task_repository.get_by_id(task_id=task_id)
        if not task_for_delete:
            raise TaskNotFound(f"Задача с id {task_id} не найдена")
        self.task_repository.delete(task_for_delete)
        self.db.commit()





