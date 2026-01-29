# Crypto Price Tracker

This is a desktop application designed to monitor real-time prices for Bitcoin and Ethereum using the Binance API. I developed this project to practice building GUI applications with Tkinter, handling network requests, and managing local data storage with SQLite.

The program polls the API at one-second intervals and displays the current price. It includes functionality to save the current price into a local database and a text file for future reference. There is also a history viewer built directly into the app to check previous records. The technical stack includes Python 3 along with the requests and sqlite3 libraries.

---

Це десктопний додаток для моніторингу цін на Bitcoin та Ethereum у реальному часі через API Binance. Я розробив цей проект, щоб попрактикуватися у створенні графічних інтерфейсів на Tkinter, роботі з мережевими запитами та збереженні даних у локальній базі SQLite.

Програма опитує API з інтервалом в одну секунду та відображає актуальну вартість. Реалізовано можливість збереження поточної ціни в базу даних та текстовий файл. Також додано вікно історії для перегляду всіх попередніх записів. Для роботи проекту використано Python 3, бібліотеку requests та вбудований модуль sqlite3.

---

### Setup and Installation

To get this project running locally, you need to clone the repository and ensure you have Python 3 installed. This project uses several development tools and libraries specified in the requirements file.

First, install the necessary dependencies using the following command in your terminal:

pip install -r requirements.txt

Once the installation is complete, launch the application by running the main script:

python tracking.py

The application will handle the initial database setup automatically upon the first run. A stable internet connection is required to fetch live price data from the API.