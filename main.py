import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from fetch_market_data import fetch_market_data
from historical_graph import plot_historical_graph, plot_backtest_results
from SMAalgo import backtest_sma_strategy, save_trades_to_csv, optimize_sma_windows
import pandas as pd
import json
import os

def main():
    # Create the main window
    root = tk.Tk()
    root.title("Automated Stock Trading Program")

    # Create and place the widgets
    tk.Label(root, text="Select Symbol (FNGU or FNGD):").grid(row=0, column=0, padx=5, pady=5)
    symbol_entry = tk.Entry(root)
    symbol_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(root, text="Start Date (MM/DD/YYYY):").grid(row=1, column=0, padx=5, pady=5)
    start_date_entry = tk.Entry(root)
    start_date_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(root, text="End Date (MM/DD/YYYY):").grid(row=2, column=0, padx=5, pady=5)
    end_date_entry = tk.Entry(root)
    end_date_entry.grid(row=2, column=1, padx=5, pady=5)

    def plot_graph():
        symbol = symbol_entry.get().strip().upper()
        start_date_str = start_date_entry.get().strip()
        end_date_str = end_date_entry.get().strip()

        # Validate symbol
        if symbol not in ['FNGU', 'FNGD']:
            messagebox.showerror("Error", "Invalid symbol. Please enter 'FNGU' or 'FNGD'.")
            return

        # Validate dates
        try:
            start_date = datetime.strptime(start_date_str, "%m/%d/%Y")
            end_date = datetime.strptime(end_date_str, "%m/%d/%Y")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use MM/DD/YYYY.")
            return

        if start_date >= end_date:
            messagebox.showerror("Error", "Start date must be before end date.")
            return

        # Read data from JSON file
        json_filename = f"{symbol}_data.json"
        if not os.path.exists(json_filename):
            # Fetch data and save to JSON file
            success = fetch_market_data(symbol, '2021-01-01', datetime.today().strftime('%Y-%m-%d'), json_filename)
            if not success:
                messagebox.showerror("Error", "Failed to fetch data. Please check the symbol and your internet connection.")
                return

        # Load data from JSON file
        with open(json_filename, 'r') as json_file:
            data_list = json.load(json_file)
            if not isinstance(data_list, list) or len(data_list) == 0:
                messagebox.showerror("Error", "No data found in the JSON file.")
                return
            try:
                data = pd.DataFrame(data_list)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create DataFrame: {e}")
                return

        # Filter data between start_date and end_date
        data['Date'] = pd.to_datetime(data['Date'])
        data.set_index('Date', inplace=True)
        mask = (data.index >= start_date) & (data.index <= end_date)
        filtered_data = data.loc[mask].copy()

        if filtered_data.empty:
            messagebox.showinfo("No Data", "No data available for the selected date range.")
            return

        # Plot the historical graph
        plot_historical_graph(filtered_data, symbol, start_date_str, end_date_str)

    def run_backtest():
        symbol = symbol_entry.get().strip().upper()
        start_date_str = start_date_entry.get().strip()
        end_date_str = end_date_entry.get().strip()

        # Validate symbol
        if symbol not in ['FNGU', 'FNGD']:
            messagebox.showerror("Error", "Invalid symbol. Please enter 'FNGU' or 'FNGD'.")
            return

        # Validate dates
        try:
            start_date = datetime.strptime(start_date_str, "%m/%d/%Y")
            end_date = datetime.strptime(end_date_str, "%m/%d/%Y")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use MM/DD/YYYY.")
            return

        if start_date >= end_date:
            messagebox.showerror("Error", "Start date must be before end date.")
            return

        # Read data from JSON file
        json_filename = f"{symbol}_data.json"
        if not os.path.exists(json_filename):
            # Fetch data and save to JSON file
            success = fetch_market_data(symbol, '2021-01-01', datetime.today().strftime('%Y-%m-%d'), json_filename)
            if not success:
                messagebox.showerror("Error", "Failed to fetch data. Please check the symbol and your internet connection.")
                return

        # Load data from JSON file
        with open(json_filename, 'r') as json_file:
            data_list = json.load(json_file)
            if not isinstance(data_list, list) or len(data_list) == 0:
                messagebox.showerror("Error", "No data found in the JSON file.")
                return
            try:
                data = pd.DataFrame(data_list)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create DataFrame: {e}")
                return

        # Filter data between start_date and end_date
        data['Date'] = pd.to_datetime(data['Date'])
        data.set_index('Date', inplace=True)
        mask = (data.index >= start_date) & (data.index <= end_date)
        filtered_data = data.loc[mask].copy()

        if filtered_data.empty:
            messagebox.showinfo("No Data", "No data available for the selected date range.")
            return

        # Optimize SMA windows to find at least one profitable trade
        result = optimize_sma_windows(filtered_data, symbol)

        if result[0] is None:
            messagebox.showinfo("Optimization Result", "No profitable SMA window combination found.")
            return

        final_balance, trade_log, data_with_signals, short_window, long_window = result

        # Save the backtest results to CSV
        save_trades_to_csv(trade_log, final_balance)

        # Plot the backtest results with SMAs and trading signals
        plot_backtest_results(data_with_signals, symbol, start_date_str, end_date_str)

        messagebox.showinfo(
            "Backtest Complete",
            f"Backtest complete using SMA windows: short={short_window}, long={long_window}.\n"
            f"Final balance: ${final_balance:,.2f}\n"
            "Trades saved to sma_crossover_trades.csv."
        )

    # Create buttons
    tk.Button(root, text="Plot Historical Graph", command=plot_graph).grid(row=3, column=0, padx=5, pady=5)
    tk.Button(root, text="Run SMA Backtest", command=run_backtest).grid(row=3, column=1, padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
