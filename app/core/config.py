from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Title'
    app_description: str = 'Description'
    database_url: str = "sqlite+aiosqlite:///./cat_charity_fund.db"
    secret: str = 'SECRET'
    jwt_lifetime_seconds: int = 3600
    type: str | None = None
    project_id: str | None = None
    private_key_id: str | None = None
    private_key: str | None = None
    client_email: str | None = None
    client_id: str | None = None
    auth_uri: str | None = None
    token_uri: str | None = None
    auth_provider_x509_cert_url: str | None = None
    client_x509_cert_url: str | None = None
    email: str | None = None

    class Config:
        env_file = '.env'


settings = Settings()
