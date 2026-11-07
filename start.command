#!/bin/bash
# Сайт БГИТУ — локальный сервер для macOS / Linux. Двойной клик в Finder или ./start.command
cd "$(dirname "$0")"
PORT=8792
URL="http://127.0.0.1:$PORT/"
echo "Сайт БГИТУ: $URL  (остановить — Ctrl+C или закрыть окно)"
( sleep 1; command -v open >/dev/null && open "$URL" || xdg-open "$URL" ) >/dev/null 2>&1 &
if command -v python3 >/dev/null; then python3 -m http.server "$PORT" --bind 127.0.0.1
elif command -v npx >/dev/null; then npx --yes serve -l "$PORT" .
else echo "Нужен Python 3: https://www.python.org/downloads/"; read -r; fi
