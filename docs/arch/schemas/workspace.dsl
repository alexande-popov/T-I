workspace "Инвестиционное приложение" {

    model {
        // ---------- Люди ----------
        user = person "Пользователь" "Инвестор. Смотрит портфель, анализирует, подтверждает сделки."
        operator = person "Оператор" "Администратор. Запускает backfill, настраивает расписание, восстанавливает БД."

        // ---------- Система ----------
        app = softwareSystem "Инвестиционное приложение" "Персональный ассистент для анализа и торговли на T-Bank Invest API." {

            // ---------- Контейнеры ----------
            cli = container "CLI" "Командная строка для операторских задач." "Python"
            bot = container "Telegram Bot" "Интерфейс пользователя в чате: просмотр портфеля, подтверждение сделок, kill switch." "Python, aiogram"
            web = container "Streamlit Dashboard" "Веб-интерфейс для аналитики: графики, структура портфеля, динамика." "Python, Streamlit"
            scheduler = container "Scheduler" "Фоновый процесс по расписанию: снимки портфеля, обновление котировок, пересчёт метрик." "Python, APScheduler"
            robot = container "Trading Robot" "Фоновый процесс исполнения стратегий: сигналы, проверка лимитов, отправка ордеров." "Python"
            core = container "Application Core" "Общая библиотека с доменной логикой: Portfolio Store, Model, Analytics, Tax, Strategy, Risk, Executor." "Python"
            db = container "Database" "Хранилище операций, снимков, цен и счетов." "SQLite" {
                tags "Database"
            }
        }

        // ---------- Внешние системы ----------
        tbankApi = softwareSystem "T-Bank Invest API" "Предоставляет данные о котировках и операциях, принимает торговые заявки." {
            tags "External System"
        }

        externalData = softwareSystem "Внешние данные" "Источники курсов валют и рыночных индексов (IMOEX, RTS)." {
            tags "External System"
        }

        // ---------- Связи: люди → интерфейсы ----------
        user -> bot "Смотрит портфель, подтверждает сделки, kill switch"
        user -> web "Смотрит графики, аналитику, структуру портфеля"
        operator -> cli "Запускает backfill, миграции, настройку расписания"

        // ---------- Связи: интерфейсы → ядро ----------
        cli -> core "Вызывает команды ядра"
        bot -> core "Запрашивает данные и передаёт подтверждения"
        web -> core "Запрашивает метрики и ряды"

        // ---------- Связи: фоновые процессы → ядро ----------
        scheduler -> core "Запускает периодические задачи"
        robot -> core "Запускает стратегии и исполнение"

        // ---------- Связи: ядро → инфраструктура ----------
        core -> db "Читает и пишет данные"
        core -> tbankApi "Получает котировки и операции, отправляет заявки"
        core -> externalData "Получает курсы валют и индексы"

        // ---------- Обратные связи: уведомления ----------
        robot -> bot "Отправляет запросы на подтверждение"
        scheduler -> bot "Отправляет алерты"
    }

    views {
        // ---------- Диаграмма контейнеров ----------
        container app "Containers" {
            include *
            autoLayout tb
        }

        // ---------- Стили ----------
        styles {
            element "Person" {
                shape Person
                background "#08427b"
                color "#ffffff"
            }
            element "Software System" {
                background "#1168bd"
                color "#ffffff"
            }
            element "Container" {
                background "#438dd5"
                color "#ffffff"
            }
            element "Database" {
                shape Cylinder
                background "#438dd5"
                color "#ffffff"
            }
            element "External System" {
                background "#999999"
                color "#ffffff"
            }
        }
    }
}