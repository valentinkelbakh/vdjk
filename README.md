# VDJK Bot

This is Telegram bot made for [VDJK Hackathon 2023](https://vdjk.kz/hackaton2023).

It's main purpose is to offer information about traditional german dishes and holidays, and about upcoming projects from VDJK.

## Installation

Install as pretty much any python program

For windows
```
git clone https://github.com/valentinkelbakh/hackaton2023.git
cd hackaton2023
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
```

For Linux:
```
git clone https://github.com/valentinkelbakh/hackaton2023.git
cd hackaton2023
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Before start create .env file in /app folder with following content:
```
API_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
```
Note: `API_TOKEN` should be your Telegram Bot token, which you can obtain from BotFather.


To start the bot:
```
python run.py
```