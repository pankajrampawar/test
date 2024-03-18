import tkinter as tk
from tkinter import ttk, messagebox
import requests

# Function to fetch debtor country codes and display them in tkinter GUI
def fetch_and_display_debtor_country_codes():
    try:
        # Requesting the locations
        dlocations = requests.get("http://api.worldbank.org/v2/sources/6/country?per_page=300&format=JSON")
        dlocationsJSON = dlocations.json()

        # Parse through the response to get the location IDs and names
        dlocations = dlocationsJSON["source"][0]["concept"][0]["variable"]
        debtor_countries = [(loc["id"], loc["value"]) for loc in dlocations]
        print(debtor_countries)

        # Clear existing data in Treeview
        for item in tree.get_children():
            tree.delete(item)

        # Display debtor country codes in the tkinter GUI
        for idx, (country_id, country_name) in enumerate(debtor_countries, start=1):
            tree.insert("", "end", values=(idx, country_id, country_name))

    except Exception as e:
        messagebox.showwarning("Warning", "Failed to fetch debtor country codes. Showing sample data instead.")
        # Sample data
        sample_data = [
            ("1", "IND", "India"),
            ("2", "USA", "United States"),
            ("3", "CHN", "China"),
            ("4", "GBR", "United Kingdom"),
            ("5", "DEU", "Germany")
        ]
        
        # Display sample data in the Treeview widget
        for idx, (country_id, country_code, country_name) in enumerate(sample_data, start=1):
            tree.insert("", "end", values=(idx, country_code, country_name))

# GUI setup
root = tk.Tk()
root.title("Debtor Country Codes")

# Treeview for displaying debtor country codes
tree = ttk.Treeview(root, columns=("Index", "Country Code", "Country Name"), show="headings")
tree.heading("Index", text="Index")
tree.heading("Country Code", text="Country Code")
tree.heading("Country Name", text="Country Name")
tree.pack(fill="both", expand=True)

# Button to fetch and display debtor country codes
btn_fetch_data = tk.Button(root, text="Fetch Debtor Country Codes", command=fetch_and_display_debtor_country_codes)
btn_fetch_data.pack(pady=10)

# Run the main event loop
root.mainloop()
