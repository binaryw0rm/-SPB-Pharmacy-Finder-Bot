# 🏥 binaryw0rm`s SPB Pharmacy Finder Bot

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Aiogram](https://img.shields.io/badge/Aiogram-3.x-blueviolet?style=for-the-badge&logo=telegram)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

A Telegram bot designed to help users find the nearest 24/7 pharmacies in Saint Petersburg. The bot calculates distances using the Haversine formula, generates route links to Google Maps, and includes a full-featured Admin Panel for managing the database directly from Telegram.

## ✨ Features

### 👤 User Features
- **📍 Geolocation Search:** Automatically finds the nearest 24/7 pharmacy based on the user's sent location.
- **🏙 District Search:** Manual selection of city districts (e.g., Central, Moscow, Vyborg) via an interactive menu.
- **🗺 Navigation:** Sends a venue location card and a direct link to build a walking route in Google Maps.
- **ℹ️ Detailed Info:** Displays pharmacy name, address, phone number, and working hours.

### 🛠 Admin Features
- **🔒 Secure Access:** Commands are restricted to the ID specified in `.env`.
- **➕ CRUD Operations:** Add new pharmacies via a step-by-step wizard and delete old ones by ID.
- **📋 Database View:** View a list of all pharmacies with their IDs directly in the chat.
- **💾 CSV Storage:** Data is stored in a CSV file, automatically updated upon changes.

---

## Screenshots

|   |   |   |
|---|---|---|
| ![image1](https://github.com/binaryw0rm/-SPB-Pharmacy-Finder-Bot/blob/main/image1.JPG?raw=true) | ![image2](https://github.com/binaryw0rm/-SPB-Pharmacy-Finder-Bot/blob/main/image2.JPG?raw=true) | ![image3](https://github.com/binaryw0rm/-SPB-Pharmacy-Finder-Bot/blob/main/image3.JPG?raw=true) |
| ![image4](https://github.com/binaryw0rm/-SPB-Pharmacy-Finder-Bot/blob/main/image4.jpg?raw=true) | ![image5](https://github.com/binaryw0rm/-SPB-Pharmacy-Finder-Bot/blob/main/image5.jpg?raw=true) |  |


---
## 🚀 Installation & Setup

### Prerequisites
- Python 3.10+
- Linux Server (Ubuntu/Debian recommended) or Local Machine

### 1. Clone the Repository
```bash
git clone https://github.com/your_username/pharma_bot.git
cd pharma_bot
```
### 2. Set Up Virtual Environment


```
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Linux/MacOS
# venv\Scripts\activate   # Windows
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

### 4. Configuration


Create a .env file in the root directory:
```
nano .env

```
Paste the following content:
```
BOT_TOKEN=your_telegram_bot_token_here
ADMIN_ID=123456789
```

BOT_TOKEN: Get this from @BotFather.
ADMIN_ID: Your numeric Telegram ID (get it from @userinfobot).

### 5. Data Preparation

The database is located at data/pharmacies.csv.
Format (UTF-8, comma-separated, text fields in double quotes):

```
id,name,address,district,phone,working_hours,is_24h,lat,lon
1,"Vita Pharmacy","Nevsky Prospect, 100","Central","+78120000000","24/7",True,59.932,30.356
```

### 6. Run the Bot

```
python main.py
```
## ⚙️ Deployment (Systemd)
To ensure the bot runs in the background and restarts automatically on server reboot:

### 1. Create a service file:

```
sudo nano /etc/systemd/system/pharma_bot.service
```

### 2. Paste the configuration (Edit paths according to your server):

```
Ini
[Unit]
Description=SPB Pharmacy Bot Service
After=network.target

[Service]
User=root
WorkingDirectory=/root/pharma_bot
ExecStart=/root/pharma_bot/venv/bin/python main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### 3. Enable and Start:

```
sudo systemctl daemon-reload
sudo systemctl enable pharma_bot
sudo systemctl start pharma_bot
```

### 4. Check Status:

```
sudo systemctl status pharma_bot
```
## 📚 Bot Commands

Command	Description	Access Level
```
/start	Start the bot and show the main menu	User
/list	Choose a district manually	User
/admin	Open the Admin Panel	Admin Only
/list_all	Show all pharmacies with IDs	Admin Only
/add_pharm	Add a new pharmacy (Wizard)	Admin Only
/del_pharm	Delete a pharmacy by ID	Admin Only
/cancel	Cancel current action	Admin Only
```

## 🔧 Project Structure

```
pharma_bot/
├── data/
│   └── pharmacies.csv      # CSV Database
├── logs/
│   └── bot.log             # Application logs
├── src/
│   ├── __init__.py
│   ├── admin_handlers.py   # Admin logic (CRUD)
│   ├── config.py           # Environment variables loader
│   ├── db_loader.py        # CSV reading/writing logic
│   ├── handlers.py         # User interaction logic
│   ├── keyboards.py        # Inline & Reply keyboards
│   ├── states.py           # FSM States
│   └── utils.py            # Haversine distance calc
├── main.py                 # Entry point
├── geocoding_script.py
├── requirements.txt        # Python dependencies
└── .env                    # Secrets (Excluded from git)
```
---
## License & Author

© 2025 

Free for personal use | Do not resell as your own product

Telegram:@binaryw0rm
