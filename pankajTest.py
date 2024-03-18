import pandas as pd
import requests
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np

def fetch_creditors_data():
    try:
        clocations = requests.get("http://api.worldbank.org/v2/sources/6/counterpart-area?per_page=300&format=JSON")
        clocationsJSON = clocations.json()
        clocations = clocationsJSON["source"][0]["concept"][0]["variable"]
        creditor_data = [{"id": loc["id"], "value": loc["value"]} for loc in clocations]
        messagebox.showinfo("Success", "Creditor data fetched successfully!")
        return creditor_data
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch creditor data: {str(e)}")
        return None

def top_10_most_credit_countries():
    try:
        creditor_data = fetch_creditors_data()
        if creditor_data:
            df = pd.DataFrame(creditor_data)
            top_10_most_credit = df.nlargest(10, 'id')
            plt.bar(top_10_most_credit['value'], top_10_most_credit['id'])
            plt.xlabel('Country')
            plt.ylabel('Credit')
            plt.title('Top 10 Countries with Most Credit')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to display top 10 most credit countries: {str(e)}")

def top_10_least_credit_countries():
    try:
        creditor_data = fetch_creditors_data()
        if creditor_data:
            df = pd.DataFrame(creditor_data)
            top_10_least_credit = df.nsmallest(10, 'id')
            plt.bar(top_10_least_credit['value'], top_10_least_credit['id'])
            plt.xlabel('Country')
            plt.ylabel('Credit')
            plt.title('Top 10 Countries with Least Credit')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to display top 10 least credit countries: {str(e)}")

def credit_distribution_pie_chart():
    try:
        creditor_data = fetch_creditors_data()
        if creditor_data:
            df = pd.DataFrame(creditor_data)
            credit_values = df['id']
            country_names = df['value']

            explode = np.zeros(len(credit_values))
            explode[credit_values.idxmax()] = 0.1

            plt.pie(credit_values, labels=country_names, explode=explode, autopct='%1.1f%%', startangle=140)
            plt.axis('equal')
            plt.title('Credit Distribution Among Creditors')
            plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to display credit distribution pie chart: {str(e)}")

# GUI setup
root = tk.Tk()
root.title("Creditor Credit Analysis")

# Buttons
btn_top_10_most_credit = tk.Button(root, text="Top 10 Most Credit Countries", command=top_10_most_credit_countries)
btn_top_10_most_credit.pack(pady=5)

btn_top_10_least_credit = tk.Button(root, text="Top 10 Least Credit Countries", command=top_10_least_credit_countries)
btn_top_10_least_credit.pack(pady=5)

btn_credit_distribution = tk.Button(root, text="Credit Distribution Pie Chart", command=credit_distribution_pie_chart)
btn_credit_distribution.pack(pady=5)

root.mainloop()
