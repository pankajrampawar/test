import pandas as pd
import requests
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np

clocationsList = None

def fetch_creditors_data():
    try:
        global clocationsList
        clocations = requests.get("http://api.worldbank.org/v2/sources/6/counterpart-area?per_page=300&format=JSON")
        clocationsJSON = clocations.json()
        clocations = clocationsJSON["source"][0]["concept"][0]["variable"]
        df = pd.DataFrame(columns=["id", "value"])     
        for i in range(len(clocations)):
            code = clocations[i]["id"]
            name = clocations[i]["value"]
            df = df.append({"id":code, "value":name}, ignore_index = True)
        clocationsList = df
        messagebox.showinfo("Success", "Creditor data fetched successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch creditor data: {str(e)}")

def top_10_most_credit_countries():
    try:
        if clocationsList is None:
            messagebox.showerror("Error", "Please fetch creditor data first.")
            return

        top_10_most_credit = clocationsList.nlargest(10, 'id')
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
        if clocationsList is None:
            messagebox.showerror("Error", "Please fetch creditor data first.")
            return

        top_10_least_credit = clocationsList.nsmallest(10, 'id')
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
        if clocationsList is None:
            messagebox.showerror("Error", "Please fetch creditor data first.")
            return

        credit_values = clocationsList['id']
        country_names = clocationsList['value']

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
btn_fetch_data = tk.Button(root, text="Fetch Creditor Data", command=fetch_creditors_data)
btn_fetch_data.pack(pady=5)

btn_top_10_most_credit = tk.Button(root, text="Top 10 Most Credit Countries", command=top_10_most_credit_countries)
btn_top_10_most_credit.pack(pady=5)

btn_top_10_least_credit = tk.Button(root, text="Top 10 Least Credit Countries", command=top_10_least_credit_countries)
btn_top_10_least_credit.pack(pady=5)

btn_credit_distribution = tk.Button(root, text="Credit Distribution Pie Chart", command=credit_distribution_pie_chart)
btn_credit_distribution.pack(pady=5)

root.mainloop()
