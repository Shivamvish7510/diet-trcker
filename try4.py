import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from mysql.connector import Error

# Color scheme
BG_COLOR = "#FFFFFE"
HEADER_COLOR = "#2c3e50"
BUTTON_COLOR = "#4796BD"
BUTTON_HOVER = "#2980b9"
ACCENT_COLOR = "#e74c3c"
LIGHT_TEXT = "#ecf0f1"
DARK_TEXT = "#2c3e50"
CARD_COLOR = "#ffffff"

def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Shivam@123",
            database="DietTracker3"
        )
        return conn
    except Error as e:
        messagebox.showerror("Error", f"Failed to connect to the database: {e}")
        return None

class Admin:
    def __init__(self, root):
        self.root = root
        self.root.title("Diet Tracker - Admin Panel")
        self.root.geometry("1000x700")
        self.root.minsize(900, 600)
        root.wm_iconbitmap("food.ico")
        self.root.config(bg=BG_COLOR)
        
        # Custom styling
        self.setup_styles()
        self.create_admin_dashboard()

    def setup_styles(self):
        style = ttk.Style()
        
        # Configure the Treeview colors
        style.configure("Treeview",
                        background=CARD_COLOR,
                        foreground=DARK_TEXT,
                        rowheight=25,
                        fieldbackground=CARD_COLOR,
                        font=('Arial', 10))
        
        style.map('Treeview', background=[('selected', BUTTON_COLOR)])
        
        # Treeview heading style
        style.configure("Treeview.Heading",
                        background=HEADER_COLOR,
                        foreground=LIGHT_TEXT,
                        font=('Arial', 10, 'bold'))
        
        # Button style
        style.configure("TButton",
                       font=('Arial', 10),
                       background=BUTTON_COLOR,
                       foreground=LIGHT_TEXT,
                       borderwidth=1)
        
        style.map("TButton",
                 background=[('active', BUTTON_HOVER), ('pressed', BUTTON_HOVER)])
        
        # Entry style
        style.configure("TEntry",
                       font=('Arial', 10),
                       fieldbackground=CARD_COLOR)
        
        # Label style
        style.configure("TLabel",
                       font=('Arial', 10),
                       background=BG_COLOR,
                       foreground=DARK_TEXT)
        
        style.configure("Header.TLabel",
                       font=('Arial', 14, 'bold'),
                       background=HEADER_COLOR,
                       foreground=LIGHT_TEXT)
        
        style.configure("Card.TLabel",
                       font=('Arial', 12, 'bold'),
                       background=CARD_COLOR,
                       foreground=DARK_TEXT)
        
        style.configure("Stat.TLabel",
                       font=('Arial', 24, 'bold'),
                       background=CARD_COLOR,
                       foreground=BUTTON_COLOR)

    def create_admin_dashboard(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Header
        self.header = tk.Frame(self.root, bg=HEADER_COLOR, height=70)
        self.header.pack(fill="x", padx=0, pady=0)
        
        tk.Label(self.header, 
                text="Admin Dashboard", 
                font=("Arial", 18, "bold"),
                bg=HEADER_COLOR,
                fg=LIGHT_TEXT).pack(side="left", padx=20, pady=15)
        
        # Logout button
        logout_btn = ttk.Button(self.header, 
                              text="Log Out",
                              style="TButton",
                              command=self.logout)
        logout_btn.pack(side="right", padx=20, pady=10)

        # Main container
        self.main_container = tk.Frame(self.root, bg=BG_COLOR)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Sidebar
        self.sidebar = tk.Frame(self.main_container, 
                               bg=HEADER_COLOR, 
                               width=200,
                               relief="raised",
                               bd=1)
        self.sidebar.pack(side="left", fill="y", padx=(0, 10), pady=0)
        
        # Navigation buttons
        nav_buttons = [
            ("Dashboard", self.create_admin_dashboard),
            ("Users", self.display_all_users),
            ("Food Items", self.display_all_foods),
            ("Add New Food", self.add_new_food),
            ("Add New User", self.add_new_user),
            ("Update User", self.update_user),
            ("Delete User", self.delete_user)
        ]
        
        for text, command in nav_buttons:
            btn = ttk.Button(self.sidebar,
                            text=text,
                            style="TButton",
                            command=command)
            btn.pack(fill="x", padx=5, pady=5)

        # Content area
        self.content = tk.Frame(self.main_container, 
                               bg=BG_COLOR,
                               relief="flat")
        self.content.pack(side="right", fill="both", expand=True)
        
        # Dashboard content
        self.create_dashboard_content()

    def create_dashboard_content(self):
        # Clear content area
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Title
        title_frame = tk.Frame(self.content, bg=BG_COLOR)
        title_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Label(title_frame, 
                 text="Dashboard Overview", 
                 style="Header.TLabel").pack(side="left", anchor="w")
        
        # Stats cards
        stats_frame = tk.Frame(self.content, bg=BG_COLOR)
        stats_frame.pack(fill="x", pady=(0, 20))
        
        # Total Users card
        user_card = tk.Frame(stats_frame, bg=CARD_COLOR, relief="raised", bd=1)
        user_card.pack(side="left", fill="both", expand=True, padx=5)
        
        ttk.Label(user_card, 
                 text="Total Users", 
                 style="Card.TLabel").pack(pady=(10, 0))
        
        self.user_count_label = ttk.Label(user_card, 
                                        text="0", 
                                        style="Stat.TLabel")
        self.user_count_label.pack(pady=(0, 10))
        
        # Total Foods card
        food_card = tk.Frame(stats_frame, bg=CARD_COLOR, relief="raised", bd=1)
        food_card.pack(side="left", fill="both", expand=True, padx=5)
        
        ttk.Label(food_card, 
                 text="Total Food Items", 
                 style="Card.TLabel").pack(pady=(10, 0))
        
        self.food_count_label = ttk.Label(food_card, 
                                         text="0", 
                                         style="Stat.TLabel")
        self.food_count_label.pack(pady=(0, 10))
        
        # Recent activity frame
        activity_frame = tk.Frame(self.content, bg=BG_COLOR)
        activity_frame.pack(fill="both", expand=True)
        
        ttk.Label(activity_frame, 
                 text="Recent Activity", 
                 style="Header.TLabel").pack(anchor="w", pady=(0, 10))
        
        # Activity table
        self.activity_table = ttk.Treeview(activity_frame, 
                                         columns=("Type", "Details", "Time"),
                                         show="headings",
                                         height=8)
        
        self.activity_table.heading("Type", text="Type")
        self.activity_table.heading("Details", text="Details")
        self.activity_table.heading("Time", text="Time")
        
        self.activity_table.column("Type", width=100, anchor="w")
        self.activity_table.column("Details", width=300, anchor="w")
        self.activity_table.column("Time", width=150, anchor="w")
        
        self.activity_table.pack(fill="both", expand=True)
        
        # Add sample activity (in a real app, this would come from the database)
        sample_activity = [
            ("User", "John Doe was added", "2023-05-15 10:30"),
            ("Food", "Apple was added", "2023-05-15 09:45"),
            ("User", "Jane Smith updated", "2023-05-14 16:20"),
            ("Food", "Banana was deleted", "2023-05-14 14:10")
        ]
        
        for activity in sample_activity:
            self.activity_table.insert("", "end", values=activity)
        
        # Update stats
        self.update_dashboard_stats()

    def update_dashboard_stats(self):
        # Get total users
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            total_users = cursor.fetchone()[0]
            self.user_count_label.config(text=str(total_users))
            
            # Get total foods
            cursor.execute("SELECT COUNT(*) FROM foods")
            total_foods = cursor.fetchone()[0]
            self.food_count_label.config(text=str(total_foods))
            
            cursor.close()
            conn.close()

    def display_all_users(self):
        # Clear content area
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Title
        title_frame = tk.Frame(self.content, bg=BG_COLOR)
        title_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Label(title_frame, 
                 text="User Management", 
                 style="Header.TLabel").pack(side="left", anchor="w")
        
        # Action buttons
        btn_frame = tk.Frame(title_frame, bg=BG_COLOR)
        btn_frame.pack(side="right")
        
        refresh_btn = ttk.Button(btn_frame, 
                               text="Refresh",
                               style="TButton",
                               command=self.display_all_users)
        refresh_btn.pack(side="left", padx=5)
        
        add_btn = ttk.Button(btn_frame, 
                            text="Add User",
                            style="TButton",
                            command=self.add_new_user)
        add_btn.pack(side="left", padx=5)
        
        # User table frame
        table_frame = tk.Frame(self.content, bg=BG_COLOR)
        table_frame.pack(fill="both", expand=True)
        
        # Scrollbars
        y_scroll = ttk.Scrollbar(table_frame)
        y_scroll.pack(side="right", fill="y")
        
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")
        
        # User table
        self.user_table = ttk.Treeview(table_frame,
                                     columns=("ID", "Name", "Email", "Role", "Calorie Goal"),
                                     yscrollcommand=y_scroll.set,
                                     xscrollcommand=x_scroll.set,
                                     selectmode="extended")
        
        self.user_table.heading("#0", text="", anchor="w")
        self.user_table.heading("ID", text="ID", anchor="w")
        self.user_table.heading("Name", text="Name", anchor="w")
        self.user_table.heading("Email", text="Email", anchor="w")
        self.user_table.heading("Role", text="Role", anchor="w")
        self.user_table.heading("Calorie Goal", text="Calorie Goal", anchor="w")
        
        self.user_table.column("#0", width=0, stretch=tk.NO)
        self.user_table.column("ID", width=50, minwidth=50)
        self.user_table.column("Name", width=150, minwidth=100)
        self.user_table.column("Email", width=200, minwidth=150)
        self.user_table.column("Role", width=100, minwidth=80)
        self.user_table.column("Calorie Goal", width=100, minwidth=80)
        
        self.user_table.pack(fill="both", expand=True)
        
        # Configure scrollbars
        y_scroll.config(command=self.user_table.yview)
        x_scroll.config(command=self.user_table.xview)
        
        # Load user data
        self.load_user_data()
        
        # Action buttons at bottom
        action_frame = tk.Frame(self.content, bg=BG_COLOR)
        action_frame.pack(fill="x", pady=(10, 0))
        
        update_btn = ttk.Button(action_frame, 
                              text="Update Selected",
                              style="TButton",
                              command=self.update_selected_user)
        update_btn.pack(side="left", padx=5)
        
        delete_btn = ttk.Button(action_frame, 
                              text="Delete Selected",
                              style="TButton",
                              command=self.delete_selected_user)
        delete_btn.pack(side="left", padx=5)

    def load_user_data(self):
        # Clear existing data
        for item in self.user_table.get_children():
            self.user_table.delete(item)
        
        # Fetch data from database
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, name, email, role, daily_calorie_goal FROM users")
            users = cursor.fetchall()
            
            for user in users:
                self.user_table.insert("", "end", values=user)
            
            cursor.close()
            conn.close()

    def update_selected_user(self):
        selected = self.user_table.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a user to update")
            return
        
        # Get selected user data
        user_data = self.user_table.item(selected[0], "values")
        
        # Open update form with user data
        self.update_user_form(user_data)

    def delete_selected_user(self):
        selected = self.user_table.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a user to delete")
            return
        
        user_id = self.user_table.item(selected[0], "values")[0]
        user_name = self.user_table.item(selected[0], "values")[1]
        
        confirm = messagebox.askyesno("Confirm Delete", 
                                    f"Are you sure you want to delete user {user_name} (ID: {user_id})?")
        
        if confirm:
            conn = connect_to_database()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
                    conn.commit()
                    messagebox.showinfo("Success", "User deleted successfully")
                    self.load_user_data()  # Refresh the table
                except Error as e:
                    messagebox.showerror("Error", f"Failed to delete user: {e}")
                finally:
                    cursor.close()
                    conn.close()

    def update_user_form(self, user_data):
        # Clear content area
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Title
        title_frame = tk.Frame(self.content, bg=BG_COLOR)
        title_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Label(title_frame, 
                 text=f"Update User: {user_data[1]} (ID: {user_data[0]})", 
                 style="Header.TLabel").pack(side="left", anchor="w")
        
        # Back button
        back_btn = ttk.Button(title_frame, 
                            text="Back to Users",
                            style="TButton",
                            command=self.display_all_users)
        back_btn.pack(side="right")
        
        # Form frame
        form_frame = tk.Frame(self.content, bg=BG_COLOR)
        form_frame.pack(fill="both", expand=True, pady=20)
        
        # Form fields
        fields = [
            ("Name:", "name", user_data[1]),
            ("Email:", "email", user_data[2]),
            ("Password:", "password", "", True),  # Password field (masked)
            ("Daily Calorie Goal:", "calorie_goal", user_data[4]),
            ("Role:", "role", user_data[3])
        ]
        
        self.entry_vars = {}
        
        for i, (label_text, field_name, default_value, *options) in enumerate(fields):
            row_frame = tk.Frame(form_frame, bg=BG_COLOR)
            row_frame.pack(fill="x", pady=5)
            
            ttk.Label(row_frame, 
                     text=label_text,
                     style="TLabel").pack(side="left", padx=(0, 10))
            
            if options and options[0]:  # Password field
                entry = ttk.Entry(row_frame, 
                                show="*",
                                style="TEntry")
            else:
                entry = ttk.Entry(row_frame,
                                style="TEntry")
                
            entry.insert(0, default_value)
            entry.pack(side="right", fill="x", expand=True)
            
            self.entry_vars[field_name] = entry
        
        # Submit button
        submit_btn = ttk.Button(form_frame,
                               text="Update User",
                               style="TButton",
                               command=lambda: self.submit_user_update(user_data[0]))
        submit_btn.pack(pady=20)

    def submit_user_update(self, user_id):
        # Get form data
        name = self.entry_vars["name"].get()
        email = self.entry_vars["email"].get()
        password = self.entry_vars["password"].get()
        calorie_goal = self.entry_vars["calorie_goal"].get()
        role = self.entry_vars["role"].get()
        
        # Validate
        if not all([name, email, calorie_goal, role]):
            messagebox.showwarning("Warning", "Please fill all required fields")
            return
        
        # Update database
        conn = connect_to_database()
        if conn:
            try:
                cursor = conn.cursor()
                
                if password:  # Only update password if it was changed
                    query = """UPDATE users SET 
                             name = %s, email = %s, password = %s, 
                             daily_calorie_goal = %s, role = %s 
                             WHERE user_id = %s"""
                    cursor.execute(query, (name, email, password, calorie_goal, role, user_id))
                else:
                    query = """UPDATE users SET 
                             name = %s, email = %s, 
                             daily_calorie_goal = %s, role = %s 
                             WHERE user_id = %s"""
                    cursor.execute(query, (name, email, calorie_goal, role, user_id))
                
                conn.commit()
                messagebox.showinfo("Success", "User updated successfully")
                self.display_all_users()  # Return to user list
            except Error as e:
                messagebox.showerror("Error", f"Failed to update user: {e}")
            finally:
                cursor.close()
                conn.close()

    def display_all_foods(self):
        # Clear content area
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Title
        title_frame = tk.Frame(self.content, bg=BG_COLOR)
        title_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Label(title_frame, 
                 text="Food Management", 
                 style="Header.TLabel").pack(side="left", anchor="w")
        
        # Action buttons
        btn_frame = tk.Frame(title_frame, bg=BG_COLOR)
        btn_frame.pack(side="right")
        
        refresh_btn = ttk.Button(btn_frame, 
                               text="Refresh",
                               style="TButton",
                               command=self.display_all_foods)
        refresh_btn.pack(side="left", padx=5)
        
        add_btn = ttk.Button(btn_frame, 
                            text="Add Food",
                            style="TButton",
                            command=self.add_new_food)
        add_btn.pack(side="left", padx=5)
        
        # Food table frame
        table_frame = tk.Frame(self.content, bg=BG_COLOR)
        table_frame.pack(fill="both", expand=True)
        
        # Scrollbars
        y_scroll = ttk.Scrollbar(table_frame)
        y_scroll.pack(side="right", fill="y")
        
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")
        
        # Food table
        self.food_table = ttk.Treeview(table_frame,
                                     columns=("ID", "Name", "Calories", "Protein", "Fat", "Carbs"),
                                     yscrollcommand=y_scroll.set,
                                     xscrollcommand=x_scroll.set,
                                     selectmode="extended")
        
        self.food_table.heading("#0", text="", anchor="w")
        self.food_table.heading("ID", text="ID", anchor="w")
        self.food_table.heading("Name", text="Name", anchor="w")
        self.food_table.heading("Calories", text="Calories", anchor="w")
        self.food_table.heading("Protein", text="Protein", anchor="w")
        self.food_table.heading("Fat", text="Fat", anchor="w")
        self.food_table.heading("Carbs", text="Carbs", anchor="w")
        
        self.food_table.column("#0", width=0, stretch=tk.NO)
        self.food_table.column("ID", width=50, minwidth=50)
        self.food_table.column("Name", width=150, minwidth=100)
        self.food_table.column("Calories", width=80, minwidth=80)
        self.food_table.column("Protein", width=80, minwidth=80)
        self.food_table.column("Fat", width=80, minwidth=80)
        self.food_table.column("Carbs", width=80, minwidth=80)
        
        self.food_table.pack(fill="both", expand=True)
        
        # Configure scrollbars
        y_scroll.config(command=self.food_table.yview)
        x_scroll.config(command=self.food_table.xview)
        
        # Load food data
        self.load_food_data()
        
        # Action buttons at bottom
        action_frame = tk.Frame(self.content, bg=BG_COLOR)
        action_frame.pack(fill="x", pady=(10, 0))
        
        update_btn = ttk.Button(action_frame, 
                              text="Update Selected",
                              style="TButton",
                              command=self.update_selected_food)
        update_btn.pack(side="left", padx=5)
        
        delete_btn = ttk.Button(action_frame, 
                              text="Delete Selected",
                              style="TButton",
                              command=self.delete_selected_food)
        delete_btn.pack(side="left", padx=5)

    def load_food_data(self):
        # Clear existing data
        for item in self.food_table.get_children():
            self.food_table.delete(item)
        
        # Fetch data from database
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT food_id, name, calories_per_100g, protein_per_100g, fat_per_100g, carbs_per_100g FROM foods")
            foods = cursor.fetchall()
            
            for food in foods:
                self.food_table.insert("", "end", values=food)
            
            cursor.close()
            conn.close()

    def update_selected_food(self):
        selected = self.food_table.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a food item to update")
            return
        
        # Get selected food data
        food_data = self.food_table.item(selected[0], "values")
        
        # Open update form with food data
        self.update_food_form(food_data)

    def delete_selected_food(self):
        selected = self.food_table.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a food item to delete")
            return
        
        food_id = self.food_table.item(selected[0], "values")[0]
        food_name = self.food_table.item(selected[0], "values")[1]
        
        confirm = messagebox.askyesno("Confirm Delete", 
                                    f"Are you sure you want to delete {food_name} (ID: {food_id})?")
        
        if confirm:
            conn = connect_to_database()
            if conn:
                try:
                    cursor = conn.cursor()
                    # First delete from food_log
                    cursor.execute("DELETE FROM food_log WHERE food_id = %s", (food_id,))
                    # Then delete from foods
                    cursor.execute("DELETE FROM foods WHERE food_id = %s", (food_id,))
                    conn.commit()
                    messagebox.showinfo("Success", "Food item deleted successfully")
                    self.load_food_data()  # Refresh the table
                except Error as e:
                    messagebox.showerror("Error", f"Failed to delete food item: {e}")
                finally:
                    cursor.close()
                    conn.close()

    def update_food_form(self, food_data):
        # Clear content area
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Title
        title_frame = tk.Frame(self.content, bg=BG_COLOR)
        title_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Label(title_frame, 
                 text=f"Update Food: {food_data[1]} (ID: {food_data[0]})", 
                 style="Header.TLabel").pack(side="left", anchor="w")
        
        # Back button
        back_btn = ttk.Button(title_frame, 
                            text="Back to Foods",
                            style="TButton",
                            command=self.display_all_foods)
        back_btn.pack(side="right")
        
        # Form frame
        form_frame = tk.Frame(self.content, bg=BG_COLOR)
        form_frame.pack(fill="both", expand=True, pady=20)
        
        # Form fields
        fields = [
            ("Name:", "name", food_data[1]),
            ("Calories (per 100g):", "calories", food_data[2]),
            ("Protein (per 100g):", "protein", food_data[3]),
            ("Fat (per 100g):", "fat", food_data[4]),
            ("Carbs (per 100g):", "carbs", food_data[5])
        ]
        
        self.food_entry_vars = {}
        
        for i, (label_text, field_name, default_value) in enumerate(fields):
            row_frame = tk.Frame(form_frame, bg=BG_COLOR)
            row_frame.pack(fill="x", pady=5)
            
            ttk.Label(row_frame, 
                     text=label_text,
                     style="TLabel").pack(side="left", padx=(0, 10))
            
            entry = ttk.Entry(row_frame,
                            style="TEntry")
            entry.insert(0, default_value)
            entry.pack(side="right", fill="x", expand=True)
            
            self.food_entry_vars[field_name] = entry
        
        # Submit button
        submit_btn = ttk.Button(form_frame,
                               text="Update Food",
                               style="TButton",
                               command=lambda: self.submit_food_update(food_data[0]))
        submit_btn.pack(pady=20)

    def submit_food_update(self, food_id):
        # Get form data
        name = self.food_entry_vars["name"].get()
        calories = self.food_entry_vars["calories"].get()
        protein = self.food_entry_vars["protein"].get()
        fat = self.food_entry_vars["fat"].get()
        carbs = self.food_entry_vars["carbs"].get()
        
        # Validate
        if not all([name, calories, protein, fat, carbs]):
            messagebox.showwarning("Warning", "Please fill all required fields")
            return
        
        # Update database
        conn = connect_to_database()
        if conn:
            try:
                cursor = conn.cursor()
                
                query = """UPDATE foods SET 
                         name = %s, calories_per_100g = %s, 
                         protein_per_100g = %s, fat_per_100g = %s, 
                         carbs_per_100g = %s 
                         WHERE food_id = %s"""
                cursor.execute(query, (name, calories, protein, fat, carbs, food_id))
                
                conn.commit()
                messagebox.showinfo("Success", "Food item updated successfully")
                self.display_all_foods()  # Return to food list
            except Error as e:
                messagebox.showerror("Error", f"Failed to update food item: {e}")
            finally:
                cursor.close()
                conn.close()

    def add_new_user(self):
        # Clear content area
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Title
        title_frame = tk.Frame(self.content, bg=BG_COLOR)
        title_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Label(title_frame, 
                 text="Add New User", 
                 style="Header.TLabel").pack(side="left", anchor="w")
        
        # Back button
        back_btn = ttk.Button(title_frame, 
                            text="Back to Users",
                            style="TButton",
                            command=self.display_all_users)
        back_btn.pack(side="right")
        
        # Form frame
        form_frame = tk.Frame(self.content, bg=BG_COLOR)
        form_frame.pack(fill="both", expand=True, pady=20)
        
        # Form fields
        fields = [
            ("Name:", "name", ""),
            ("Email:", "email", ""),
            ("Password:", "password", "", True),  # Password field (masked)
            ("Daily Calorie Goal:", "calorie_goal", "2000"),
            ("Role:", "role", "user")  # Default role
        ]
        
        self.new_user_entry_vars = {}
        
        for i, (label_text, field_name, default_value, *options) in enumerate(fields):
            row_frame = tk.Frame(form_frame, bg=BG_COLOR)
            row_frame.pack(fill="x", pady=5)
            
            ttk.Label(row_frame, 
                     text=label_text,
                     style="TLabel").pack(side="left", padx=(0, 10))
            
            if options and options[0]:  # Password field
                entry = ttk.Entry(row_frame, 
                                show="*",
                                style="TEntry")
            else:
                entry = ttk.Entry(row_frame,
                                style="TEntry")
                
            entry.insert(0, default_value)
            entry.pack(side="right", fill="x", expand=True)
            
            self.new_user_entry_vars[field_name] = entry
        
        # Submit button
        submit_btn = ttk.Button(form_frame,
                               text="Add User",
                               style="TButton",
                               command=self.submit_new_user)
        submit_btn.pack(pady=20)

    def submit_new_user(self):
        # Get form data
        name = self.new_user_entry_vars["name"].get()
        email = self.new_user_entry_vars["email"].get()
        password = self.new_user_entry_vars["password"].get()
        calorie_goal = self.new_user_entry_vars["calorie_goal"].get()
        role = self.new_user_entry_vars["role"].get()
        
        # Validate
        if not all([name, email, password, calorie_goal, role]):
            messagebox.showwarning("Warning", "Please fill all required fields")
            return
        
        # Add to database
        conn = connect_to_database()
        if conn:
            try:
                cursor = conn.cursor()
                
                query = """INSERT INTO users 
                         (name, email, password, daily_calorie_goal, role) 
                         VALUES (%s, %s, %s, %s, %s)"""
                cursor.execute(query, (name, email, password, calorie_goal, role))
                
                conn.commit()
                messagebox.showinfo("Success", "User added successfully")
                self.display_all_users()  # Return to user list
            except Error as e:
                messagebox.showerror("Error", f"Failed to add user: {e}")
            finally:
                cursor.close()
                conn.close()

    def add_new_food(self):
        # Clear content area
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Title
        title_frame = tk.Frame(self.content, bg=BG_COLOR)
        title_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Label(title_frame, 
                 text="Add New Food", 
                 style="Header.TLabel").pack(side="left", anchor="w")
        
        # Back button
        back_btn = ttk.Button(title_frame, 
                            text="Back to Foods",
                            style="TButton",
                            command=self.display_all_foods)
        back_btn.pack(side="right")
        
        # Form frame
        form_frame = tk.Frame(self.content, bg=BG_COLOR)
        form_frame.pack(fill="both", expand=True, pady=20)
        
        # Form fields
        fields = [
            ("Name:", "name", ""),
            ("Calories (per 100g):", "calories", ""),
            ("Protein (per 100g):", "protein", ""),
            ("Fat (per 100g):", "fat", ""),
            ("Carbs (per 100g):", "carbs", "")
        ]
        
        self.new_food_entry_vars = {}
        
        for i, (label_text, field_name, default_value) in enumerate(fields):
            row_frame = tk.Frame(form_frame, bg=BG_COLOR)
            row_frame.pack(fill="x", pady=5)
            
            ttk.Label(row_frame, 
                     text=label_text,
                     style="TLabel").pack(side="left", padx=(0, 10))
            
            entry = ttk.Entry(row_frame,
                            style="TEntry")
            entry.insert(0, default_value)
            entry.pack(side="right", fill="x", expand=True)
            
            self.new_food_entry_vars[field_name] = entry
        
        # Submit button
        submit_btn = ttk.Button(form_frame,
                               text="Add Food",
                               style="TButton",
                               command=self.submit_new_food)
        submit_btn.pack(pady=20)

    def submit_new_food(self):
        # Get form data
        name = self.new_food_entry_vars["name"].get()
        calories = self.new_food_entry_vars["calories"].get()
        protein = self.new_food_entry_vars["protein"].get()
        fat = self.new_food_entry_vars["fat"].get()
        carbs = self.new_food_entry_vars["carbs"].get()
        
        # Validate
        if not all([name, calories, protein, fat, carbs]):
            messagebox.showwarning("Warning", "Please fill all required fields")
            return
        
        # Add to database
        conn = connect_to_database()
        if conn:
            try:
                cursor = conn.cursor()
                
                query = """INSERT INTO foods 
                         (name, calories_per_100g, protein_per_100g, fat_per_100g, carbs_per_100g) 
                         VALUES (%s, %s, %s, %s, %s)"""
                cursor.execute(query, (name, calories, protein, fat, carbs))
                
                conn.commit()
                messagebox.showinfo("Success", "Food item added successfully")
                self.display_all_foods()  # Return to food list
            except Error as e:
                messagebox.showerror("Error", f"Failed to add food item: {e}")
            finally:
                cursor.close()
                conn.close()

    def update_user(self):
        self.display_all_users()

    def delete_user(self):
        self.display_all_users()

    def logout(self):
        self.root.destroy()
        # If you have a main app reference:
        # self.main_app.on_dashboard_close()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = Admin(root)
    root.mainloop()