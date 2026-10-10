from dataclasses import dataclass

#froze = True защита от изменений значения полей из вне

@dataclass(frozen = True)
class Settings:
    DATABASE_URL : str
    redis_url : str
    cache_ttl_seconds : int
    cache_tasks_key : str
    cors_allowed_origin : list[str]

def get_settings() -> Settings:

    return Settings(
        DATABASE_URL = "sqlite:///./finance.db",
        redis_url = "redis:/localhost:6379/0",
        cache_ttl_seconds = 3600,
        cache_tasks_key = "cache:tasks_list",
        cors_allowed_origin = ["http://localhost:3000"]
    )