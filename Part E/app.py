import oracledb
import tkinter as tk
from tkinter import ttk, messagebox

DB_USER = "system"
DB_PASS = "Password123"
DB_DSN = "127.0.0.1:1521/FREEPDB1"


class SmartGridApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Grid Energy Consumption Database")
        self.root.geometry("1280x760")
        self.root.minsize(1100, 680)
        self.root.configure(bg="#1e1e1e")

        self.conn = None
        self.setup_style()
        self.create_widgets()
        self.connect_db()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="#252526",
            foreground="white",
            fieldbackground="#252526",
            rowheight=32,
            bordercolor="#3c3c3c",
            borderwidth=0,
            font=("Arial", 11)
        )
        style.configure(
            "Treeview.Heading",
            background="#2d2d30",
            foreground="white",
            font=("Arial", 11, "bold"),
            relief="flat"
        )
        style.map("Treeview.Heading", background=[("active", "#3a3d41")])

        style.configure("TButton", font=("Arial", 11, "bold"), padding=8)

    def connect_db(self):
        try:
            self.conn = oracledb.connect(
                user=DB_USER,
                password=DB_PASS,
                dsn=DB_DSN
            )
            self.set_status("Connected to Oracle database.")
        except Exception as e:
            self.set_status("Database connection failed.")
            messagebox.showerror("Database Error", f"Could not connect to database:\n{e}")

    def create_widgets(self):
        outer = tk.Frame(self.root, bg="#1e1e1e", padx=20, pady=20)
        outer.pack(fill="both", expand=True)

        title = tk.Label(
            outer,
            text="Smart Grid Energy Consumption Database",
            bg="#1e1e1e",
            fg="white",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=(0, 10))

        subtitle = tk.Label(
            outer,
            text="Graphical User Interface for Smart Grid Features",
            bg="#1e1e1e",
            fg="#bdbdbd",
            font=("Arial", 11)
        )
        subtitle.pack(pady=(0, 18))

        top_panel = tk.Frame(outer, bg="#1e1e1e")
        top_panel.pack(fill="x", pady=(0, 18))

        left_buttons = tk.LabelFrame(
            top_panel,
            text="Features",
            bg="#252526",
            fg="white",
            font=("Arial", 12, "bold"),
            bd=1,
            relief="solid",
            padx=12,
            pady=12
        )
        left_buttons.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right_inputs = tk.LabelFrame(
            top_panel,
            text="Inputs",
            bg="#252526",
            fg="white",
            font=("Arial", 12, "bold"),
            bd=1,
            relief="solid",
            padx=12,
            pady=12
        )
        right_inputs.pack(side="left", fill="both", expand=True)

        self.make_button(left_buttons, "1. Households and Smart Meters", self.feature_1_households_and_meters, 0, 0)
        self.make_button(left_buttons, "2. Meter Readings by Date Range", self.feature_2_meter_readings_by_date, 0, 1)
        self.make_button(left_buttons, "3. Rate Plan for Household", self.feature_3_rate_plan_for_household, 1, 0)
        self.make_button(left_buttons, "4. Average Usage for Household", self.feature_4_average_usage_for_household, 1, 1)
        self.make_button(left_buttons, "5. Meter Location for Household", self.feature_5_meter_location_for_household, 2, 0)
        self.make_button(left_buttons, "Clear Results", self.clear_results, 2, 1)

        for i in range(2):
            left_buttons.grid_columnconfigure(i, weight=1)

        self.make_label(right_inputs, "Household ID", 0, 0)
        self.household_id_entry = self.make_entry(right_inputs, 0, 1)

        self.make_label(right_inputs, "Meter ID", 1, 0)
        self.meter_id_entry = self.make_entry(right_inputs, 1, 1)

        self.make_label(right_inputs, "Start Date/Time", 2, 0)
        self.start_date_entry = self.make_entry(right_inputs, 2, 1)
        self.start_date_entry.insert(0, "2006-01-01 00:00:00")

        self.make_label(right_inputs, "End Date/Time", 3, 0)
        self.end_date_entry = self.make_entry(right_inputs, 3, 1)
        self.end_date_entry.insert(0, "2011-01-01 00:00:00")

        hint = tk.Label(
            right_inputs,
            text="Example: Household ID = 1, Meter ID = 1",
            bg="#252526",
            fg="#bdbdbd",
            font=("Arial", 10)
        )
        hint.grid(row=4, column=0, columnspan=2, sticky="w", pady=(12, 0))

        results_frame = tk.LabelFrame(
            outer,
            text="Results",
            bg="#252526",
            fg="white",
            font=("Arial", 12, "bold"),
            bd=1,
            relief="solid",
            padx=10,
            pady=10
        )
        results_frame.pack(fill="both", expand=True)

        tree_container = tk.Frame(results_frame, bg="#252526")
        tree_container.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(tree_container, show="headings")
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar_y = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        scrollbar_y.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar_y.set)

        scrollbar_x = ttk.Scrollbar(results_frame, orient="horizontal", command=self.tree.xview)
        scrollbar_x.pack(fill="x", pady=(8, 0))
        self.tree.configure(xscrollcommand=scrollbar_x.set)

        self.status_label = tk.Label(
            outer,
            text="Ready",
            anchor="w",
            bg="#2d2d30",
            fg="#d4d4d4",
            font=("Arial", 10),
            padx=10,
            pady=8
        )
        self.status_label.pack(fill="x", pady=(12, 0))

    def make_button(self, parent, text, command, row, col):
        btn = ttk.Button(
            parent,
            text=text,
            command=command
        )
        btn.grid(row=row, column=col, sticky="ew", padx=6, pady=6, ipady=8)

    def make_label(self, parent, text, row, col):
        lbl = tk.Label(
            parent,
            text=text,
            bg="#252526",
            fg="white",
            font=("Arial", 11, "bold")
        )
        lbl.grid(row=row, column=col, sticky="w", padx=(0, 10), pady=8)

    def make_entry(self, parent, row, col):
        entry = tk.Entry(
            parent,
            bg="#1e1e1e",
            fg="white",
            insertbackground="white",
            font=("Arial", 11),
            relief="solid",
            bd=1,
            width=28
        )
        entry.grid(row=row, column=col, sticky="ew", pady=8)
        parent.grid_columnconfigure(col, weight=1)
        return entry

    def set_status(self, text):
        self.status_label.config(text=text)

    def clear_results(self):
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = ()
        self.set_status("Results cleared.")

    def display_results(self, cursor, rows):
        self.clear_results()

        if not rows:
            self.set_status("No results found.")
            messagebox.showinfo("No Results", "No results found.")
            return

        columns = [col[0] for col in cursor.description]
        self.tree["columns"] = columns

        for col in columns:
            self.tree.heading(col, text=col.replace("_", " "))
            self.tree.column(col, width=170, minwidth=120, anchor="center")

        for row in rows:
            cleaned = ["" if value is None else str(value) for value in row]
            self.tree.insert("", "end", values=cleaned)

        self.set_status(f"Loaded {len(rows)} row(s).")

    def run_query(self, query, params=None):
        if self.conn is None:
            messagebox.showerror("Database Error", "No database connection.")
            self.set_status("No database connection.")
            return

        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            rows = cursor.fetchall()
            self.display_results(cursor, rows)
            cursor.close()
        except Exception as e:
            self.set_status("Query failed.")
            messagebox.showerror("Query Error", str(e))

    def feature_1_households_and_meters(self):
        query = """
        SELECT h.id AS household_id,
               h.address,
               h.city,
               sm.id AS meter_id,
               sm.serial_number,
               sm.manufacturer
        FROM households h
        JOIN smart_meters sm
          ON h.id = sm.household_id
        ORDER BY h.id, sm.id
        """
        self.run_query(query)

    def feature_2_meter_readings_by_date(self):
        meter_id = self.meter_id_entry.get().strip()
        start_date = self.start_date_entry.get().strip()
        end_date = self.end_date_entry.get().strip()

        if not meter_id:
            messagebox.showwarning("Input Error", "Please enter a Meter ID.")
            return

        query = """
        SELECT meter_id,
               reading_timestamp,
               global_active_power,
               global_reactive_power,
               voltage,
               global_intensity
        FROM energy_readings
        WHERE meter_id = :meter_id
          AND reading_timestamp BETWEEN
              TO_TIMESTAMP(:start_date, 'YYYY-MM-DD HH24:MI:SS')
              AND TO_TIMESTAMP(:end_date, 'YYYY-MM-DD HH24:MI:SS')
        ORDER BY reading_timestamp
        """
        self.run_query(query, {
            "meter_id": int(meter_id),
            "start_date": start_date,
            "end_date": end_date
        })

    def feature_3_rate_plan_for_household(self):
        household_id = self.household_id_entry.get().strip()

        if not household_id:
            messagebox.showwarning("Input Error", "Please enter a Household ID.")
            return

        query = """
        SELECT h.id AS household_id,
               h.address,
               rp.id AS rate_plan_id,
               rp.plan_name,
               rp.base_rate_per_kwh,
               rp.peak_rate_per_kwh,
               hrp.start_date,
               hrp.end_date
        FROM households h
        JOIN household_to_rate_plans hrp
          ON h.id = hrp.household_id
        JOIN rate_plans rp
          ON hrp.rate_plan_id = rp.id
        WHERE h.id = :household_id
        ORDER BY hrp.start_date DESC
        """
        self.run_query(query, {"household_id": int(household_id)})

    def feature_4_average_usage_for_household(self):
        household_id = self.household_id_entry.get().strip()

        if not household_id:
            messagebox.showwarning("Input Error", "Please enter a Household ID.")
            return

        query = """
        SELECT h.id AS household_id,
               h.address,
               AVG(er.global_active_power) AS avg_active_power,
               AVG(er.voltage) AS avg_voltage,
               AVG(er.global_intensity) AS avg_intensity
        FROM households h
        JOIN smart_meters sm
          ON h.id = sm.household_id
        JOIN energy_readings er
          ON sm.id = er.meter_id
        WHERE h.id = :household_id
        GROUP BY h.id, h.address
        """
        self.run_query(query, {"household_id": int(household_id)})

    def feature_5_meter_location_for_household(self):
        household_id = self.household_id_entry.get().strip()

        if not household_id:
            messagebox.showwarning("Input Error", "Please enter a Household ID.")
            return

        query = """
        SELECT h.id AS household_id,
               h.address,
               sm.id AS meter_id,
               ml.latitude,
               ml.longitude,
               ml.last_verified_date
        FROM households h
        JOIN smart_meters sm
          ON h.id = sm.household_id
        JOIN meter_locations ml
          ON sm.id = ml.meter_id
        WHERE h.id = :household_id
        ORDER BY sm.id
        """
        self.run_query(query, {"household_id": int(household_id)})


if __name__ == "__main__":
    root = tk.Tk()
    app = SmartGridApp(root)
    root.mainloop()
