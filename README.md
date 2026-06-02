# 💼 Nexus Labs — Портфолио проектов

> Репозиторий с реальными проектами по разработке API, автоматизации, Telegram-ботов и парсингу данных.
> 
> 🌐 **Сайт**: [rage213.github.io/nexus-labs/](https://rage213.github.io/nexus-labs/) | ✉️ Контакт через сайт

> [!WARNING]
> ### 🛡️ Юридическая защита и Лицензия / Proprietary License
> Все материалы данного репозитория защищены авторским правом (Copyright © 2026 knrcharge). 
> Копирование, распространение, коммерческое использование или развертывание проектов без письменного согласия автора **строго запрещено**. Просмотр кода разрешен исключительно в целях ознакомления и оценки квалификации.


---

## 🚀 Проекты

| Проект | Описание | Технологии |
|--------|----------|------------|
| [🛒 Telegram-магазин](./tg-shop-bot) | Полноценный интернет-магазин в Telegram с корзиной, SQLite и оплатой | `aiogram 3.x` `aiosqlite` `FSM` |
| [📈 Парсер цен](./price-tracker-parser) | Асинхронный мониторинг цен с Telegram-уведомлениями | `aiohttp` `asyncio` `BeautifulSoup` |
| [🤖 CRM-аналитика бот](./crm-analytics-bot) | Telegram-бот для анализа продаж с графиками и отчётами | `aiogram` `SQLite` `matplotlib` |
| [🔍 AI-ассистент с RAG](./rag-ai-assistant) | Умный Telegram-бот-помощник с базой знаний и векторным поиском | `aiogram` `openai` `vector-store` |
| [🛡️ Обход антибот-защиты](./anti-bot-scraper) | Продвинутый скрапер с обходом Cloudflare и CAPTCHA | `playwright` `aiohttp` |
| [📊 WebSocket монитор](./websocket-price-monitor) | Real-time мониторинг криптовалютных бирж через WebSocket | `websockets` `asyncio` |
| [⚡ FastAPI Analytics API](./fastapi-analytics-api) | Аналитический REST API для сбора и агрегации метрик ботов | `FastAPI` `aiosqlite` `Pydantic v2` |
| [💳 Crypto Payment Bot](./crypto-payment-bot) | Телеграм-магазин с приёмом криптоплатежей и автовыдачей | `aiogram 3.x` `CryptoBot API` `aiohttp` |
| [📅 Auto-Posting Bot](./auto-posting-bot) | Бот автопостинга в Telegram-каналы по расписанию с очередью задач | `aiogram 3.x` `APScheduler` `SQLAlchemy` |
| [🛡️ Chat Moderation Bot](./chat-moderation-bot) | Бот модерации чатов с капчей для новых участников и антиспамом | `aiogram 3.x` `aiosqlite` `regex` |
| [📥 Feedback Support Bot](./feedback-support-bot) | Бот обратной связи с администратором через нативный Reply | `aiogram 3.x` `aiosqlite` `FSM` |

---

## 🛠️ Стек технологий

```
Python 3.11+       │  aiogram 3.x      │  FastAPI / Pydantic v2
SQLite / aiosqlite │  BeautifulSoup   │  Playwright / scraping
pyrogram           │  websockets       │  matplotlib / charts
APScheduler        │  SQLAlchemy       │  Crypto Payment integration
```

---

## 📦 Как запустить любой проект

1. Перейди в папку проекта: `cd <project-name>`
2. Установи зависимости: `pip install -r requirements.txt`
3. Скопируй `.env.example` → `.env` и заполни токены
4. Запусти: `python bot.py` или `python main.py`

*Примечание по безопасности: Для демонстрации защиты софта от реверс-инжиниринга, в каждый проект добавлена папка `obfuscated/` с защищенной/обфусцированной версией точки входа (`*_protected.py`), упакованной в безопасный загрузчик.*

---

## 📬 Контакты

- 🌐 Сайт: [rage213.github.io/nexus-labs/](https://rage213.github.io/nexus-labs/)
- 💬 Telegram: [@knrcharge](https://t.me/knrcharge)
