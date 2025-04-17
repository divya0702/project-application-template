# gui/flexible_bucket_gui.py

import tkinter as tk
from tkinter import ttk, messagebox
from utils.data_extractors import extract_minutes_from_issues, bucket_values, UNIT_MAP
from utils.plot_utils import gui_bar_chart


class BucketRow:
    """
    A single row representing a time bucket for filtering issues by resolution time.
    Each row allows input of start and end values with corresponding time units.
    """

    def __init__(
        self,
        parent,
        app,
        row,
        start_val="",
        start_unit="days",
        end_val="",
        end_unit="days",
    ):
        self.app = app

        # Frame for a single bucket row
        self.frame = tk.Frame(parent, bg="#f7f7f7", pady=8)
        self.frame.grid(row=row, column=0, sticky="ew", padx=15, pady=5)

        entry_font = ("Segoe UI", 12)
        combo_font = ("Segoe UI", 12)

        # Entry for start value
        self.start_val = tk.Entry(self.frame, width=12, font=entry_font)
        self.start_val.grid(row=0, column=0, padx=6)
        self.start_val.insert(0, start_val)

        # Dropdown for start unit
        self.start_unit = ttk.Combobox(
            self.frame,
            values=["minutes", "hours", "days"],
            width=12,
            font=combo_font,
            state="readonly",
        )
        self.start_unit.grid(row=0, column=1, padx=6)
        self.start_unit.set(start_unit)

        # Entry for end value
        self.end_val = tk.Entry(self.frame, width=12, font=entry_font)
        self.end_val.grid(row=0, column=2, padx=6)
        self.end_val.insert(0, end_val)

        # Dropdown for end unit or "+" for open-ended
        self.end_unit = ttk.Combobox(
            self.frame,
            values=["minutes", "hours", "days", "+"],
            width=12,
            font=combo_font,
            state="readonly",
        )
        self.end_unit.grid(row=0, column=3, padx=6)
        self.end_unit.set(end_unit)

        # Delete button to remove this row
        self.del_button = tk.Button(
            self.frame,
            text="✖",
            command=self.delete,
            bg="#ff4d4d",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            width=4,
        )
        self.del_button.grid(row=0, column=4, padx=8)

    def delete(self):
        """
        Deletes the bucket row from UI and data list.
        """
        self.frame.destroy()
        self.app.bucket_rows.remove(self)
        self.app.update_plot()

    def get_range(self):
        """
        Extracts the start and end values (in minutes) from this row.
        Returns:
            tuple: (start_minutes, end_minutes), label
        """
        try:
            start = int(self.start_val.get())
            start_minutes = start * UNIT_MAP[self.start_unit.get().lower()]
            end_unit = self.end_unit.get().lower()

            # Handle open-ended bucket using "+" or blank end value
            if self.end_val.get().strip() == "" or end_unit == "+":
                end_minutes = float("inf")
                label = f"{start} {self.start_unit.get()}+"
            else:
                end = int(self.end_val.get())
                end_minutes = end * UNIT_MAP[end_unit]
                label = f"{start} {self.start_unit.get()} - {end} {end_unit}"

            return (start_minutes, end_minutes), label
        except:
            raise ValueError("Invalid entry in bucket")


class FlexibleXUnitApp:
    """
    A Tkinter GUI application for exploring issue resolution times using
    dynamic, user-defined time buckets.
    """

    def __init__(self, root, issues):
        self.root = root
        self.root.title("Resolution Time Vs Number of Issues")
        self.root.configure(bg="#eaeaea")

        # Extract resolution time from issues (in minutes)
        self.time_list = extract_minutes_from_issues(issues)
        self.bucket_rows = []

        # Header label
        tk.Label(
            root,
            text="Customize Time Buckets for Number of Issues",
            font=("Segoe UI", 16, "bold"),
            bg="#eaeaea",
        ).pack(pady=(14, 8))

        # Header labels for input columns
        header_frame = tk.Frame(root, bg="#eaeaea")
        header_frame.pack()
        for i, label in enumerate(["Start", "Unit", "End", "Unit / +", ""]):
            tk.Label(
                header_frame,
                text=label,
                font=("Segoe UI", 12, "bold"),
                bg="#eaeaea",
                padx=10,
            ).grid(row=0, column=i)

        # Frame to hold bucket rows
        self.bucket_frame = tk.Frame(root, bg="#eaeaea")
        self.bucket_frame.pack()

        # Initialize with default buckets
        self.add_bucket_row("0", "days", "20", "days")
        self.add_bucket_row("20", "days", "60", "days")
        self.add_bucket_row("60", "days", "", "+")

        # Controls to add new bucket or refresh graph
        control_frame = tk.Frame(root, bg="#eaeaea")
        control_frame.pack(pady=18)

        tk.Button(
            control_frame,
            text="Add Bucket",
            command=self.add_bucket_row,
            bg="#007acc",
            fg="white",
            font=("Segoe UI", 12),
            padx=20,
        ).pack(side=tk.LEFT, padx=12)

        tk.Button(
            control_frame,
            text="Update Graph",
            command=self.update_plot,
            bg="#28a745",
            fg="white",
            font=("Segoe UI", 12),
            padx=20,
        ).pack(side=tk.LEFT, padx=12)

        # Placeholder where the chart will be embedded
        self.chart_frame = tk.Frame(root, bg="#eaeaea")
        self.chart_frame.pack()
        self.fig = None
        self.ax = None
        self.canvas = None

        # Show chart initially
        self.update_plot()

    def add_bucket_row(
        self, start_val="", start_unit="minutes", end_val="", end_unit="minutes"
    ):
        """
        Adds a new BucketRow to the UI and updates internal state.
        """
        row = len(self.bucket_rows)
        new_row = BucketRow(
            self.bucket_frame, self, row, start_val, start_unit, end_val, end_unit
        )
        self.bucket_rows.append(new_row)

    def update_plot(self):
        """
        Redraws the bar chart based on current bucket values and issue data.
        """
        try:
            ranges, labels = [], []

            # Gather all ranges and labels from each bucket row
            for bucket in self.bucket_rows:
                rng, label = bucket.get_range()
                ranges.append(rng)
                labels.append(label)

            # Compute how many values fall into each range
            counts = bucket_values(self.time_list, ranges)

            # Remove old chart if present
            for widget in self.chart_frame.winfo_children():
                widget.destroy()

            # Render new chart
            self.fig, self.ax, self.canvas = gui_bar_chart(
                tk_root=self.chart_frame,
                labels=labels,
                counts=counts,
                xlabel="Resolution Time",
                ylabel="Number of Issues",
                title="Issues Solved by Time Range",
                color="#ff7f50",
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))
