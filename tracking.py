import requests
import tkinter as tk
from tkinter import messagebox  
import datetime
import sqlite3
import time

#Constants
DB_FILE = "prices.db"
API_URL = "https://api.binance.com/api/v3/ticker/price"
SYMBOLS = ["BTCUSDT", "ETHUSDT"]
UPDATE_INTERVAL_MS = 1000  

#Global State
latest_prices = {
    "BTC": 0.0,
    "ETH": 0.0
}
tracking_active = False
after_id = None 

#Database Functions
def init_db():
    """Initializes the database and creates the table if it doesn't exist."""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS prices
                              (timestamp TEXT, btc_price REAL, eth_price REAL)''')
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Could not initialize database: {e}")
        root.quit()

#API Functions
def fetch_prices():
    """Fetches prices from the API and updates the global state. Returns True on success."""
    try:
        # Make requests for all symbols
        response_btc = requests.get(API_URL, params={"symbol": "BTCUSDT"})
        response_eth = requests.get(API_URL, params={"symbol": "ETHUSDT"})

        # Check if the requests were successful
        response_btc.raise_for_status()
        response_eth.raise_for_status()

        # Update the global price dictionary
        latest_prices["BTC"] = float(response_btc.json()["price"])
        latest_prices["ETH"] = float(response_eth.json()["price"])
        return True

    except requests.exceptions.RequestException as e:
        # Handle network errors or bad responses from the API
        print(f"Error fetching data: {e}") 
        price_label.config(text="Error fetching prices...\nRetrying...")
        return False
    except (KeyError, ValueError) as e:
        # Handle cases where the JSON from the API is not as expected
        print(f"Error parsing data: {e}")
        price_label.config(text="Error parsing data...")
        return False

#UI Functions
def update_price_display():
    """Fetches new prices and updates the UI label. Schedules itself to run again."""
    global after_id
    if not tracking_active:
        return

    if fetch_prices():
        # Update the label text using data from the `latest_prices` variable
        price_text = f"BTC: ${latest_prices['BTC']:.2f}\nETH: ${latest_prices['ETH']:.2f}"
        price_label.config(text=price_text)

    # Schedule the next update
    after_id = root.after(UPDATE_INTERVAL_MS, update_price_display)

def start_tracking():
    """Starts the price tracking loop and updates the UI."""
    global tracking_active
    if tracking_active:
        return

    tracking_active = True
    # Update button states for better user experience
    start_button.pack_forget()
    stop_button.pack(pady=10)
    save_button.config(state=tk.NORMAL) 
    price_label.pack(pady=10)
    update_price_display() 

def stop_tracking():
    """Stops the price tracking loop."""
    global tracking_active, after_id
    if not tracking_active:
        return

    tracking_active = False
    if after_id:
        root.after_cancel(after_id) # Cancel the scheduled update
        after_id = None

    # Update button states
    stop_button.pack_forget()
    start_button.pack(pady=10)
    save_button.config(state=tk.DISABLED) 
    price_label.config(text="Tracking stopped")

def save_current_price():
    """Saves the current price from the `latest_prices` variable to the database."""
    if not tracking_active or latest_prices["BTC"] == 0.0:
        messagebox.showwarning("Warning", "No price data to save. Start tracking first.")
        return

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    btc_price = latest_prices["BTC"]
    eth_price = latest_prices["ETH"]

    # Save to database
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO prices (timestamp, btc_price, eth_price) VALUES (?, ?, ?)",
                           (now, btc_price, eth_price))
            conn.commit()
            messagebox.showinfo("Success", "Price saved successfully!")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Could not save data: {e}")

    # The logic for writing to a text file 
    with open("remember.txt", 'a') as f:
        f.write(f"{now}\nBTC: ${btc_price:.2f}, ETH: ${eth_price:.2f}\n\n")

def show_db_data():
    """Displays all saved data from the database in a new window."""
    data_window = tk.Toplevel(root)
    data_window.title("Saved Prices")
    data_window.geometry("450x400")
    data_window.configure(bg="#1c1c1c")

    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM prices ORDER BY timestamp DESC")
            rows = cursor.fetchall()

        if not rows:
            label = tk.Label(data_window, text="No data saved yet.", bg="#1c1c1c", fg="white", font=("Arial", 14))
            label.pack(pady=20)
            return

        # Display data in a Text widget
        text_widget = tk.Text(data_window, bg="#1c1c1c", fg="white", font=("Courier", 12), wrap=tk.WORD, borderwidth=0)
        text_widget.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        for row in rows:
            text_widget.insert(tk.END, f"{row[0]} | BTC: ${row[1]:.2f} | ETH: ${row[2]:.2f}\n")
        text_widget.config(state=tk.DISABLED) 

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Could not fetch data: {e}", parent=data_window)

# GUI Setup 
root = tk.Tk()
root.title("Crypto Price Tracker")
root.geometry("500x400")
root.resizable(False, False)
root.configure(bg="#1c1c1c") 

# Widgets 
common_button_style = {"bg": "#333", "fg": "white", "font": ("Arial", 14), "width": 15, "borderwidth": 0, "activebackground": "#555"}

price_label = tk.Label(root, text="Click 'Start' to begin", bg="#1c1c1c", fg="cyan", font=("Arial", 20))
price_label.pack(pady=20)

start_button = tk.Button(root, text="Start Tracking", command=start_tracking, **common_button_style)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Tracking", command=stop_tracking, **common_button_style)
# Stop button is hidden initially

save_button = tk.Button(root, text="Save Price", command=save_current_price, **common_button_style)
save_button.config(state=tk.DISABLED) # Disabled until tracking starts
save_button.pack(pady=10)

show_button = tk.Button(root, text="Show History", command=show_db_data, **common_button_style)
show_button.pack(pady=10)


if __name__ == "__main__":
    init_db()  
    root.mainloop()
