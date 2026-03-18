import ctypes
from ctypes import wintypes
import psutil
import requests
import time
from datetime import datetime

# ========== КОНФИГУРАЦИЯ ==========
SERVER_URL = "http://localhost:8000"
CHECK_INTERVAL = 5      # проверка каждые 5 секунд
SEND_INTERVAL = 30      # отправка раз в 30 секунд
# ==================================


class SimpleAgent:
    def __init__(self):
        self.current_app = None
        self.current_window = None
        self.start_time = None
        self.buffer = []
        self.last_send = time.time()

    def get_active_window_info(self):
        """Получает имя процесса и заголовок активного окна"""
        try:
            user32 = ctypes.windll.user32

            # Получаем handle активного окна
            hwnd = user32.GetForegroundWindow()

            # Получаем PID процесса
            pid = wintypes.DWORD()
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))

            # Получаем заголовок окна
            length = user32.GetWindowTextLengthW(hwnd)
            buffer = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buffer, length + 1)
            window_title = buffer.value

            # Получаем имя процесса по PID
            try:
                process = psutil.Process(pid.value)
                app_name = process.name()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                app_name = f"unknown (pid:{pid.value})"

            return app_name, window_title

        except Exception as e:
            print(f"⚠️ Ошибка получения окна: {e}")
            return "unknown", "unknown"

    def run(self):
        """Основной цикл работы"""
        print("🟢 Агент запущен")
        print(f"📡 Сервер: {SERVER_URL}")
        print(f"⏱️  Проверка: каждые {CHECK_INTERVAL}с")
        print(f"📦 Отправка: раз в {SEND_INTERVAL}с")
        print("-" * 50)

        try:
            while True:
                # Получаем текущее активное окно
                app, window = self.get_active_window_info()
                now = datetime.now()

                # Если сменилось приложение или окно
                if app != self.current_app or window != self.current_window:
                    # Если была предыдущая активность - сохраняем
                    if self.current_app and self.start_time:
                        duration = (now - self.start_time).total_seconds()
                        if duration > 1:  # игнорируем меньше секунды
                            activity = {
                                "app_name": self.current_app,
                                "window_title": self.current_window,
                                "duration_seconds": round(duration, 1),
                                "start_time": self.start_time.isoformat(),
                                "end_time": now.isoformat()
                            }
                            self.buffer.append(activity)
                            print(f"📝 {self.current_app}: {duration:.1f}с — {self.current_window[:40]}")

                    # Начинаем новую активность
                    self.current_app = app
                    self.current_window = window
                    self.start_time = now

                # Отправляем данные если пора
                if time.time() - self.last_send > SEND_INTERVAL and self.buffer:
                    self._send_buffer()

                time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            print("\n🛑 Останавливаем агента...")
            # Отправляем остатки
            if self.current_app and self.start_time:
                duration = (datetime.now() - self.start_time).total_seconds()
                if duration > 1:
                    self.buffer.append({
                        "app_name": self.current_app,
                        "window_title": self.current_window,
                        "duration_seconds": round(duration, 1),
                        "start_time": self.start_time.isoformat(),
                        "end_time": datetime.now().isoformat()
                    })
            self._send_buffer()
            print("👋 Агент завершил работу")

    def _send_buffer(self):
        """Отправка накопленных данных на сервер"""
        if not self.buffer:
            return

        successful = []
        failed = []

        for activity in self.buffer:
            try:
                response = requests.post(
                    f"{SERVER_URL}/api/v1/activity",
                    json=activity,
                    timeout=5
                )
                if response.status_code == 201:
                    successful.append(activity)
                else:
                    failed.append(activity)
            except requests.exceptions.ConnectionError:
                failed.append(activity)
                break  # сервер недоступен - не пытаемся дальше
            except Exception:
                failed.append(activity)

        if successful:
            print(f"📤 Отправлено: {len(successful)}")

        if failed:
            print(f"⏳ Осталось в буфере: {len(failed)}")
            self.buffer = failed
        else:
            self.buffer = []

        self.last_send = time.time()


if __name__ == "__main__":
    agent = SimpleAgent()
    agent.run()