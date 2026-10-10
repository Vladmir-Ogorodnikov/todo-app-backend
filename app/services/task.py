from sqlalchemy.orm import Session

from app.cache.redis_cache import RedisCacheBackend
from app.repositories.task import TaskRepository
from app.schemas.task import TaskReadSchema, TaskCreateSchema, TaskUpdateSchema
from app.core.config import get_settings

class TaskNotFound(Exception):
    ...

settings = get_settings()

class TaskService:

    def __init__(self, db : Session, cache_redis_url : str) -> None:

        self.db = db
        self.task_repository = TaskRepository(db = db)
        self.cache = RedisCacheBackend(cache_redis_url, settings.cache_ttl_seconds)


    def list_tasks(self) -> list[TaskReadSchema]:
        # ШАГ 1 Сходить в redis
        cached_tasks = self.cache.get(settings.cache_tasks_key)
        if cached_tasks is not None:
            return cached_tasks



        tasks_orm = self.task_repository.get_all() #шаг 2 сходили в бд

        #Шаг 3. Закешировать
        tasks_read = [TaskReadSchema.model_validate(task) for task in tasks_orm]
        tasks_for_cache = [task.model_dump() for task in tasks_read]
        self.cache.set(settings.cache_tasks_key, tasks_for_cache)
        return tasks_read

    def create_task(self, task_create: TaskCreateSchema) -> TaskReadSchema:
        self.cache.delete(settings.cache_tasks_key)
        #инвалидировать кеш
        task_orm = self.task_repository.create_task(title = task_create.title)
        self.db.commit()

        return TaskReadSchema.model_validate(task_orm)


    def update_task(self, task_id : str, task_update : TaskUpdateSchema) -> TaskReadSchema:
        self.cache.delete(settings.cache_tasks_key)
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
        self.cache.delete(settings.cache_tasks_key)
        task_for_delete = self.task_repository.get_by_id(task_id=task_id)
        if not task_for_delete:
            raise TaskNotFound(f"Задача с id {task_id} не найдена")
        self.task_repository.delete(task_for_delete)
        self.db.commit()





