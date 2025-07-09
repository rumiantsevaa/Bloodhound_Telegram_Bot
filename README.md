# Bloodhound Telegram Bot

@BloodhoundRBot is a Python Telegram bot designed for convenient image search by text and reverse image search.

![1](https://github.com/rumiantsevaa/Bloodhound_Telegram_Bot/assets/89034072/ef195d97-31fa-472e-8b5b-cb8b8fea7f29)

## Key Features

### Royalty Free Image Search
- Search for copyright-free images using text queries
- Powered by Pixabay API
- Supports both English and Russian queries
- **New:** Daily limit of 1 search per user to ensure fair usage

![2](https://github.com/rumiantsevaa/Bloodhound_Telegram_Bot/assets/89034072/d2e33f67-8ee5-4d6f-af95-b2cd3c9d7f16)

### Google Reverse Image Search
- Upload photos to find similar images online
- Uses Google Reverse Image Search via SerpApi
- **New:** 24/7 availability through PythonAnywhere hosting
- **New:** 1 search per day limit per user

![3](https://github.com/rumiantsevaa/Bloodhound_Telegram_Bot/assets/89034072/65e8e545-f96c-43f7-95b3-07f8defd9d63)

### Yandex Reverse Image Search
- Alternative reverse image search option
- Powered by Yandex API through SerpApi
- **New:** Stable hosting with daily search limits

![4](https://github.com/rumiantsevaa/Bloodhound_Telegram_Bot/assets/89034072/6d8437fb-2fba-4f3e-b3a5-a50fdfa7fbad)

## Usage

### Button Navigation
Simple menu-driven interface for all features:

![5](https://github.com/rumiantsevaa/Bloodhound_Telegram_Bot/assets/89034072/4181612c-2ef5-47c5-beb1-dfc80f2147a5)

1. Expand the button menu
2. Choose your search type
3. Follow the instructions
4. Receive your results

**Note:** Each search type can be used once per 24 hours per user due to API limitations.

## Technical Details

### Important Updates
- Now hosted on PythonAnywhere for 24/7 availability
- Added SQLite database to track user searches
- Implemented fair usage policy (1 search/type/day)
- Removed repeat search functionality to conserve resources
- Added complete requirements.txt for easier setup

### Dependencies
- `telebot` – interaction with the Telegram Bot API (via pyTelegramBotAPI)
- `requests` – handling HTTP requests to external APIs (Pixabay, SerpAPI, etc.)
- `sqlite3` – built-in database for per-user search tracking and daily usage limits
- `datetime` – used for checking and resetting daily search limits
- `pixabay` – optional helper library for accessing Pixabay image search API
- `config.py` – custom file for securely storing API keys (Telegram, SerpAPI, Pixabay)

### Installation
1. Use the live bot: [@BloodhoundRBot](https://t.me/BloodhoundRBot)
   
OR

1. Self-host:
   ```bash
   git clone https://github.com/rumiantsevaa/Bloodhound_Telegram_Bot.git
 
2. Add your API keys to config.py

### Privacy Notice
This is a non-commercial project that:

* Doesn't store your images or search history
* Doesn't collect personal data
* Uses official API services with their own privacy policies
