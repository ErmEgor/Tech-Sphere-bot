# config.py
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# --- Настройки для вебхука ---
BASE_WEBHOOK_URL = os.getenv("RENDER_EXTERNAL_URL")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
WEBHOOK_PATH = "/webhook"

# --- Настройки для сервера ---
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.getenv("PORT", 8080))


# --- РАСШИРЕННЫЙ КАТАЛОГ ТОВАРОВ С ХАРАКТЕРИСТИКАМИ ---
CATALOG = {
    "audio": {
        "name": "🎧 Аудио-техника",
        "products": {
            "airpods_pro2": {
                "name": "AirPods Pro 2",
                "price": 115000,
                "desc": "Наушники с активным шумоподавлением и пространственным аудио. Идеальный звук в компактном формате.",
                "specs": "<b>Тип:</b> Внутриканальные, беспроводные\n"
                         "<b>Чип:</b> Apple H2\n"
                         "<b>Шумоподавление:</b> Активное (ANC)\n"
                         "<b>Время работы:</b> до 6 ч (до 30 ч с кейсом)\n"
                         "<b>Защита:</b> IPX4 (от пота и брызг)",
                "photo": "AgACAgIAAxkBAAOlaElLtY9pWmCKKcNM8M_6l8e0IUkAAoPtMRvonUlKSRmyCq2lyDUBAAMCAANtAAM2BA"
            },
            "sony_wh1000": {
                "name": "Sony WH-1000XM5",
                "price": 180000,
                "desc": "Легендарные полноразмерные наушники с лучшим на рынке шумоподавлением. До 30 часов работы.",
                "specs": "<b>Тип:</b> Полноразмерные, беспроводные\n"
                         "<b>Драйвер:</b> 30 мм, динамический\n"
                         "<b>Шумоподавление:</b> Активное (ANC) с авто-оптимизацией\n"
                         "<b>Время работы:</b> до 30 ч (с ANC), до 40 ч (без ANC)\n"
                         "<b>Подключение:</b> Bluetooth 5.2, 3.5 мм аудио-джек",
                "photo": "AgACAgIAAxkBAANJaElDc5u92dceDqnUVNxLs1L_ZP0AAuftMRsTekhKO6CxCL7J_IkBAAMCAANtAAM2BA"
            },
            "jbl_charge5": {
                "name": "JBL Charge 5",
                "price": 85000,
                "desc": "Портативная водонепроницаемая колонка с мощным звуком и функцией Powerbank. До 20 часов музыки.",
                "specs": "<b>Мощность:</b> 40 Вт RMS\n"
                         "<b>Диапазон частот:</b> 65 Гц - 20 кГц\n"
                         "<b>Время работы:</b> до 20 часов\n"
                         "<b>Защита:</b> IP67 (водо- и пыленепроницаемость)\n"
                         "<b>Особенности:</b> PartyBoost, встроенный Powerbank",
                "photo": "AgACAgIAAxkBAAPSaElPnAlm1INY5RFfwemTdG6xYdEAAnDuMRsTekhKSw7ktC2HX-IBAAMCAANtAAM2BA"
            },
            "sennheiser_momentum4": {
                "name": "Sennheiser Momentum 4",
                "price": 165000,
                "desc": "Аудиофильский звук и непревзойденный комфорт. До 60 часов работы от одного заряда.",
                "specs": "<b>Тип:</b> Полноразмерные, беспроводные\n"
                         "<b>Драйвер:</b> 42 мм, динамический\n"
                         "<b>Шумоподавление:</b> Адаптивное гибридное (ANC)\n"
                         "<b>Время работы:</b> до 60 часов (с ANC)\n"
                         "<b>Кодеки:</b> SBC, AAC, aptX, aptX Adaptive",
                "photo": "AgACAgIAAxkBAAPQaElPlAT02nXEmFioxqS2UDySeXcAAm_uMRsTekhKAda-NrkL9y0BAAMCAANtAAM2BA"
            }
        }
    },
    "gadgets": {
        "name": "⌚️ Смарт-гаджеты",
        "products": {
            "apple_watch9": {
                "name": "Apple Watch S9",
                "price": 210000,
                "desc": "Самые мощные смарт-часы от Apple. Измеряйте кислород в крови, делайте ЭКГ и оставайтесь на связи.",
                "specs": "<b>Дисплей:</b> Always-On Retina LTPO OLED\n"
                         "<b>Чип:</b> S9 SiP\n"
                         "<b>Датчики:</b> SpO2, ЭКГ, датчик температуры, оптический датчик сердца\n"
                         "<b>Защита:</b> до 50 метров под водой\n"
                         "<b>Особенности:</b> Жест Double Tap, Crash Detection",
                "photo": "AgACAgIAAxkBAANLaElDf4dlTAasn5Ak63hOf8P2VLEAAujtMRsTekhKplF15N89lw4BAAMCAANtAAM2BA"
            },
            "dyson_styler": {
                "name": "Dyson Airwrap Styler",
                "price": 290000,
                "desc": "Мультистайлер для волос, который сушит и укладывает волосы без экстремальных температур.",
                "specs": "<b>Мощность:</b> 1300 Вт\n"
                         "<b>Скорость потока:</b> 13.5 л/с\n"
                         "<b>Режимы:</b> 3 скорости, 3 температурных режима\n"
                         "<b>Насадки в комплекте:</b> 6 шт.\n"
                         "<b>Особенности:</b> Эффект Коанда, интеллектуальный контроль температуры",
                "photo": "AgACAgIAAxkBAANNaElDjK46Yu5Ty2kllDimvcPw65UAAuntMRsTekhKa9iDur6QyJoBAAMCAANtAAM2BA"
            },
            "xiaomi_band8": {
                "name": "Xiaomi Mi Band 8",
                "price": 25000,
                "desc": "Народный фитнес-браслет с ярким AMOLED-дисплеем и множеством спортивных режимов.",
                "specs": "<b>Дисплей:</b> 1.62\" AMOLED, 60 Гц\n"
                         "<b>Датчики:</b> SpO2, мониторинг пульса, сна, стресса\n"
                         "<b>Спортивные режимы:</b> 150+\n"
                         "<b>Время работы:</b> до 16 дней\n"
                         "<b>Защита:</b> 5 ATM (до 50 метров)",
                "photo": "AgACAgIAAxkBAAPOaElPjWfqEqjJi2nxXvkQUTPWVbAAAm7uMRsTekhKH69TEyltgysBAAMCAANtAAM2BA"
            },
            "gopro_hero12": {
                "name": "GoPro HERO12 Black",
                "price": 230000,
                "desc": "Лучшая экшн-камера для ваших приключений. Видео в 5.3K, невероятная стабилизация HyperSmooth 6.0.",
                "specs": "<b>Видео:</b> 5.3K60, 4K120, 2.7K240\n"
                         "<b>Фото:</b> 27 МП\n"
                         "<b>Стабилизация:</b> HyperSmooth 6.0\n"
                         "<b>Защита:</b> до 10 метров без бокса\n"
                         "<b>Особенности:</b> HDR видео, 8-битный и 10-битный цвет + Log",
                "photo": "AgACAgIAAxkBAAPMaElPg8r-9HaW5T9Fl12ANgmp5WoAAmzuMRsTekhKrnELHbP1HgIBAAMCAANtAAM2BA"
            }
        }
    },
    "laptops": {
        "name": "💻 Ноутбуки и ПК",
        "products": {
            "macbook_air_m2": {
                "name": "MacBook Air M2",
                "price": 550000,
                "desc": "Невероятно тонкий и легкий ноутбук с мощным чипом M2. Работает до 18 часов без подзарядки.",
                "specs": "<b>Чип:</b> Apple M2 (8-ядерный CPU, 8-ядерный GPU)\n"
                         "<b>Память:</b> 8 ГБ объединенной памяти\n"
                         "<b>Накопитель:</b> 256 ГБ SSD\n"
                         "<b>Дисплей:</b> 13.6\" Liquid Retina\n"
                         "<b>Вес:</b> 1.24 кг",
                "photo": "AgACAgIAAxkBAAPaaElQh-cybocfLqQHKIabrSQTAlgAAn7uMRsTekhKXTjAIlUjsLEBAAMCAANtAAM2BA"
            },
            "lenovo_legion5": {
                "name": "Lenovo Legion 5 Pro",
                "price": 780000,
                "desc": "Мощный игровой ноутбук с видеокартой NVIDIA GeForce RTX и дисплеем 165 Гц.",
                "specs": "<b>Процессор:</b> AMD Ryzen 7 7745HX\n"
                         "<b>Видеокарта:</b> NVIDIA GeForce RTX 4060 8 ГБ\n"
                         "<b>Память:</b> 16 ГБ DDR5\n"
                         "<b>Дисплей:</b> 16\" WQXGA (2560x1600), 165 Гц\n"
                         "<b>Накопитель:</b> 1 ТБ SSD",
                "photo": "AgACAgIAAxkBAAPYaElQfbTvd55NTTHz5Gav8hUbpwcAAn3uMRsTekhK8JtHBHMr4Q4BAAMCAANtAAM2BA"
            },
            "dell_xps15": {
                "name": "Dell XPS 15",
                "price": 890000,
                "desc": "Премиальный ноутбук для работы и творчества с потрясающим 4K OLED-дисплеем.",
                "specs": "<b>Процессор:</b> Intel Core i7-13700H\n"
                         "<b>Видеокарта:</b> NVIDIA GeForce RTX 4050 6 ГБ\n"
                         "<b>Память:</b> 16 ГБ DDR5\n"
                         "<b>Дисплей:</b> 15.6\" 3.5K (3456x2160) OLED, сенсорный\n"
                         "<b>Накопитель:</b> 512 ГБ SSD",
                "photo": "AgACAgIAAxkBAAPWaElQdDFFtSFXrdiXajNFgHa13nYAAnzuMRsTekhKCHeypToh3QoBAAMCAANtAAM2BA"
            },
            "imac_24": {
                "name": "iMac 24\" M3",
                "price": 710000,
                "desc": "Стильный и мощный моноблок для дома и офиса. Яркий дисплей Retina 4.5K.",
                "specs": "<b>Чип:</b> Apple M3 (8-ядерный CPU, 8-ядерный GPU)\n"
                         "<b>Память:</b> 8 ГБ объединенной памяти\n"
                         "<b>Накопитель:</b> 256 ГБ SSD\n"
                         "<b>Дисплей:</b> 24\" 4.5K Retina\n"
                         "<b>Комплект:</b> Magic Keyboard, Magic Mouse",
                "photo": "AgACAgIAAxkBAAPUaElQbXrf5kPha8Atwh7UxLd0OHIAAvLtMRvonUlKJnf9ao9q5ksBAAMCAANtAAM2BA"
            }
        }
    },
    "gaming": {
        "name": "🎮 Игровые консоли",
        "products": {
            "ps5": {
                "name": "Sony PlayStation 5",
                "price": 280000,
                "desc": "Консоль нового поколения с невероятно быстрой загрузкой и поддержкой игр в 4K 120 fps.",
                "specs": "<b>Процессор:</b> 8-ядерный AMD Zen 2\n"
                         "<b>Графика:</b> AMD RDNA 2, 10.3 терафлопс\n"
                         "<b>Память:</b> 16 ГБ GDDR6\n"
                         "<b>Накопитель:</b> 825 ГБ SSD\n"
                         "<b>Привод:</b> Blu-Ray",
                "photo": "AgACAgIAAxkBAAPiaElRL6qQJgbzlkkoRCPnMNuJLH4AAofuMRsTekhKVOAHkTEL-bMBAAMCAANtAAM2BA"
            },
            "xbox_series_x": {
                "name": "Microsoft Xbox Series X",
                "price": 275000,
                "desc": "Самая мощная консоль Xbox. Наслаждайтесь тысячами игр с лучшей графикой и производительностью.",
                "specs": "<b>Процессор:</b> 8-ядерный Custom Zen 2\n"
                         "<b>Графика:</b> Custom RDNA 2, 12 терафлопс\n"
                         "<b>Память:</b> 16 ГБ GDDR6\n"
                         "<b>Накопитель:</b> 1 ТБ SSD\n"
                         "<b>Привод:</b> 4K UHD Blu-Ray",
                "photo": "AgACAgIAAxkBAAPgaElRJ7mO2DarV8lbmUJZGY2yFD8AAobuMRsTekhKNKm0A0Yur94BAAMCAANtAAM2BA"
            },
            "nintendo_switch_oled": {
                "name": "Nintendo Switch OLED",
                "price": 160000,
                "desc": "Играйте где угодно и как угодно. Яркий OLED-экран делает ваши любимые игры еще красочнее.",
                "specs": "<b>Экран:</b> 7-дюймовый OLED\n"
                         "<b>Память:</b> 64 ГБ встроенной\n"
                         "<b>Режимы:</b> ТВ, настольный, портативный\n"
                         "<b>Контроллеры:</b> Joy-Con (съемные)\n"
                         "<b>Время работы:</b> 4.5 - 9 часов",
                "photo": "AgACAgIAAxkBAAPeaElRIin6xvLsFmB292VndtAEQhYAAoPuMRsTekhKVM1wQPT65UcBAAMCAANtAAM2BA"
            },
            "steam_deck": {
                "name": "Valve Steam Deck",
                "price": 250000,
                "desc": "Портативный ПК для игр. Вся ваша библиотека Steam теперь у вас в руках.",
                "specs": "<b>Процессор:</b> AMD APU (Zen 2 + RDNA 2)\n"
                         "<b>Память:</b> 16 ГБ LPDDR5\n"
                         "<b>Накопитель:</b> 256 ГБ NVMe SSD (в этой версии)\n"
                         "<b>Экран:</b> 7-дюймовый LCD, 1280x800\n"
                         "<b>ОС:</b> SteamOS 3.0",
                "photo": "AgACAgIAAxkBAAPcaElRG0V8m6OhngHZyH3j5Ix9J5cAAgvuMRvonUlKG2sWjGpdO4YBAAMCAANtAAM2BA"
            }
        }
    }
}