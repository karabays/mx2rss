from pydantic import BaseSettings

from log import logger

class Settings(BaseSettings):
    site_url: str
    email_domain: str
    dapanel_url: str
    dapanel_user: str
    dapanel_pass: str
    inbox: str
    inbox_url: str
    inbox_pass: str
    fetch_frequency: str = 300

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()