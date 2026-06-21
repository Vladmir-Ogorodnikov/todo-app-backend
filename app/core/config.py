from dataclasses import dataclass

#froze = True защита от изменений значения полей из вне

@dataclass(frozen = True)
class Settings:
    DATABASE_URL : str
    cors_allowed_origin : list[str]

def get_settings() -> Settings:

    return Settings(
        DATABASE_URL = "sqlite:///./finance.db",
        cors_allowed_origin = ["http://localhost:3000"]
    )