#!/bin/bash
# Setup cron job for async task monitoring

SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/monitor_tasks.py"
CRON_JOB="*/30 * * * * cd $(dirname "$SCRIPT_PATH") && python3 $SCRIPT_PATH >> /var/log/async-task-manager.log 2>&1"

# Add to crontab
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

echo "Cron job added successfully"
echo "Monitor script: $SCRIPT_PATH"
echo "Log file: /var/log/async-task-manager.log"
echo "Cron job runs every 30 minutes"