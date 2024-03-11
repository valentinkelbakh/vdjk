# VDJKate

This is Telegram bot made for VDJK (Verband der Deutschen Jugend Kasachstans)

It's main purpose is to offer information about traditional german dishes and holidays, and about upcoming projects from VDJK.

It was initially created for [VDJK Hackathon 2023](https://vdjk.kz/hackaton2023).
I continued developing this bot after Hackathon for a while and this is latest version of the bot.



## Installation

First set up a [Database](https://github.com/valentinkelbakh/vdjk_db) for this bot.

Then:

For windows:
```bat
git clone https://github.com/valentinkelbakh/vdjk.git
cd vdjk
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
pybabel compile -d app/locales
```

For Linux:
```bash
git clone https://github.com/valentinkelbakh/vdjk.git
cd vdjk
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
pybabel compile -d app/locales
```

Before start create .env file, based on .env.example.
API_LOGIN, API_PASSWORD and WEBHOOK_PASS should match appropriate values used during database installation.

To start the bot:
```
python -m app
```
