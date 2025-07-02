from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    parser_url: str = "https://suip.biz/ru/?act=mat"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        fields = {
            "database_url": {"env": "DATABASE_URL"},
            "parser_url": {"env": "PARSER_URL"},
        }


settings = Settings()
