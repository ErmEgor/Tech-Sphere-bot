# main.py
import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from config import BOT_TOKEN, BASE_WEBHOOK_URL, WEBHOOK_SECRET, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT
from handlers import router

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('bot.log')  # Сохраняем логи в файл для диагностики
    ]
)
logger = logging.getLogger(__name__)

async def on_startup(bot: Bot):
    """Выполняется при старте: устанавливает вебхук."""
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Существующий вебхук удалён")
        await bot.set_webhook(
            url=f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}",
            secret_token=WEBHOOK_SECRET,
            drop_pending_updates=True
        )
        webhook_info = await bot.get_webhook_info()
        logger.info(f"Вебхук установлен: {webhook_info}")
        if webhook_info.url != f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}":
            raise Exception("Вебхук не установлен корректно!")
    except Exception as e:
        logger.error(f"Ошибка при установке вебхука: {e}")
        raise

async def on_shutdown(bot: Bot):
    """Выполняется при остановке: удаляет вебхук."""
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Вебхук удалён")
        await bot.session.close()
        logger.info("Сессия бота закрыта")
    except Exception as e:
        logger.error(f"Ошибка при удалении вебхука: {e}")

async def handle_ping(request):
    """Обработчик для пинг-запросов от UptimeRobot."""
    logger.info("Получен пинг-запрос от UptimeRobot")
    return web.Response(text="Pong")

async def handle_root(request):
    """Обработчик для корневого маршрута."""
    logger.info("Получен запрос на корневой маршрут")
    return web.Response(text="Bot is running")

async def main():
    # Инициализация бота и диспетчера
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)

    # Регистрация lifecycle-хуков
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    # Создание веб-приложения
    app = web.Application()
    app.add_routes([
        web.get('/ping', handle_ping),  # Явная регистрация маршрута для UptimeRobot
        web.get('/', handle_root)       # Корневой маршрут для проверки
    ])

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
    
    logger.info(f"Сервер запущен на {WEBAPP_HOST}:{WEBAPP_PORT}")
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен.")