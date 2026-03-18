from __future__ import annotations

import threading
import uuid
from typing import Callable, Optional


def keep_online(
    client,
    on_event: Optional[Callable[[str, dict | None], None]] = None,
    background: bool = True,
) -> threading.Thread | None:
    """
    Поддерживает статус "в сети" через SSE-поток /api/notifications/stream.

    Параметры:
        on_event  — колбэк(event_type, data) для входящих событий (лайк, комментарий и т.д.)
        background — True: запускает в фоновом потоке и сразу возвращает Thread
                     False: блокирует текущий поток (используй в простых скриптах)

    Пример:
        # Фоновый режим
        thread = client.keep_online()

        # С обработкой событий
        def handler(event, data):
            print(f"Новое событие: {event}", data)
        client.keep_online(on_event=handler)
    """
    def _run():
        import time

        # Уникальный device_id на всё время жизни соединения
        device_id = str(uuid.uuid4())
        client.session.headers.setdefault("x-device-id", device_id)
        client.session.headers.setdefault("x-requested-with", "XMLHttpRequest")

        while True:
            try:
                response = client.session.get(
                    f"{client.base_url}/api/notifications/stream",
                    stream=True,
                    timeout=(10, 600),
                    headers={
                        "Accept": "text/event-stream",
                        "Cache-Control": "no-cache",
                    },
                )

                if response.status_code == 401:
                    if client._auth_manager:
                        client._auth_manager.refresh_access_token()
                    continue

                if response.status_code == 429:
                    time.sleep(60)
                    continue

                if response.status_code != 200:
                    time.sleep(10)
                    continue

                event_type = None
                for raw_line in response.iter_lines():
                    if not raw_line:
                        event_type = None
                        continue

                    line = raw_line.decode("utf-8") if isinstance(raw_line, bytes) else raw_line

                    # пинги игнорируем
                    if line.startswith(": ping"):
                        continue

                    if line.startswith("event:"):
                        event_type = line[len("event:"):].strip()

                    elif line.startswith("data:") and on_event and event_type:
                        import json
                        raw = line[len("data:"):].strip()
                        try:
                            data = json.loads(raw)
                        except Exception:
                            data = {"raw": raw}
                        if event_type != "connected":
                            on_event(event_type, data)

            except Exception:
                time.sleep(5)

    if background:
        t = threading.Thread(target=_run, daemon=True)
        t.start()
        return t
    else:
        _run()
        return None
