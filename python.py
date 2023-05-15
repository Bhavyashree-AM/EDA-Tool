import tkinter as tk
from tkinter import filedialog
import pandas as pd
from tkinter import messagebox
from tkinter import simpledialog

data = None
eda_data = None  # New DataFrame to store modified data

def open_file():
    global data, eda_data
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        data = pd.read_csv(file_path)
        eda_data = data.copy()  # Make a copy to preserve the original data
        perform_eda()

window = tk.Tk()

open_button = tk.Button(window, text="Open File", command=open_file)
open_button.pack()

def prompt_unique_identifier():
    global data, eda_data
    if eda_data is not None:
        unique_identifier = simpledialog.askstring("Unique Identifier", "Enter the unique identifier column:")
        if unique_identifier:
            print("Unique Identifier Column:", unique_identifier)
            if unique_identifier in eda_data.columns:
                null_count = eda_data[unique_identifier].isnull().sum()
                if null_count > 0:
                    confirm_delete = messagebox.askyesno("Delete Rows", f"There are {null_count} rows with null values in the unique identifier column. Delete these rows?")
                    if confirm_delete:
                        eda_data.dropna(subset=[unique_identifier], inplace=True)
                        print(f"{null_count} rows with null unique identifier values deleted.")
                    else:
                        print("Rows with null unique identifier values were not deleted.")
                else:
                    print("No Null values")
            else:
                print("Invalid unique identifier column.")
        else:
            print("No unique identifier column provided.")
    else:
        print("No data loaded.")

# prompt_button = tk.Button(window, text="Prompt Unique Identifier", command=prompt_unique_identifier)
# prompt_button.pack()

def perform_eda():
    global eda_data
    print("Data Summary:")
    print(eda_data.head())
    print("\nData Statistics:")
    print(eda_data.describe())
    print("Correlation Matrix:")
    numeric_df = eda_data.select_dtypes(include=['int', 'float'])
    print(numeric_df.corr())
    print("Missing Values")
    print(eda_data.isnull().sum())
    prompt_unique_identifier()
    numeric_cols = eda_data.select_dtypes(include=['int', 'float']).columns
    eda_data[numeric_cols] = eda_data[numeric_cols].fillna(eda_data[numeric_cols].mean())
    categorical_cols = eda_data.select_dtypes(include=['object']).columns
    eda_data[categorical_cols] = eda_data[categorical_cols].fillna(eda_data[categorical_cols].mode().iloc[0])

def show_eda_data():
    global eda_data
    if eda_data is not None:
        print("Modified EDA Data:")
        print(eda_data)
        print(eda_data.isnull().sum())
    else:
        print("No EDA data available.")

show_button = tk.Button(window, text="Show EDA Data", command=show_eda_data)
show_button.pack()

window.mainloop()
