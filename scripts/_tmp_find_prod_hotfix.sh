#!/bin/bash
set -e
echo "=== recently modified py/js/html under sources+scripts (3 days) ==="
find /var/www/ielts/sources /var/www/ielts/scripts -type f \( -name "*.py" -o -name "*.js" -o -name "*.html" \) -mtime -3 -printf "%T+ %p\n" 2>/dev/null | sort -r | head -60
echo "=== P4genduceshi ==="
ls -la --time-style=long-iso /var/www/ielts/sources/P4genduceshi/
echo "=== key scripts mtime ==="
ls -la --time-style=long-iso /var/www/ielts/scripts/local_server.py /var/www/ielts/scripts/task_api.py /var/www/ielts/sources/P4genduceshi/config.js /var/www/ielts/sources/P4genduceshi/index.html
echo "=== service restart logs? ==="
ls -lt /root/ielts_backups 2>/dev/null | head -8
journalctl -u ielts --since "2026-10-22 18:00" --no-pager 2>/dev/null | tail -30 || true
