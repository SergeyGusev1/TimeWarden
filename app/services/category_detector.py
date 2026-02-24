from enum import Enum
from typing import Dict, List, Optional


class AppCategory(str, Enum):
    """Категории приложений"""
    PRODUCTIVE = "productive"      # Полезное (учёба, работа)
    NEUTRAL = "neutral"            # Нейтральное (браузер, файлы)
    WASTEFUL = "wasteful"          # Вредное (игры, фильмы)
    UNKNOWN = "unknown"            # Неизвестное


class CategoryDetector:
    """Определитель категорий приложений"""

    # Словарь категорий с ключевыми словами
    CATEGORY_KEYWORDS: Dict[AppCategory, List[str]] = {
        AppCategory.PRODUCTIVE: [
            # IDE и редакторы
            "code", "pycharm", "idea", "vscode", "visual studio", "sublime",
            "webstorm", "eclipse", "netbeans", "xcode", "android studio",
            # Учёба
            "pdf", "lecture", "coursera", "udemy", "stepik", "geekbrains",
            "skillbox", "yandex practicum", "book", "ebook", "dictionary",
            "translate", "translator", "microsoft word", "excel", "powerpoint",
            "notion", "obsidian", "roam", "evernote", "onenote",
            # Документы
            "document", "spreadsheet", "presentation", "pdf reader",
            "adobe acrobat", "foxit", "word", "excel", "powerpoint",
            # Терминалы и DevOps
            "terminal", "cmd", "powershell", "putty", "wsl", "docker",
            "kubernetes", "kubectl", "postman", "insomnia", "grafana",
            "prometheus", "jenkins", "gitlab", "github desktop",
        ],

        AppCategory.NEUTRAL: [
            # Браузеры
            "browser", "chrome", "firefox", "opera", "edge", "safari",
            "yandex browser", "brave", "tor", "chromium",
            # Файловые менеджеры
            "explorer", "finder", "total commander", "far manager",
            "directory", "file manager",
            # Системные
            "system", "settings", "preferences", "control panel",
            "task manager", "activity monitor", "launcher",
            # Коммуникация (нейтрально, зависит от контекста)
            "slack", "teams", "discord", "telegram", "whatsapp",
            "zoom", "skype", "meet", "webex", "messenger",
            # Почта
            "outlook", "thunderbird", "mail", "spark",
        ],

        AppCategory.WASTEFUL: [
            # Игры
            "game", "steam", "epic", "origin", "battle.net", "ubisoft",
            "minecraft", "dota", "csgo", "counter-strike", "warcraft",
            "world of warcraft", "wow", "league of legends", "lol",
            "cyberpunk", "gta", "red dead", "fortnite", "pubg",
            "apex legends", "valorant", "overwatch", "diablo",
            # Развлечения
            "netflix", "youtube", "twitch", "kinopoisk", "ivi", "okko",
            "megogo", "spotify", "apple music", "yandex music",
            "vk video", "tiktok", "instagram", "facebook", "vk",
            # Торренты
            "utorrent", "bittorrent", "qbittorrent", "transmission",
            "deluge", "vuze", "media player", "vlc", "kmplayer",
            "potplayer", "movist", "plex", "kodi",
        ]
    }

    @classmethod
    def detect(cls, app_name: str, window_title: str = "") -> AppCategory:
        """
        Определяет категорию приложения по названию и заголовку окна

        Args:
            app_name: Название приложения/процесса
            window_title: Заголовок окна (может уточнить категорию)

        Returns:
            AppCategory: Определённая категория
        """
        app_lower = app_name.lower()
        window_lower = window_title.lower()

        window_category = cls._check_window_title(window_lower)
        if window_category:
            return window_category

        return cls._check_app_name(app_name=app_lower)

    @classmethod
    def _check_window_title(cls, window_title: str) -> Optional[AppCategory]:
        """Проверка заголовка окна"""
        productive_indicators = [
            "lecture", "tutorial", "course", "lesson", "homework",
            "assignment", "lab", "practice", "study", "learning",
            "документ", "лекция", "курс", "урок", "дз", "домашнее задание"
        ]

        wasteful_indicators = [
            "youtube", "twitch", "netflix", "game", "play", "watch",
            "смотреть", "игра", "сериал", "фильм", "ютуб", "ютюб"
        ]

        for indicator in productive_indicators:
            if indicator in window_title:
                return AppCategory.PRODUCTIVE

        for indicator in wasteful_indicators:
            if indicator in window_title:
                return AppCategory.WASTEFUL

        return None

    @classmethod
    def _check_app_name(cls, app_name: str) -> AppCategory:
        """Проверка названия приложения"""
        for category, keywords in cls.CATEGORY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in app_name:
                    return category
        return AppCategory.UNKNOWN
