from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://jaruser:jarpassword@localhost:5432/jardb"
    PRINTER_WIDTH_MM: float = 62.0
    PRINTER_DPI: int = 300

    class Config:
        env_file = ".env"

settings = Settings()
