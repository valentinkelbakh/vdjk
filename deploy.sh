#!/bin/bash

cd /root/vdjk/
git pull
chmod +x /root/vdjk/bot.sh
chmod +x /root/vdjk/deploy.sh
source /root/vdjk/.venv/bin/activate
pip install -r requirements.txt
pybabel compile -d app/locales
./bot.sh restart
