"""
Конфигурация приложения
"""
import os
import logging
import sys
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

# === Настройка логирования ===
def setup_logging():
    """Настройка логирования для всего приложения"""
    log_format = "%(asctime)s | %(levelname)-8s | %(name)-25s | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # Основной логгер
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Уменьшаем логи от сторонних библиотек
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("selenium").setLevel(logging.WARNING)
    logging.getLogger("WDM").setLevel(logging.WARNING)
    
    return logging.getLogger("competitor_monitor")

# Инициализация логгера
logger = setup_logging()


class Settings(BaseSettings):
    """Настройки приложения"""

    # ProxyAPI (OpenAI-совместимый) или прямой OpenAI API.
    # По умолчанию ходим в ProxyAPI (как в исходном уроке). Если задан свой
    # настоящий ключ OpenAI (platform.openai.com), укажите в .env:
    #   OPENAI_BASE_URL=https://api.openai.com/v1
    # и он переопределит base_url на официальный эндпоинт OpenAI.
    proxy_api_key: str = os.getenv("PROXY_API_KEY", "")
    proxy_api_base_url: str = os.getenv("OPENAI_BASE_URL", "https://api.proxyapi.ru/openai/v1")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    openai_vision_model: str = os.getenv("OPENAI_VISION_MODEL", "gpt-4o-mini")

    # Ниша: интернет-магазины морепродуктов (Москва)
    niche: str = "Интернет-магазины морепродуктов"
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # История
    history_file: str = "history.json"
    max_history_items: int = 10
    
    # Парсер
    parser_timeout: int = 30
    parser_user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    
    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()


# === Конкуренты для парсинга (шаг 4 задания) ===
# 5 московских интернет-магазинов морепродуктов — целевые URL для /parse_demo
COMPETITORS = [
    {"name": "Краб Креветка", "url": "https://www.krab-krevetka.ru/"},
    {"name": "Crab:Store", "url": "https://crabstore.online/"},
    {"name": "KraBsBeRi", "url": "https://krabsberi.ru/"},
    {"name": "Краб №1", "url": "https://krab1.ru/"},
    {"name": "Mr. CRAB", "url": "https://mistercrab.ru/"},
]

