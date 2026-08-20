# 🔍 Мониторинг конкурентов - AI Ассистент

MVP приложение для анализа конкурентной среды с поддержкой мультимодальности (текст и изображения).

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-purple.svg)

> Форк учебного проекта [Toxap/pem08](https://github.com/Toxap/pem08), адаптированный под домашнее
> задание "Персональный AI-анализатор рынка конкурентов".

## 🦀 Мой кейс: интернет-магазины морепродуктов

Ниша: **интернет-магазины морепродуктов** (камчатский краб, креветки, гребешки, икра — доставка на дом).

5 реальных конкурентов, добавленных в [`backend/config.py`](backend/config.py) для демо-парсинга:

| Магазин | URL |
|---|---|
| Краб Креветка | https://www.krab-krevetka.ru/ |
| Crab:Store | https://crabstore.online/ |
| KraBsBeRi | https://krabsberi.ru/ |
| Краб №1 | https://krab1.ru/ |
| Mr. CRAB | https://mistercrab.ru/ |

Референсные материалы (скриншоты лендингов + распарсенные title/H1/абзац для каждого магазина)
собраны через `/parse_demo` и лежат в [`data/`](data): [`data/screenshots/`](data/screenshots)
и [`data/competitors_reference.json`](data/competitors_reference.json). 4 из 5 сайтов спарсились
успешно за один прогон; Mr. CRAB не уложился в таймаут headless-браузера (10 сек) — итоговая
запись с полем `error` для этого сайта тоже сохранена в JSON, без ретраев.

### Кастомные поля анализа (шаг 3 задания)

В [`backend/services/openai_service.py`](backend/services/openai_service.py) промпты дополнены
под нишу двумя оценками 0-10, которые возвращаются во всех трёх режимах анализа
(`/analyze_text`, `/analyze_image`, `/parse_demo`):

- **`design_score`** — визуальный стиль/UX сайта или подачи текста.
- **`freshness_trust_score`** — насколько текст/изображение внушает доверие к свежести и
  качеству морепродуктов (упоминания вылова, шоковой заморозки, сроков доставки, сертификатов,
  вид продукта на фото). Это нишевая замена примера `animation_potential` из задания,
  адаптированная под e-commerce морепродуктов, а не дизайн-студии.

## 📋 Описание

Приложение позволяет:
- **Анализировать текст конкурентов** — получать структурированную аналитику с сильными/слабыми сторонами, уникальными предложениями и рекомендациями
- **Анализировать изображения** — баннеры, скриншоты сайтов, упаковки товаров с оценкой визуального стиля
- **Парсить сайты** — автоматически извлекать и анализировать контент по URL
- **Хранить историю** — последние 10 запросов сохраняются для быстрого доступа

## 🚀 Быстрый старт

### 1. Клонирование и установка зависимостей

```bash
# Клонируйте репозиторий
cd competitor-monitor

# Создайте виртуальное окружение
python -m venv venv

# Активируйте окружение
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt
```

### 2. Настройка переменных окружения

Скопируйте `env.example.txt` в `.env` (сам `.env` в `.gitignore` и никогда не коммитится):

```bash
cp env.example.txt .env
```

Впишите ключ в `PROXY_API_KEY`. Поддерживаются два варианта:

```env
# Вариант A — ключ ProxyAPI (proxyapi.ru), используется как есть
PROXY_API_KEY=your_proxy_api_key_here

# Вариант B — настоящий ключ OpenAI (platform.openai.com): тот же PROXY_API_KEY,
# но дополнительно укажите официальный эндпоинт OpenAI
PROXY_API_KEY=sk-...
OPENAI_BASE_URL=https://api.openai.com/v1
```

### 3. Запуск приложения

```bash
python run.py
```

(эквивалент: `python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000`)

Приложение будет доступно по адресу: http://localhost:8000

## 📁 Структура проекта

```
competitor-monitor/
├── backend/
│   ├── __init__.py
│   ├── main.py              # FastAPI приложение
│   ├── config.py            # Конфигурация
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py       # Pydantic модели
│   └── services/
│       ├── __init__.py
│       ├── openai_service.py    # Работа с OpenAI API
│       ├── parser_service.py    # Парсинг веб-страниц
│       └── history_service.py   # Управление историей
├── frontend/
│   ├── index.html           # HTML страница
│   ├── styles.css           # Стили
│   └── app.js               # JavaScript логика
├── requirements.txt         # Зависимости Python
├── env.example.txt          # Пример .env файла
├── history.json             # Файл истории (создаётся автоматически)
├── README.md                # Этот файл
└── docs.md                  # Документация API
```

## 🔧 Функциональность

### Анализ текста (`/analyze_text`)
- Принимает текст конкурента (минимум 10 символов)
- Возвращает:
  - Сильные стороны
  - Слабые стороны
  - Уникальные предложения
  - Рекомендации по улучшению
  - Общее резюме
  - `design_score` (0-10) и `freshness_trust_score` (0-10)

### Анализ изображений (`/analyze_image`)
- Принимает файл (PNG, JPG, GIF, WEBP) **или** ссылку на изображение на стороннем сайте —
  без скачивания на диск, ссылка уходит напрямую в OpenAI Vision API
- Возвращает:
  - Описание изображения
  - Маркетинговые инсайты
  - Оценку визуального стиля (0-10)
  - Рекомендации
  - `design_score` (0-10) и `freshness_trust_score` (0-10)

### Парсинг сайтов (`/parse_demo`)
- Принимает URL сайта
- Извлекает: title, h1, первый абзац, скриншот страницы
- Автоматически анализирует извлечённый контент + скриншот через Vision API

### История (`/history`)
- Хранит последние 10 запросов
- Сохраняет тип запроса, краткое описание, время

## 🛠️ Технологии

- **Backend**: FastAPI, Python 3.9+
- **AI**: OpenAI GPT-4o-mini (или GPT-4.1)
- **Frontend**: Vanilla JS, CSS3
- **Парсинг**: BeautifulSoup4, httpx
- **Валидация**: Pydantic

## 📖 API Документация

После запуска сервера доступна интерактивная документация:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Подробная документация API в файле [docs.md](docs.md)

## 🖥️ Desktop-приложение

В [`desktop/`](desktop) лежит PyQt6-обёртка вокруг того же API (см. [`desktop/README.md`](desktop/README.md)).
Собрать исполняемый файл:

```bash
cd desktop
pip install -r requirements.txt
python build.py          # → dist/CompetitorMonitor.exe на Windows
```

Backend должен быть запущен отдельно (`python run.py`) — desktop-клиент обращается к нему по HTTP.

## 🐧 Разработка в WSL: на что натыкались

Весь кейс собран и прогнан в WSL (Ubuntu на Windows). Три момента, специфичных именно для этого
окружения — на обычном Linux/macOS с установленным Chrome их не будет:

- **Chrome не установлен по умолчанию.** `webdriver-manager` в `parser_service.py` скачивает
  только `chromedriver`, а не сам браузер — без Chrome драйвер падает с
  `chromedriver unexpectedly exited. Status code was: 127`. Ставится один раз:
  ```bash
  wget -O /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  sudo apt install -y /tmp/chrome.deb
  ```
  Если Chrome поставить нельзя (например, нет root — так было в песочнице при сборе скриншотов
  для `data/`), `parser_service.py` понимает переменные окружения `CHROME_BINARY_LOCATION` и
  `CHROMEDRIVER_PATH` — можно скачать портативную сборку
  [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/) и указать пути к
  распакованным бинарникам явно, без установки в систему.

- **Нет цветного эмодзи-шрифта.** Desktop-приложение (PyQt6) использует эмодзи в подписях вкладок
  и заголовках блоков (📝🖼️🌐📋 и т.д.) — без `fonts-noto-color-emoji` Qt рисует на их месте пустые
  квадратики:
  ```bash
  sudo apt install -y fonts-noto-color-emoji && fc-cache -f
  ```

- **`build.py` не даёт `.exe` при запуске из WSL.** PyInstaller собирает исполняемый файл под ту
  ОС, где его запустили, а не кросс-компилирует. Сборка из WSL кладёт в `dist/` ELF-бинарник
  `CompetitorMonitor` без расширения. Чтобы получить `CompetitorMonitor.exe`, `build.py` нужно
  запускать из Windows-Python (PowerShell/CMD, не WSL-терминал) — можно зайти в проект по
  сетевому пути `\\wsl.localhost\<дистрибутив>\...\desktop` и собрать оттуда.

Обратное работает без доп. настройки: WSL2 сам пробрасывает порты, поэтому backend, запущенный в
WSL на `localhost:8000`, виден и приложениям на самой Windows.

## ⚠️ Требования

- Python 3.9+
- ProxyAPI-ключ (или OpenAI API ключ) с доступом к gpt-4o-mini / gpt-4o
- Интернет-соединение для работы AI и парсинга
- **Никогда не коммитьте `.env`** — он в `.gitignore`; используйте `env.example.txt` как шаблон

## 📝 Лицензия

MIT License

