# bot_webhook.py
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from config import BOT_TOKEN, BASE_WEBHOOK_URL, WEBHOOK_SECRET, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT
from handlers import router

async def on_startup(bot: Bot):
    """Выполняется при старте: устанавливает вебхук."""
    await bot.set_webhook(
        url=f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}",
        secret_token=WEBHOOK_SECRET
    )
    logging.info(f"Вебхук установлен на {BASE_WEBHOOK_URL}{WEBHOOK_PATH}")

async def on_shutdown(bot: Bot):
    """Выполняется при остановке: удаляет вебхук."""
    await bot.delete_webhook()
    await bot.session.close()
    logging.info("Вебхук удален и сессия закрыта.")

async def ping_server(request):
    """Отвечает на 'ping' запросы от сервисов мониторинга."""
    return web.Response(text="ok")

async def main():
    # Настройка логирования
    logging.basicConfig(level=logging.INFO)

    # Инициализация бота и диспетчера
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)

    # Регистрация lifecycle-хуков
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    # Создание веб-приложения
    app = web.Application()
    app.router.add_get("/ping", ping_server)

    # Настройка обработчика вебхуков
    webhook_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET,
    )
    webhook_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    
    # Запуск сервера
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host=WEBAPP_HOST, port=WEBAPP_PORT)
    await site.start()
    
    logging.info(f"Сервер запущен на {WEBAPP_HOST}:{WEBAPP_PORT}")
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен.")