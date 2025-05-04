import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import hashlib

class AdminDashboard:
    def __init__(self, root, main_app):
        self.root = root
        self.main_app = main_app
        
        # Configure main window
        self.root.title("Diet Tracker - Admin Dashboard")
        self.root.geometry("1000x700")
        self.root.minsize(900, 600)
        try:
            self.root.wm_iconbitmap("food.ico")
        except:
            pass
        self.root.config(bg="#f0f2f5")
        
        # Style configuration
        self.configure_styles()
        
        # Database connection
        self.conn = None
        self.connect_to_database()
        
        # UI Setup
        self.create_admin_dashboard()
        
        # Initialize with dashboard content
        self.update_dashboard_stats()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def configure_styles(self):
        """Configure ttk styles for the application"""
        style = ttk.Style()
        
        # Configure theme
        style.theme_use('clam')
        
        # Header style
        style.configure('Header.TFrame', background="#4796BD")
        style.configure('Header.TLabel', background="#4796BD", foreground='white', font=('Arial', 14, 'bold'))
        
        # Button styles
        style.configure('TButton', font=('Arial', 10), padding=5)
        style.configure('Primary.TButton', background='#E3EDEF', foreground='white')
        style.map('Primary.TButton', background=[('active', '#4796BD')])
        
        style.configure('Danger.TButton', background='#e74c3c', foreground='white')
        style.map('Danger.TButton', background=[('active', '#c0392b')])
        
        style.configure('Success.TButton', background='#2ecc71', foreground='white')
        style.map('Success.TButton', background=[('active', '#27ae60')])
        
        # Entry styles
        style.configure('TEntry', padding=5)
        
        # Treeview styles
        style.configure('Treeview', font=('Arial', 10), rowheight=25)
        style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
        style.map('Treeview', background=[('selected', '#E3EDEF')])

    def connect_to_database(self):
        """Connect to MySQL database"""
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Shivam@123",
                database="DietTracker3",
                autocommit=True
            )
            return True
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to connect to database:\n{str(e)}")
            return False

    def reconnect_database(self):
        """Reconnect to database if connection is lost"""
        if self.conn and self.conn.is_connected():
            return True
        
        return self.connect_to_database()

    def create_admin_dashboard(self):
        """Create the main dashboard layout"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Header frame
        header_frame = ttk.Frame(self.root, style='Header.TFrame')
        header_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(header_frame, text="Admin Dashboard", style='Header.TLabel').pack(side='left', padx=20, pady=10)
        
        # User info and logout button
        user_frame = ttk.Frame(header_frame)
        user_frame.pack(side='right', padx=20)
        
        ttk.Button(user_frame, text="Log Out", command=self.logout, style='Danger.TButton').pack(side='right', padx=5)

        # Footer
        self.footer = tk.Frame(self.root, bg="#4796BD")  
        self.footer.pack(side="bottom", fill="both")

        tk.Label(self.footer, bg="#4796BD", fg="white", text="shivam copyright ").pack( anchor="center")


        # Main content area
        main_frame = tk.Frame(self.root,bg="#f0f2f5")
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Navigation sidebar
        sidebar_frame = tk.Frame(main_frame, width=200,bg="#FFFFFE", relief='raised')
        sidebar_frame.pack(side='left', fill='y', padx=(0, 10))


        
        # Navigation menu
        nav_label = tk.Label(sidebar_frame, text="Navigation Menu", font=('Arial', 11, 'bold'),bg="#4796BD")
        nav_label.pack(fill='x', pady=(0, 15))
        
        menu_buttons = [
            ("Dashboard", self.create_dashboard_content),
            ("Manage Users", self.display_all_users),
            ("Manage Foods", self.display_all_foods),
            ("Add New Food", self.add_new_food),
            ("Add New User", self.add_new_user)
        ]
        
        for text, command in menu_buttons:
            ttk.Button(sidebar_frame, text=text, command=command, style='TButton').pack(fill='x', pady=2)

        # Content area
        self.content_frame = ttk.Frame(main_frame)
        self.content_frame.pack(side='right', fill='both', expand=True)
        

        
        # Initialize with dashboard content
        self.create_dashboard_content()

    def clear_content_frame(self):
        """Clear the content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def create_dashboard_content(self):
        """Create dashboard overview content"""
        self.clear_content_frame()
        
        # Title
        title_frame = ttk.Frame(self.content_frame)
        title_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(title_frame, text="Dashboard Overview", font=('Arial', 14, 'bold')).pack(side='left')
        
        # Stats cards
        stats_frame = ttk.Frame(self.content_frame)
        stats_frame.pack(fill='x', pady=(0, 20))
        
        # Total Users card
        user_card = ttk.Frame(stats_frame, style='TFrame')
        user_card.pack(side='left', expand=True, fill='both', padx=5)
        
        ttk.Label(user_card, text="Total Users", font=('Arial', 10, 'bold')).pack(pady=(10, 0))
        
        self.user_count_label = ttk.Label(user_card, text="Loading...", font=('Arial', 18, 'bold'))
        self.user_count_label.pack(pady=(0, 10))
        
        # Total Foods card
        food_card = ttk.Frame(stats_frame, style='TFrame')
        food_card.pack(side='left', expand=True, fill='both', padx=5)
        
        ttk.Label(food_card, text="Total Food Items", font=('Arial', 10, 'bold')).pack(pady=(10, 0))
        
        self.food_count_label = ttk.Label(food_card, text="Loading...", font=('Arial', 18, 'bold'))
        self.food_count_label.pack(pady=(0, 10))
        
        # Recent activity frame
        activity_frame = ttk.Frame(self.content_frame)
        activity_frame.pack(fill='both', expand=True)
        
        ttk.Label(activity_frame, text="Recent Activity", font=('Arial', 11, 'bold')).pack(anchor='w', pady=(0, 10))
        
        # Activity table
        self.activity_table = ttk.Treeview(activity_frame, columns=("Type", "Details", "Time"), show="headings", height=8)
        
        self.activity_table.heading("Type", text="Type")
        self.activity_table.heading("Details", text="Details")
        self.activity_table.heading("Time", text="Time")
        
        self.activity_table.column("Type", width=100, anchor='w')
        self.activity_table.column("Details", width=300, anchor='w')
        self.activity_table.column("Time", width=150, anchor='w')
        
        scroll_y = ttk.Scrollbar(activity_frame, orient='vertical', command=self.activity_table.yview)
        scroll_y.pack(side='right', fill='y')
        self.activity_table.configure(yscrollcommand=scroll_y.set)
        
        self.activity_table.pack(fill='both', expand=True)
        
        # Add sample activity (would come from database in real app)
        self.load_recent_activity()
        
        # Update stats
        self.update_dashboard_stats()

    def load_recent_activity(self):
        """Load recent activity from database"""
        if not self.reconnect_database():
            return
            
        try:
            cursor = self.conn.cursor()
            query = """
                (SELECT 'User' as type, CONCAT('User created: ', name) as details, created_at as time 
                 FROM users ORDER BY created_at DESC LIMIT 3)
                UNION
                (SELECT 'Food' as type, CONCAT('Food added: ', name) as details, created_at as time 
                 FROM foods ORDER BY created_at DESC LIMIT 3)
                ORDER BY time DESC LIMIT 5
            """
            cursor.execute(query)
            activities = cursor.fetchall()
            
            # Clear existing items
            for item in self.activity_table.get_children():
                self.activity_table.delete(item)
            
            # Add activities to table
            for activity in activities:
                self.activity_table.insert("", "end", values=activity)
                
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load recent activity:\n{str(e)}")
        finally:
            if cursor:
                cursor.close()

    def update_dashboard_stats(self):
        """Update the dashboard statistics"""
        if not self.reconnect_database():
            self.user_count_label.config(text="Error")
            self.food_count_label.config(text="Error")
            return
            
        try:
            cursor = self.conn.cursor()
            
            # Get total users
            cursor.execute("SELECT COUNT(*) FROM users")
            total_users = cursor.fetchone()[0]
            self.user_count_label.config(text=str(total_users))
            
            # Get total foods
            cursor.execute("SELECT COUNT(*) FROM foods")
            total_foods = cursor.fetchone()[0]
            self.food_count_label.config(text=str(total_foods))
            
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to update stats:\n{str(e)}")
        finally:
            if cursor:
                cursor.close()

    def display_all_users(self):
        """Display all users in a table"""
        self.clear_content_frame()
        
        # Title and controls
        title_frame = ttk.Frame(self.content_frame)
        title_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(title_frame, text="User Management", font=('Arial', 14, 'bold')).pack(side='left')
        
        button_frame = ttk.Frame(title_frame)
        button_frame.pack(side='right')
        
        ttk.Button(button_frame, text="Refresh", command=self.display_all_users, style='TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="Add User", command=self.add_new_user, style='Success.TButton').pack(side='left', padx=5)
        
        # User table frame
        table_frame = ttk.Frame(self.content_frame)
        table_frame.pack(fill='both', expand=True)
        
        # Create scrollbars
        scroll_y = ttk.Scrollbar(table_frame)
        scroll_y.pack(side='right', fill='y')
        
        scroll_x = ttk.Scrollbar(table_frame, orient='horizontal')
        scroll_x.pack(side='bottom', fill='x')
        
        # Create user table
        self.user_table = ttk.Treeview(
            table_frame,
            columns=('ID', 'Name', 'Email', 'Password', 'Calorie Goal', 'Role', 'Created'),
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            selectmode='browse'
        )
        
        # Configure columns
        self.user_table.heading('#0', text='')
        self.user_table.heading('ID', text='ID', anchor='w')
        self.user_table.heading('Name', text='Name', anchor='w')
        self.user_table.heading('Email', text='Email', anchor='w')
        self.user_table.heading('Password', text='Password', anchor='w')
        self.user_table.heading('Calorie Goal', text='Calorie Goal', anchor='w')
        self.user_table.heading('Role', text='Role', anchor='w')
        self.user_table.heading('Created', text='Created', anchor='w')
        
        self.user_table.column('#0', width=0, stretch=False)
        self.user_table.column('ID', width=50, minwidth=50)
        self.user_table.column('Name', width=150, minwidth=100)
        self.user_table.column('Email', width=200, minwidth=150)
        self.user_table.column('Password', width=100, minwidth=80)
        self.user_table.column('Calorie Goal', width=100, minwidth=80)
        self.user_table.column('Role', width=80, minwidth=60)
        self.user_table.column('Created', width=120, minwidth=100)
        
        self.user_table.pack(fill='both', expand=True)
        
        # Configure scrollbars
        scroll_y.config(command=self.user_table.yview)
        scroll_x.config(command=self.user_table.xview)
        
        # Action buttons
        action_frame = ttk.Frame(self.content_frame)
        action_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Button(action_frame, text="Update User", command=self.update_selected_user, style='Primary.TButton').pack(side='left', padx=5)
        ttk.Button(action_frame, text="Delete User", command=self.delete_selected_user, style='Danger.TButton').pack(side='left', padx=5)
        
        # Load user data
        self.load_user_data()

    def load_user_data(self):
        """Load user data from database"""
        if not self.reconnect_database():
            return
            
        try:
            cursor = self.conn.cursor(dictionary=True)
            query = "SELECT user_id, name, email, password, daily_calorie_goal, role, created_at FROM users"
            cursor.execute(query)
            users = cursor.fetchall()
            
            # Clear existing data
            for item in self.user_table.get_children():
                self.user_table.delete(item)
            
            # Add users to table
            for user in users:
                # Hash password for display
                hashed_pw = hashlib.sha256(user['password'].encode()).hexdigest()[:8] + "..."
                self.user_table.insert('', 'end', values=(
                    user['user_id'],
                    user['name'],
                    user['email'],
                    hashed_pw,
                    user['daily_calorie_goal'],
                    user['role'],
                    user['created_at'].strftime('%Y-%m-%d %H:%M') if user['created_at'] else ''
                ))
                
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load users:\n{str(e)}")
        finally:
            if cursor:
                cursor.close()

    def update_selected_user(self):
        """Update the selected user"""
        selected = self.user_table.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a user to update")
            return
            
        user_id = self.user_table.item(selected, 'values')[0]
        self.edit_user(user_id)

    def edit_user(self, user_id):
        """Edit user form"""
        self.clear_content_frame()
        
        # Get user data
        if not self.reconnect_database():
            return
            
        try:
            cursor = self.conn.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()
            
            if not user:
                messagebox.showerror("Error", "User not found")
                self.display_all_users()
                return
                
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load user:\n{str(e)}")
            return
        finally:
            if cursor:
                cursor.close()
        
        # Title
        title_frame = ttk.Frame(self.content_frame)
        title_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(title_frame, text=f"Edit User: {user['name']}", font=('Arial', 14, 'bold')).pack(side='left')
        
        ttk.Button(title_frame, text="Back", command=self.display_all_users, style='TButton').pack(side='right')
        
        # Form frame
        form_frame = ttk.Frame(self.content_frame)
        form_frame.pack(fill='both', expand=True)
        
        # Form fields
        fields = [
            ("Name:", "name", user['name']),
            ("Email:", "email", user['email']),
            ("Password:", "password", "", True),  # Password field
            ("Daily Calorie Goal:", "calorie_goal", user['daily_calorie_goal']),
            ("Role:", "role", user['role'])
        ]
        
        self.user_form_vars = {}
        
        for i, (label_text, field_name, default_value, *options) in enumerate(fields):
            row_frame = ttk.Frame(form_frame)
            row_frame.pack(fill='x', pady=5)
            
            ttk.Label(row_frame, text=label_text, width=20, anchor='e').pack(side='left', padx=5)
            
            if options and options[0]:  # Password field
                entry = ttk.Entry(row_frame, show="*")
            else:
                entry = ttk.Entry(row_frame)
                
            entry.insert(0, default_value)
            entry.pack(side='left', fill='x', expand=True)
            
            self.user_form_vars[field_name] = entry
        
        # Submit button
        submit_btn = ttk.Button(
            form_frame, 
            text="Update User", 
            command=lambda: self.submit_user_update(user_id), 
            style='Primary.TButton'
        )
        submit_btn.pack(pady=20)

    def submit_user_update(self, user_id):
        """Submit user update to database"""
        # Get form data
        name = self.user_form_vars['name'].get().strip()
        email = self.user_form_vars['email'].get().strip()
        password = self.user_form_vars['password'].get().strip()
        calorie_goal = self.user_form_vars['calorie_goal'].get().strip()
        role = self.user_form_vars['role'].get().strip()
        
        # Validate inputs
        if not all([name, email, calorie_goal, role]):
            messagebox.showwarning("Warning", "Please fill in all required fields")
            return
            
        if not calorie_goal.isdigit():
            messagebox.showwarning("Warning", "Calorie goal must be a number")
            return
            
        # Prepare update query
        update_fields = {
            'name': name,
            'email': email,
            'daily_calorie_goal': calorie_goal,
            'role': role
        }
        
        # Only update password if it was changed
        if password:
            update_fields['password'] = password
            
        if not self.reconnect_database():
            return
            
        try:
            cursor = self.conn.cursor()
            
            # Build the update query dynamically
            set_clause = ", ".join([f"{field} = %s" for field in update_fields.keys()])
            values = list(update_fields.values())
            values.append(user_id)
            
            query = f"UPDATE users SET {set_clause} WHERE user_id = %s"
            cursor.execute(query, values)
            
            messagebox.showinfo("Success", "User updated successfully")
            self.display_all_users()
            
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to update user:\n{str(e)}")
        finally:
            if cursor:
                cursor.close()

    def delete_selected_user(self):
        """Delete the selected user"""
        selected = self.user_table.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a user to delete")
            return
            
        user_id = self.user_table.item(selected, 'values')[0]
        user_name = self.user_table.item(selected, 'values')[1]
        
        # Confirm deletion
        confirm = messagebox.askyesno(
            "Confirm Delete", 
            f"Are you sure you want to delete user:\n\n{user_name} (ID: {user_id})?\n\nThis action cannot be undone."
        )
        
        if not confirm:
            return
            
        if not self.reconnect_database():
            return
            
        try:
            cursor = self.conn.cursor()
            
            # First delete dependent records
            cursor.execute("DELETE FROM food_log WHERE user_id = %s", (user_id,))
            cursor.execute("DELETE FROM water_intake WHERE user_id = %s", (user_id,))
            
            # Then delete the user
            cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
            
            messagebox.showinfo("Success", "User deleted successfully")
            self.display_all_users()
            
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to delete user:\n{str(e)}")
            self.conn.rollback()
        finally:
            if cursor:
                cursor.close()

    def add_new_user(self):
        """Form to add a new user"""
        self.clear_content_frame()
        
        # Title
        title_frame = ttk.Frame(self.content_frame)
        title_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(title_frame, text="Add New User", font=('Arial', 14, 'bold')).pack(side='left')
        
        ttk.Button(title_frame, text="Back", command=self.display_all_users, style='TButton').pack(side='right')
        
        # Form frame
        form_frame = ttk.Frame(self.content_frame)
        form_frame.pack(fill='both', expand=True)
        
        # Form fields
        fields = [
            ("Name:", "name", ""),
            ("Email:", "email", ""),
            ("Password:", "password", "", True),  # Password field
            ("Daily Calorie Goal:", "calorie_goal", "2000"),
            ("Role:", "role", "user")
        ]
        
        self.new_user_vars = {}
        
        for i, (label_text, field_name, default_value, *options) in enumerate(fields):
            row_frame = ttk.Frame(form_frame)
            row_frame.pack(fill='x', pady=5)
            
            ttk.Label(row_frame, text=label_text, width=20, anchor='e').pack(side='left', padx=5)
            
            if options and options[0]:  # Password field
                entry = ttk.Entry(row_frame, show="*")
            else:
                entry = ttk.Entry(row_frame)
                
            entry.insert(0, default_value)
            entry.pack(side='left', fill='x', expand=True)
            
            self.new_user_vars[field_name] = entry
        
        # Submit button
        submit_btn = ttk.Button(
            form_frame, 
            text="Add User", 
            command=self.submit_new_user, 
            style='Success.TButton'
        )
        submit_btn.pack(pady=20)

    def submit_new_user(self):
        """Submit new user to database"""
        # Get form data
        name = self.new_user_vars['name'].get().strip()
        email = self.new_user_vars['email'].get().strip()
        password = self.new_user_vars['password'].get().strip()
        calorie_goal = self.new_user_vars['calorie_goal'].get().strip()
        role = self.new_user_vars['role'].get().strip()
        
        # Validate inputs
        if not all([name, email, password, calorie_goal, role]):
            messagebox.showwarning("Warning", "Please fill in all required fields")
            return
            
        if not calorie_goal.isdigit():
            messagebox.showwarning("Warning", "Calorie goal must be a number")
            return
            
        if not self.reconnect_database():
            return
            
        try:
            cursor = self.conn.cursor()
            
            # Check if email already exists
            cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s", (email,))
            if cursor.fetchone()[0] > 0:
                messagebox.showwarning("Warning", "Email already exists")
                return
                
            # Insert new user
            query = """
                INSERT INTO users 
                (name, email, password, daily_calorie_goal, role, created_at) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                name, 
                email, 
                password, 
                calorie_goal, 
                role, 
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))
            
            messagebox.showinfo("Success", "User added successfully")
            self.display_all_users()
            
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to add user:\n{str(e)}")
        finally:
            if cursor:
                cursor.close()

    def display_all_foods(self):
        """Display all foods in a table"""
        self.clear_content_frame()
        
        # Title and controls
        title_frame = ttk.Frame(self.content_frame)
        title_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(title_frame, text="Food Management", font=('Arial', 14, 'bold')).pack(side='left')
        
        button_frame = ttk.Frame(title_frame)
        button_frame.pack(side='right')
        
        ttk.Button(button_frame, text="Refresh", command=self.display_all_foods, style='TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="Add Food", command=self.add_new_food, style='Success.TButton').pack(side='left', padx=5)
        
        # Food table frame
        table_frame = ttk.Frame(self.content_frame)
        table_frame.pack(fill='both', expand=True)
        
        # Create scrollbars
        scroll_y = ttk.Scrollbar(table_frame)
        scroll_y.pack(side='right', fill='y')
        
        scroll_x = ttk.Scrollbar(table_frame, orient='horizontal')
        scroll_x.pack(side='bottom', fill='x')
        
        # Create food table
        self.food_table = ttk.Treeview(
            table_frame,
            columns=('ID', 'Name', 'Calories', 'Protein', 'Fat', 'Carbs', 'Created'),
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            selectmode='browse'
        )
        
        # Configure columns
        self.food_table.heading('#0', text='')
        self.food_table.heading('ID', text='ID', anchor='w')
        self.food_table.heading('Name', text='Name', anchor='w')
        self.food_table.heading('Calories', text='Calories', anchor='w')
        self.food_table.heading('Protein', text='Protein', anchor='w')
        self.food_table.heading('Fat', text='Fat', anchor='w')
        self.food_table.heading('Carbs', text='Carbs', anchor='w')
        self.food_table.heading('Created', text='Created', anchor='w')
        
        self.food_table.column('#0', width=0, stretch=False)
        self.food_table.column('ID', width=50, minwidth=50)
        self.food_table.column('Name', width=200, minwidth=150)
        self.food_table.column('Calories', width=80, minwidth=70)
        self.food_table.column('Protein', width=80, minwidth=70)
        self.food_table.column('Fat', width=80, minwidth=70)
        self.food_table.column('Carbs', width=80, minwidth=70)
        self.food_table.column('Created', width=120, minwidth=100)
        
        self.food_table.pack(fill='both', expand=True)
        
        # Configure scrollbars
        scroll_y.config(command=self.food_table.yview)
        scroll_x.config(command=self.food_table.xview)
        
        # Action buttons
        action_frame = ttk.Frame(self.content_frame)
        action_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Button(action_frame, text="Update Food", command=self.update_selected_food, style='Primary.TButton').pack(side='left', padx=5)
        ttk.Button(action_frame, text="Delete Food", command=self.delete_selected_food, style='Danger.TButton').pack(side='left', padx=5)
        
        # Load food data
        self.load_food_data()

    def load_food_data(self):
        """Load food data from database"""
        if not self.reconnect_database():
            return
            
        try:
            cursor = self.conn.cursor(dictionary=True)
            query = """
                SELECT food_id, name, calories_per_100g, protein_per_100g, 
                       fat_per_100g, carbs_per_100g, created_at 
                FROM foods
            """
            cursor.execute(query)
            foods = cursor.fetchall()
            
            # Clear existing data
            for item in self.food_table.get_children():
                self.food_table.delete(item)
            
            # Add foods to table
            for food in foods:
                self.food_table.insert('', 'end', values=(
                    food['food_id'],
                    food['name'],
                    food['calories_per_100g'],
                    food['protein_per_100g'],
                    food['fat_per_100g'],
                    food['carbs_per_100g'],
                    food['created_at'].strftime('%Y-%m-%d %H:%M') if food['created_at'] else ''
                ))
                
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load foods:\n{str(e)}")
        finally:
            if cursor:
                cursor.close()

    def update_selected_food(self):
        """Update the selected food"""
        selected = self.food_table.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a food to update")
            return
            
        food_id = self.food_table.item(selected, 'values')[0]
        self.edit_food(food_id)

    def edit_food(self, food_id):
        """Edit food form"""
        self.clear_content_frame()
        
        # Get food data
        if not self.reconnect_database():
            return
            
        try:
            cursor = self.conn.cursor(dictionary=True)
            query = "SELECT * FROM foods WHERE food_id = %s"
            cursor.execute(query, (food_id,))
            food = cursor.fetchone()
            
            if not food:
                messagebox.showerror("Error", "Food not found")
                self.display_all_foods()
                return
                
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load food:\n{str(e)}")
            return
        finally:
            if cursor:
                cursor.close()
        
        # Title
        title_frame = ttk.Frame(self.content_frame)
        title_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(title_frame, text=f"Edit Food: {food['name']}", font=('Arial', 14, 'bold')).pack(side='left')
        
        ttk.Button(title_frame, text="Back", command=self.display_all_foods, style='TButton').pack(side='right')
        
        # Form frame
        form_frame = ttk.Frame(self.content_frame)
        form_frame.pack(fill='both', expand=True)
        
        # Form fields
        fields = [
            ("Name:", "name", food['name']),
            ("Calories (per 100g):", "calories", food['calories_per_100g']),
            ("Protein (per 100g):", "protein", food['protein_per_100g']),
            ("Fat (per 100g):", "fat", food['fat_per_100g']),
            ("Carbs (per 100g):", "carbs", food['carbs_per_100g'])
        ]
        
        self.food_form_vars = {}
        
        for i, (label_text, field_name, default_value) in enumerate(fields):
            row_frame = ttk.Frame(form_frame)
            row_frame.pack(fill='x', pady=5)
            
            ttk.Label(row_frame, text=label_text, width=20, anchor='e').pack(side='left', padx=5)
            
            entry = ttk.Entry(row_frame)
            entry.insert(0, default_value)
            entry.pack(side='left', fill='x', expand=True)
            
            self.food_form_vars[field_name] = entry
        
        # Submit button
        submit_btn = ttk.Button(
            form_frame, 
            text="Update Food", 
            command=lambda: self.submit_food_update(food_id), 
            style='Primary.TButton'
        )
        submit_btn.pack(pady=20)

    def submit_food_update(self, food_id):
        """Submit food update to database"""
        # Get form data
        name = self.food_form_vars['name'].get().strip()
        calories = self.food_form_vars['calories'].get().strip()
        protein = self.food_form_vars['protein'].get().strip()
        fat = self.food_form_vars['fat'].get().strip()
        carbs = self.food_form_vars['carbs'].get().strip()
        
        # Validate inputs
        if not all([name, calories, protein, fat, carbs]):
            messagebox.showwarning("Warning", "Please fill in all required fields")
            return
            
        for value in [calories, protein, fat, carbs]:
            if not self.is_float(value):
                messagebox.showwarning("Warning", "Nutrition values must be numbers")
                return
                
        if not self.reconnect_database():
            return
            
        try:
            cursor = self.conn.cursor()
            
            query = """
                UPDATE foods SET 
                name = %s, 
                calories_per_100g = %s, 
                protein_per_100g = %s,
                fat_per_100g = %s,
                carbs_per_100g = %s
                WHERE food_id = %s
            """
            cursor.execute(query, (name, calories, protein, fat, carbs, food_id))
            
            messagebox.showinfo("Success", "Food updated successfully")
            self.display_all_foods()
            
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to update food:\n{str(e)}")
        finally:
            if cursor:
                cursor.close()

    def is_float(self, value):
        """Check if a string can be converted to float"""
        try:
            float(value)
            return True
        except ValueError:
            return False

    def delete_selected_food(self):
        """Delete the selected food"""
        selected = self.food_table.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a food to delete")
            return
            
        food_id = self.food_table.item(selected, 'values')[0]
        food_name = self.food_table.item(selected, 'values')[1]
        
        # Confirm deletion
        confirm = messagebox.askyesno(
            "Confirm Delete", 
            f"Are you sure you want to delete food:\n\n{food_name} (ID: {food_id})?\n\nThis will also delete all related food log entries."
        )
        
        if not confirm:
            return
            
        if not self.reconnect_database():
            return
            
        try:
            cursor = self.conn.cursor()
            
            # First delete dependent records
            cursor.execute("DELETE FROM food_log WHERE food_id = %s", (food_id,))
            
            # Then delete the food
            cursor.execute("DELETE FROM foods WHERE food_id = %s", (food_id,))
            
            messagebox.showinfo("Success", "Food deleted successfully")
            self.display_all_foods()
            
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to delete food:\n{str(e)}")
            self.conn.rollback()
        finally:
            if cursor:
                cursor.close()

    def add_new_food(self):
        """Form to add a new food"""
        self.clear_content_frame()
        
        # Title
        title_frame = ttk.Frame(self.content_frame)
        title_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(title_frame, text="Add New Food", font=('Arial', 14, 'bold')).pack(side='left')
        
        ttk.Button(title_frame, text="Back", command=self.display_all_foods, style='TButton').pack(side='right')
        
        # Form frame
        form_frame = ttk.Frame(self.content_frame)
        form_frame.pack(fill='both', expand=True)
        
        # Form fields
        fields = [
            ("Name:", "name", ""),
            ("Calories (per 100g):", "calories", ""),
            ("Protein (per 100g):", "protein", ""),
            ("Fat (per 100g):", "fat", ""),
            ("Carbs (per 100g):", "carbs", "")
        ]
        
        self.new_food_vars = {}
        
        for i, (label_text, field_name, default_value) in enumerate(fields):
            row_frame = ttk.Frame(form_frame)
            row_frame.pack(fill='x', pady=5)
            
            ttk.Label(row_frame, text=label_text, width=20, anchor='e').pack(side='left', padx=5)
            
            entry = ttk.Entry(row_frame)
            entry.insert(0, default_value)
            entry.pack(side='left', fill='x', expand=True)
            
            self.new_food_vars[field_name] = entry
        
        # Submit button
        submit_btn = ttk.Button(
            form_frame, 
            text="Add Food", 
            command=self.submit_new_food, 
            style='Success.TButton'
        )
        submit_btn.pack(pady=20)

    def submit_new_food(self):
        """Submit new food to database"""
        # Get form data
        name = self.new_food_vars['name'].get().strip()
        calories = self.new_food_vars['calories'].get().strip()
        protein = self.new_food_vars['protein'].get().strip()
        fat = self.new_food_vars['fat'].get().strip()
        carbs = self.new_food_vars['carbs'].get().strip()
        
        # Validate inputs
        if not all([name, calories, protein, fat, carbs]):
            messagebox.showwarning("Warning", "Please fill in all required fields")
            return
            
        for value in [calories, protein, fat, carbs]:
            if not self.is_float(value):
                messagebox.showwarning("Warning", "Nutrition values must be numbers")
                return
                
        if not self.reconnect_database():
            return
            
        try:
            cursor = self.conn.cursor()
            
            # Insert new food
            query = """
                INSERT INTO foods 
                (name, calories_per_100g, protein_per_100g, fat_per_100g, carbs_per_100g, created_at) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                name, 
                calories, 
                protein, 
                fat, 
                carbs, 
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))
            
            messagebox.showinfo("Success", "Food added successfully")
            self.display_all_foods()
            
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to add food:\n{str(e)}")
        finally:
            if cursor:
                cursor.close()

    def logout(self):
        """Log out of admin dashboard"""
        if self.conn and self.conn.is_connected():
            self.conn.close()
        self.root.destroy()
        self.main_app.on_dashboard_close()

    def on_close(self):
        """Handle window close event"""
        if messagebox.askokcancel("Quit", "Do you want to quit the application?"):
            self.logout()

if __name__ == "__main__":
    # For testing purposes
    class MockMainApp:
        def on_dashboard_close(self):
            print("Dashboard closed")
    
    root = tk.Tk()
    app = AdminDashboard(root, MockMainApp())
    root.mainloop()