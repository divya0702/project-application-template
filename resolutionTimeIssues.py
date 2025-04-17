# import json
# import matplotlib.pyplot as plt
# from collections import defaultdict
# import re

# # Load JSON data from 'closed_issues.json'
# with open("closed_issues.json", "r") as file:
#     issues = json.load(file)

# # Initialize counters for each time_to_close range
# time_range_count = {
#     "Less than 7 days": 0,
#     "8 to 60 days": 0,
#     "More than 60 days": 0
# }

# # Regular expression to extract days from 'time_to_close' field
# days_pattern = re.compile(r"(\d+)\s+days?")

# # Iterate through the issues to categorize them based on 'time_to_close'
# for issue in issues:
#     time_to_close = issue.get("time_to_close", "")
    
#     # Extract the number of days from the 'time_to_close' field
#     days_match = days_pattern.search(time_to_close)
#     if days_match:
#         days = int(days_match.group(1))
#     else:
#         days = 0  # Handle cases where 'time_to_close' is less than 1 day or does not have "days"

#     # Categorize based on the number of days
#     if days < 7:
#         time_range_count["Less than 7 days"] += 1
#     elif 8 <= days <= 60:
#         time_range_count["8 to 60 days"] += 1
#     elif days > 60:
#         time_range_count["More than 60 days"] += 1

# # Prepare data for the bar chart
# categories = list(time_range_count.keys())
# counts = list(time_range_count.values())

# # Create a bar plot
# plt.figure(figsize=(10, 6))
# plt.bar(categories, counts, color='lightcoral')

# # Add labels and title
# plt.xlabel("Resolution Time (in Days)")
# plt.ylabel("Number of Issues")
# plt.title("Number of Issues Based on Time to Close")

# # Display the graph
# plt.tight_layout()  # Adjust layout to prevent label cut-off
# plt.show()

import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox
import re
import math

# --- Unit multipliers ---
UNIT_MAP = {
    "minutes": 1,
    "minute": 1,
    "hours": 60,
    "hour": 60,
    "days": 1440,
    "day": 1440
}

# --- Load issues ---
with open("closed_issues.json", "r") as file:
    issues = json.load(file)

def parse_time_to_minutes(time_str):
    match = re.search(r"(\d+)\s*(minutes?|hours?|days?)", time_str)
    if match:
        value, unit = int(match.group(1)), match.group(2).lower()
        return value * UNIT_MAP.get(unit, 1)
    return 0

def extract_minutes_from_issues():
    return [parse_time_to_minutes(issue.get("time_to_close", "")) for issue in issues]

def bucket_values(values, ranges):
    counts = [0] * len(ranges)
    for v in values:
        for i, (start, end) in enumerate(ranges):
            if start <= v <= end:
                counts[i] += 1
                break
    return counts

class BucketRow:
    def __init__(self, parent, app, row, start_val="", start_unit="days", end_val="", end_unit="days"):
        self.app = app
        self.frame = tk.Frame(parent, bg="#f7f7f7", pady=8)
        self.frame.grid(row=row, column=0, sticky="ew", padx=15, pady=5)

        entry_font = ("Segoe UI", 12)
        combo_font = ("Segoe UI", 12)

        self.start_val = tk.Entry(self.frame, width=12, font=entry_font)
        self.start_val.grid(row=0, column=0, padx=6)
        self.start_val.insert(0, start_val)

        self.start_unit = ttk.Combobox(self.frame, values=["minutes", "hours", "days"], width=12, font=combo_font, state="readonly")
        self.start_unit.grid(row=0, column=1, padx=6)
        self.start_unit.set(start_unit)

        self.end_val = tk.Entry(self.frame, width=12, font=entry_font)
        self.end_val.grid(row=0, column=2, padx=6)
        self.end_val.insert(0, end_val)

        self.end_unit = ttk.Combobox(self.frame, values=["minutes", "hours", "days", "+"], width=12, font=combo_font, state="readonly")
        self.end_unit.grid(row=0, column=3, padx=6)
        self.end_unit.set(end_unit)

        self.del_button = tk.Button(self.frame, text="✖", command=self.delete, bg="#ff4d4d", fg="white", font=("Segoe UI", 11, "bold"), width=4)
        self.del_button.grid(row=0, column=4, padx=8)

    def delete(self):
        self.frame.destroy()
        self.app.bucket_rows.remove(self)
        self.app.update_plot()

    def get_range(self):
        try:
            start = int(self.start_val.get())
            start_unit = self.start_unit.get().lower()
            start_minutes = start * UNIT_MAP[start_unit]

            end_unit = self.end_unit.get().lower()
            if self.end_val.get().strip() == "" or end_unit == "+":
                end_minutes = float("inf")
                label = f"{start} {start_unit}+"
            else:
                end = int(self.end_val.get())
                end_minutes = end * UNIT_MAP[end_unit]
                label = f"{start} {start_unit} - {end} {end_unit}"

            return (start_minutes, end_minutes), label
        except:
            raise ValueError("Invalid entry in bucket")

class FlexibleXUnitApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🕒 Resolution Time Vs Number of Issues")
        self.root.configure(bg="#eaeaea")
        self.time_list = extract_minutes_from_issues()
        self.bucket_rows = []

        tk.Label(root, text="🧠 Customize Time Buckets for Number of Issues", font=("Segoe UI", 16, "bold"), bg="#eaeaea").pack(pady=(14, 8))

        header_frame = tk.Frame(root, bg="#eaeaea")
        header_frame.pack()
        for i, label in enumerate(["Start", "Unit", "End", "Unit / +", ""]):
            tk.Label(header_frame, text=label, font=("Segoe UI", 12, "bold"), bg="#eaeaea", padx=10).grid(row=0, column=i)

        self.bucket_frame = tk.Frame(root, bg="#eaeaea")
        self.bucket_frame.pack()

        # Default buckets
        self.add_bucket_row("0", "days", "20", "days")
        self.add_bucket_row("20", "days", "60", "days")
        self.add_bucket_row("60", "days", "", "+")

        control_frame = tk.Frame(root, bg="#eaeaea")
        control_frame.pack(pady=18)

        tk.Button(control_frame, text="➕ Add Bucket", command=self.add_bucket_row,
                  bg="#007acc", fg="white", font=("Segoe UI", 12), padx=20).pack(side=tk.LEFT, padx=12)

        tk.Button(control_frame, text="📊 Update Graph", command=self.update_plot,
                  bg="#28a745", fg="white", font=("Segoe UI", 12), padx=20).pack(side=tk.LEFT, padx=12)

        self.fig, self.ax = plt.subplots(figsize=(9.5, 5.2))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(padx=20, pady=15)

        self.update_plot()

    def add_bucket_row(self, start_val="", start_unit="minutes", end_val="", end_unit="minutes"):
        row = len(self.bucket_rows)
        new_row = BucketRow(self.bucket_frame, self, row, start_val, start_unit, end_val, end_unit)
        self.bucket_rows.append(new_row)

    def update_plot(self):
        try:
            ranges, labels = [], []

            for bucket in self.bucket_rows:
                rng, label = bucket.get_range()
                ranges.append(rng)
                labels.append(label)

            counts = bucket_values(self.time_list, ranges)
            self.plot_graph(labels, counts)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def plot_graph(self, labels, counts):
        self.ax.clear()
        pos = range(len(labels))

        # Calculate dynamic Y max
        max_count = max(counts) if counts else 0
        step = int(round(max_count * 0.1)) or 1
        y_max = math.ceil(max_count / step) * step + step

        self.ax.bar(pos, counts, color='#ff7f50')
        self.ax.set_xticks(pos)
        self.ax.set_xticklabels(labels, rotation=30, ha="right", fontsize=11)
        self.ax.set_ylim(0, y_max)
        self.ax.set_xlabel("⏳ Resolution Time", fontsize=13)
        self.ax.set_ylabel("📌 Number of Issues", fontsize=13)
        self.ax.set_title("📈 Issues Solved by Time Range", fontsize=15, weight="bold")
        self.fig.tight_layout()
        self.canvas.draw()

# Run app
root = tk.Tk()
app = FlexibleXUnitApp(root)
root.mainloop()


