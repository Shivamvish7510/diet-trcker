import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from mysql.connector import Error


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

# Main Application Class
class Admin:
    def __init__(self, root,main_app ):
        self.root = root
        self.main_app = main_app 
        
        self.root.title("Diet Tracker")
        self.root.geometry("800x500")
        root.wm_iconbitmap("food.ico")
        self.create_admin_dashboard()

                # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        root.config(bg="#E3EDEF")

    def create_admin_dashboard(self):
        # Create User Dashboard Frame
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Header
        self.user = tk.Frame(self.root, bg="#4796BD", height=50)  # Set a fixed height
        self.user.pack(fill="x")
        tk.Label(self.user, bg="#4796BD", fg="white", text="Admin Dashboard", 
                 font=("Arial", 18, "bold")).pack(side="left",padx=20,pady=15, anchor="center")
        
        logout_btn = ttk.Button(self.user, 
                              text="Log Out",
                              style="TButton",
                              command=self.logout)
        logout_btn.pack(side="right", padx=20, pady=15)

        # Footer
        self.footer = tk.Frame(self.root, bg="#4796BD")  
        self.footer.pack(side="bottom", fill="both")

        tk.Label(self.footer, bg="#4796BD", fg="white", text="shivam copyright ").pack( anchor="center")
        
        # admin dashboard frame
        self.dashboard = tk.Frame(self.root, bg="#FFFFFE", bd=2)
        self.dashboard.pack(side="left", fill="y", anchor="n", padx=(0, 50))

        # Navigation Menu
        self.navigation_menu = tk.Frame(self.dashboard, bg="#FFFFFE")
        self.navigation_menu.pack(side="top", fill="both", expand=True)

        # Menu buttons frame
        self.menu_buttons_frame = tk.Frame(self.navigation_menu, bg="#FFFFFE")
        self.menu_buttons_frame.pack(side="top", fill="x")

        tk.Label(self.menu_buttons_frame, text="Navigation Menu",bg="#4796BD", font=("Arial", 10, "bold")).pack(side="top", fill="x")
        tk.Button(self.menu_buttons_frame, text="Dashboard", font=("Arial", 10), command=self.create_admin_dashboard).pack(side="top", fill="x")
        tk.Button(self.menu_buttons_frame, text="Manage Users",command=self.display_all_users, font=("Arial", 10)).pack(side="top", fill="x")
        tk.Button(self.menu_buttons_frame, text="Manage Food", font=("Arial", 10),command=self.display_all_foods).pack(side="top", fill="x")
        tk.Button(self.menu_buttons_frame, text="add new food", font=("Arial", 10) , command=self.add_new_food).pack(side="top", fill="x")
        tk.Button(self.menu_buttons_frame, text="Add new user",command=self.add_new_user, font=("Arial", 10)).pack(side="top", fill="x")


        # Login button frame
        self.login_button_frame = tk.Frame(self.navigation_menu, bg="#FFFFFE")
        self.login_button_frame.pack(side="bottom", fill="x")

        tk.Button(self.login_button_frame, bg="#4796BD", fg="white",text="Log Out",command=self.logout ,font=("Arial", 10,"bold")).pack(side="bottom",pady=5, fill="x")


        # Dashboard Statistics

        self.right_side_frame = tk.Frame(self.root, bg="#FFFFFE", bd=2,width=400, height=500)
        self.right_side_frame.pack(side="left", fill="both",expand=True, anchor="ne")
        

        scrollbar = tk.Scrollbar(self.right_side_frame)
        scrollbar.pack(side="right", fill="y")

             # Dashboard content
        self.create_dashboard_content()

    def create_dashboard_content(self):
        # Clear content area
        for widget in self.right_side_frame.winfo_children():
            widget.destroy()
        
        # Title
        title_frame = tk.Frame(self.right_side_frame, bg="#FFFFFE")
        title_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Label(title_frame, 
                 text="Dashboard Overview",background="#E3EDEF" ,font=("Arial", 18),
                 style="Header.TLabel").pack(side="left", anchor="w")
        
        # Stats cards
        stats_frame = tk.Frame(self.right_side_frame, bg="#FFFFFE")
        stats_frame.pack(fill="x", pady=(0, 20))
        
        # Total Users card
        user_card = tk.Frame(stats_frame, bg="#FFFFFE", relief="raised", bd=1)
        user_card.pack(side="left", fill="both", expand=True, padx=5)
        
        tk.Label(user_card, 
                 text="Total Users", font=("Arial", 10, "bold"),bg="#FFFFFE" 
                 ).pack(pady=(10, 0))
        
        self.user_count_label = tk.Label(user_card,  font=("Arial", 18, "bold"),bg="#FFFFFE",
                                        text="0")
        self.user_count_label.pack(pady=(0, 10))
        
        # Total Foods card
        food_card = tk.Frame(stats_frame, bg="#FFFFFE", relief="raised", bd=1)
        food_card.pack(side="left", fill="both", expand=True, padx=5)
        
        tk.Label(food_card, 
                 text="Total Food Items",  font=("Arial", 10, "bold"),bg="#FFFFFE"
                 ).pack(pady=(10, 0))
        
        self.food_count_label = tk.Label(food_card,  font=("Arial", 18, "bold"),bg="#FFFFFE",
                                         text="0")
        self.food_count_label.pack(pady=(0, 10))
        
        # Recent activity frame
        activity_frame = tk.Frame(self.right_side_frame, bg="#FFFFFE")
        activity_frame.pack(fill="both", expand=True)
        
        ttk.Label(activity_frame, 
                 text="Recent Activity",background="#E3EDEF",font=("Arial", 10), 
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
            # Add sample activity (would come from database in real app)
        self.load_recent_activity()
        
        
        # Update stats
        self.update_dashboard_stats()

    def load_recent_activity(self):
        """Load recent activity from database"""
   
        try:
            conn = connect_to_database()
            cursor = conn.cursor()
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
        # finally:
            
        #     cursor.close()

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

    def display_all_foods(self):
        # Clear existing widgets
        for widget in self.right_side_frame.winfo_children():
            widget.destroy()

        title_frame = tk.Frame(self.right_side_frame, bg="#FFFFFE")
        title_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Label(title_frame, 
                 text="Food management",background="#E3EDEF" ,font=("Arial", 18),
                 style="Header.TLabel").pack(side="left", anchor="w")
        
        refresh_btn = ttk.Button(title_frame, 
                               text="Refresh",
                               style="TButton",
                               command=self.display_all_foods)
        refresh_btn.pack(side="right", padx=5)

        # Create a frame to hold the food list
        self.food_list_frame = tk.Frame(self.right_side_frame, bg="#FFFFFE")
        self.food_list_frame.pack(side="top", fill="both", expand=True)

        # Create a scrollbar
        self.scrollbar = tk.Scrollbar(self.food_list_frame)
        self.scrollbar.pack(side="right", fill="y")

        # Create a horizontal scrollbar
        self.x_scrollbar = tk.Scrollbar(self.food_list_frame, orient=tk.HORIZONTAL)
        self.x_scrollbar.pack(side="bottom", fill="x")

        # Create a table to display the food list
        self.food_list_table = ttk.Treeview(self.food_list_frame, 
                                          yscrollcommand=self.scrollbar.set,
                                          xscrollcommand=self.x_scrollbar.set)
        self.food_list_table.pack(side="left", fill="both", expand=True)

        # Configure the scrollbars
        self.scrollbar.config(command=self.food_list_table.yview)
        self.x_scrollbar.config(command=self.food_list_table.xview)

        # Define the columns
        self.food_list_table['columns'] = ('Food ID', 'Food Name', 'Calories', 'Portion', 'Fat', 'Carbohydrates','Created')

        # Format the columns
        self.food_list_table.column("#0", width=0, stretch=tk.NO)
        self.food_list_table.column("Food ID", anchor=tk.W, width=50)
        self.food_list_table.column("Food Name", anchor=tk.W, width=150)
        self.food_list_table.column("Calories", anchor=tk.W, width=80)
        self.food_list_table.column("Portion", anchor=tk.W, width=80)
        self.food_list_table.column("Fat", anchor=tk.W, width=80)
        self.food_list_table.column("Carbohydrates", anchor=tk.W, width=100)
        self.food_list_table.column("Created", anchor=tk.W, width=100)

        # Create the headings
        self.food_list_table.heading("#0", text="", anchor=tk.W)
        self.food_list_table.heading("Food ID", text="Food ID", anchor=tk.W)
        self.food_list_table.heading("Food Name", text="Food Name", anchor=tk.W)
        self.food_list_table.heading("Calories", text="Calories", anchor=tk.W)
        self.food_list_table.heading("Portion", text="Portion", anchor=tk.W)
        self.food_list_table.heading("Fat", text="Fat (per 100g)", anchor=tk.W)
        self.food_list_table.heading("Carbohydrates", text="Carbs (per 100g)", anchor=tk.W)
        self.food_list_table.heading("Created", text="Created", anchor=tk.W)

        # Retrieve food data from database
        conn = connect_to_database()
        cursor = conn.cursor()
        query = "SELECT * FROM foods"
        cursor.execute(query)
        food_data = cursor.fetchall()
        cursor.close()
        conn.close()

        # Insert food data into table
        for food in food_data:
            self.food_list_table.insert('', 'end', values=(food[0], food[1], food[2], food[3], food[4], food[5],food[6]))

        # Add action buttons frame
        self.food_action_frame = tk.Frame(self.right_side_frame, bg="#FFFFFE")
        self.food_action_frame.pack(side="bottom", fill="x", pady=10)

        # Add food button
        tk.Button(self.food_action_frame, text="Add Food", bg="#4796BD", fg="white",
                 font=("Arial", 10, "bold"), command=self.add_new_food).pack(side="left", padx=5)
        
        # Add update button
        tk.Button(self.food_action_frame, text="Update Selected Food", bg="#4796BD", fg="white",
                 font=("Arial", 10, "bold"), command=self.update_selected_food).pack(side="left", padx=5)

        # Add delete button
        tk.Button(self.food_action_frame, text="Delete Selected Food", bg="#FF0000", fg="white",
                 font=("Arial", 10, "bold"), command=self.delete_selected_food).pack(side="left", padx=5)

    def update_selected_food(self):
        selected_item = self.food_list_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a food item to update")
            return

        # Get the selected food's data
        food_data = self.food_list_table.item(selected_item, 'values')
        
        # Clear existing widgets
        for widget in self.right_side_frame.winfo_children():
            widget.destroy()

        # Create a frame to hold the input fields
        self.input_fields_frame = tk.Frame(self.right_side_frame, bg="#FFFFFE")
        self.input_fields_frame.pack(side="top", fill="both", expand=True)

        # Create input fields with current values
        tk.Label(self.input_fields_frame, text="Food ID:", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5)
        self.food_id_entry = tk.Entry(self.input_fields_frame, font=("Arial", 10))
        self.food_id_entry.insert(0, food_data[0])
        self.food_id_entry.config(state='readonly')
        self.food_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.input_fields_frame, text="Food Name:", font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=5)
        self.food_name_entry = tk.Entry(self.input_fields_frame, font=("Arial", 10))
        self.food_name_entry.insert(0, food_data[1])
        self.food_name_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.input_fields_frame, text="Calories:", font=("Arial", 10)).grid(row=2, column=0, padx=5, pady=5)
        self.calories_entry = tk.Entry(self.input_fields_frame, font=("Arial", 10))
        self.calories_entry.insert(0, food_data[2])
        self.calories_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.input_fields_frame, text="Portion:", font=("Arial", 10)).grid(row=3, column=0, padx=5, pady=5)
        self.portion_entry = tk.Entry(self.input_fields_frame, font=("Arial", 10))
        self.portion_entry.insert(0, food_data[3])
        self.portion_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.input_fields_frame, text="Fat (per 100g):", font=("Arial", 10)).grid(row=4, column=0, padx=5, pady=5)
        self.fat_entry = tk.Entry(self.input_fields_frame, font=("Arial", 10))
        self.fat_entry.insert(0, food_data[4])
        self.fat_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(self.input_fields_frame, text="Carbs (per 100g):", font=("Arial", 10)).grid(row=5, column=0, padx=5, pady=5)
        self.carb_entry = tk.Entry(self.input_fields_frame, font=("Arial", 10))
        self.carb_entry.insert(0, food_data[5])
        self.carb_entry.grid(row=5, column=1, padx=5, pady=5)

        # Create a button to submit the update
        tk.Button(self.input_fields_frame, bg="#4796BD", fg="white", text="Update Food", 
                 font=("Arial", 10, "bold"), command=self.submit_update_food).grid(row=6, column=1, padx=5, pady=10)

        # Back button
        tk.Button(self.input_fields_frame, text="Back", font=("Arial", 10),
                 command=self.display_all_foods).grid(row=6, column=0, padx=5, pady=10)

    def submit_update_food(self):
        try:
            # Get the updated values
            food_id = self.food_id_entry.get()
            food_name = self.food_name_entry.get()
            calories = self.calories_entry.get()
            portion = self.portion_entry.get()
            fat = self.fat_entry.get()
            carb = self.carb_entry.get()

            # Validate inputs
            if not all([food_name, calories, portion]):
                messagebox.showerror("Error", "Please fill in all required fields")
                return

            # Update the food in database
            conn = connect_to_database()
            cursor = conn.cursor()
            query = """UPDATE foods SET 
                      name = %s, 
                      calories_per_100g = %s, 
                      protein_per_100g = %s,
                      fat_per_100g = %s,
                      carbs_per_100g = %s
                      WHERE food_id = %s"""
            cursor.execute(query, (food_name, calories, portion, fat, carb, food_id))
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "Food updated successfully")
            self.display_all_foods()  # Refresh the food list

        except Error as e:
            messagebox.showerror("Error", f"Failed to update food: {e}")

    def delete_selected_food(self):
        selected_item = self.food_list_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a food item to delete")
            return

        # Get the selected food's ID
        food_id = self.food_list_table.item(selected_item, 'values')[0]
        food_name = self.food_list_table.item(selected_item, 'values')[1]

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Delete", 
                                     f"Are you sure you want to delete {food_name} (ID: {food_id})?")

        if confirm:
            try:
                # Delete the food from database
                conn = connect_to_database()
                cursor = conn.cursor()
                # First delete from food_log
                query1 = "DELETE FROM food_log WHERE food_id = %s;"
                cursor.execute(query1, (food_id,))

                # Then delete from foods
                query2 = "DELETE FROM foods WHERE food_id = %s;"
                cursor.execute(query2, (food_id,))
                conn.commit()
                cursor.close()
                conn.close()

                messagebox.showinfo("Success", "Food deleted successfully")
                self.display_all_foods()  # Refresh the food list

            except Error as e:
                messagebox.showerror("Error", f"Failed to delete food: {e}")

    def display_all_users(self):
        # Clear existing widgets
        for widget in self.right_side_frame.winfo_children():
            widget.destroy()


        title_frame = tk.Frame(self.right_side_frame, bg="#FFFFFE")
        title_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Label(title_frame, 
                 text="User Management",background="#E3EDEF" ,font=("Arial", 18),
                 style="Header.TLabel").pack(side="left", anchor="w")
        
        refresh_btn = ttk.Button(title_frame, 
                               text="Update User",
                               style="TButton",
                               command=self.update_selected_user
                              )
        refresh_btn.pack(side="right", padx=5)

        refresh_btn = ttk.Button(title_frame, 
                               text="Add user",
                               style="TButton",
                               command=self.add_new_user)
        refresh_btn.pack(side="right", padx=5)

        add_user_btn = ttk.Button(title_frame, 
                               text="Refresh",
                               style="TButton",
                               command=self.display_all_users)
        add_user_btn.pack(side="right", padx=5)

        
        # User table frame
        table_frame = ttk.Frame(self.right_side_frame)
        table_frame.pack(fill='both', expand=True)
        
        # Create scrollbars
        self.scroll_y = ttk.Scrollbar(table_frame)
        self.scroll_y.pack(side='right', fill='y')
        
        self.scroll_x = ttk.Scrollbar(table_frame, orient='horizontal')
        self.scroll_x.pack(side='bottom', fill='x')


        

        # Create user table
        self.user_list_table = ttk.Treeview(
            table_frame,
            columns=('ID', 'Name', 'Email', 'Password', 'Calorie Goal', 'Role', 'Created'),
            yscrollcommand=self.scroll_y.set,
            xscrollcommand=self.scroll_x.set,
            selectmode='browse'
        )


                # Configure the scrollbar
        self.scroll_x.config(command=self.user_list_table.xview)
        self.scroll_y.config(command=self.user_list_table.yview)

                # Configure columns
        self.user_list_table.heading('#0', text='')
        self.user_list_table.heading('ID', text='ID', anchor='w')
        self.user_list_table.heading('Name', text='Name', anchor='w')
        self.user_list_table.heading('Email', text='Email', anchor='w')
        self.user_list_table.heading('Password', text='Password', anchor='w')
        self.user_list_table.heading('Calorie Goal', text='Calorie Goal', anchor='w')
        self.user_list_table.heading('Role', text='Role', anchor='w')
        self.user_list_table.heading('Created', text='Created', anchor='w')

        self.user_list_table.column('#0', width=0, stretch=False)
        self.user_list_table.column('ID', width=50, minwidth=50)
        self.user_list_table.column('Name', width=150, minwidth=100)
        self.user_list_table.column('Email', width=200, minwidth=150)
        self.user_list_table.column('Password', width=100, minwidth=80)
        self.user_list_table.column('Calorie Goal', width=100, minwidth=80)
        self.user_list_table.column('Role', width=80, minwidth=60)
        self.user_list_table.column('Created', width=120, minwidth=100)

        self.user_list_table.pack(fill='both', expand=True)
        

        def fetch_users():
            conn = connect_to_database()
            cursor = conn.cursor()
            query = "SELECT * FROM users"
            cursor.execute(query)
            data = cursor.fetchall()
            cursor.close()
            conn.close()
            return data 

        # Sample user data (replace with actual data from database)
        users = fetch_users()
        for user in users:
            self.user_list_table.insert('', 'end', values=(user[0], user[1], user[2],user[3],user[4],user[5],user[6]))

        

        self.user_action_frame = tk.Frame(self.right_side_frame, bg="#FFFFFE")
        self.user_action_frame.pack(side="bottom", fill="x", pady=10)


            # Add update button
        tk.Button(self.user_action_frame, text="Update User", bg="#4796BD", fg="white",
                 command=self.update_selected_user,font=("Arial", 10, "bold")).pack(side="left", padx=5)

        # Add delete button
        tk.Button(self.user_action_frame, text="Delete User", bg="#FF0000", fg="white",
                 command=self.delete_selected_user,font=("Arial", 10, "bold")).pack(side="left", padx=5)

    def delete_selected_user(self):
        selected_item = self.user_list_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a user to delete")
            return

        # Get the selected user's ID
        user_id = self.user_list_table.item(selected_item, 'values')[0]
        user_name = self.user_list_table.item(selected_item, 'values')[1]

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Delete", 
                                    f"Are you sure you want to delete {user_name} (ID: {user_id})?")

        if confirm:
            try:
                # Delete rows in water_intake table that reference the user's ID
                conn = connect_to_database()
                cursor = conn.cursor()
                query = "DELETE FROM water_intake WHERE user_id = %s"
                cursor.execute(query, (user_id,))

                # Delete rows in food_log table that reference the user's ID
                query = "DELETE FROM food_log WHERE user_id = %s"
                cursor.execute(query, (user_id,))

                # Delete the user from the users table
                query = "DELETE FROM users WHERE user_id = %s"
                cursor.execute(query, (user_id,))

                conn.commit()
                cursor.close()
                conn.close()

                messagebox.showinfo("Success", "User deleted successfully")
                self.display_all_users()  # Refresh the user list

            except Error as e:
                messagebox.showerror("Error", f"Failed to delete user: {e}")

    def update_selected_user(self):
        selected_item = self.user_list_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a user to update")
            return

        # Get the selected user's data
        user_data = self.user_list_table.item(selected_item, 'values')
        user_id = user_data[0]  # Get the user ID from the selected item

        # Clear existing widgets
        for widget in self.right_side_frame.winfo_children():
            widget.destroy()

        title_frame = tk.Frame(self.right_side_frame, bg="#FFFFFE")
        title_frame.pack(fill="x", pady=(0, 20))

        ttk.Label(title_frame, 
                text=f"Update User: {user_data[1]} (ID: {user_id})", 
                background="#E3EDEF",
                font=("Arial", 18),
                style="Header.TLabel").pack(side="left", anchor="w")
        
        refresh_btn = ttk.Button(title_frame, 
                            text="Back to Users",
                            style="TButton",
                            command=self.display_all_users)
        refresh_btn.pack(side="right", padx=5)

        # Create a frame to hold the input fields
        form_frame = tk.Frame(self.right_side_frame, bg="#FFFFFE")
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
            row_frame = tk.Frame(form_frame, bg="#FFFFFE")
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
        submit_btn = tk.Button(form_frame,
                            text="Update User",
                            bg="#4796BD",
                            command=lambda: self.submit_update_user(user_id))  # Pass user_id to submit
        submit_btn.pack(pady=20)

        self.load_user_for_editing(user_id)  # Pass user_id to load function

    def submit_update_user(self, user_id):
        # Get the current values from the form fields
        name = self.new_user_entry_vars["name"].get()
        email = self.new_user_entry_vars["email"].get()
        password = self.new_user_entry_vars["password"].get()
        calorie_goal = self.new_user_entry_vars["calorie_goal"].get()
        role = self.new_user_entry_vars["role"].get()

        # Validate
        if not all([name, email, calorie_goal, role]):
            messagebox.showwarning("Warning", "Please fill all required fields")
            return
        
        # Update database
        conn = connect_to_database()
        if conn:
            try:
                cursor = conn.cursor()
                
                if password:  # Only update password if it was changed (field isn't empty)
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

    def load_user_for_editing(self, user_id):
        conn = connect_to_database()
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()

        if user_data:
            # Clear existing entries first
            for entry in self.new_user_entry_vars.values():
                entry.delete(0, tk.END)  # Clear the entry
            
            # Populate the form fields with the user's data
            self.new_user_entry_vars["name"].insert(0, user_data[1])
            self.new_user_entry_vars["email"].insert(0, user_data[2])
            # Password field typically left empty for security
            self.new_user_entry_vars["calorie_goal"].insert(0, str(user_data[4]))
            self.new_user_entry_vars["role"].insert(0, user_data[5])

    def add_new_user(self):
        # Clear existing widgets
        for widget in self.right_side_frame.winfo_children():
            widget.destroy()

        title_frame = tk.Frame(self.right_side_frame, bg="#FFFFFE")
        title_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Label(title_frame, 
                 text="Add New User",background="#E3EDEF" ,font=("Arial", 18),
                 style="Header.TLabel").pack(side="left", anchor="w")
        
        refresh_btn = ttk.Button(title_frame, 
                               text="Back to Users",
                               style="TButton",
                               command=self.display_all_users)
        refresh_btn.pack(side="right", padx=5)
        


        # Create a frame to hold the input fields
        
        # Form frame
        form_frame = tk.Frame(self.right_side_frame, bg="#FFFFFE")
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
            row_frame = tk.Frame(form_frame, bg="#FFFFFE")
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
        submit_btn = tk.Button(form_frame,
                               text="Add User",
                               bg="#4796BD",
                               
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

    def submit_add_food_form(self):
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

    def add_new_food(self):
        # Clear content area

        for widget in self.right_side_frame.winfo_children():
            widget.destroy()
        
        # Title
        self.title_frame = tk.Frame(self.right_side_frame, bg="#FFFFFE")
        self.title_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Label(self.title_frame, 
                 text="Add New Food",style="TLabel", 
                 background="#4796BD").pack(side="left", anchor="w")

        # tk.Label(title_frame, text="Navigation Menu",bg="#4796BD", font=("Arial", 10, "bold")).pack(side="top", fill="x")
        # Back button
        tk.Button(self.title_frame, text="Back", font=("Arial", 10, "bold"),
                 command=self.display_all_foods).pack(side="right")
        
        # Form frame
        self.form_frame = tk.Frame(self.right_side_frame, bg="#FFFFFE")
        self.form_frame.pack(fill="both", expand=True, pady=20)
        
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
            row_frame = tk.Frame(self.form_frame, bg="#FFFFFE")
            row_frame.pack(fill="x", pady=5)
            
            ttk.Label(row_frame, 
                     text=label_text,
                     style="TLabel").pack(side="left", padx=(0, 10))
            
            entry = ttk.Entry(row_frame,
                            style="TEntry")
            entry.insert(0, default_value)
            entry.pack(side="right", fill="x", expand=True)
            
            self.new_food_entry_vars[field_name] = entry

        #  button to submit the form
        tk.Button(self.form_frame, bg="#4796BD", fg="white", text="Add Food", font=("Arial", 10, "bold"),
                   command=self.submit_add_food_form).pack(pady=20)

    def logout(self):
        self.root.destroy()
        self.main_app.on_dashboard_close()

    def on_close(self):
        """Handle window close event"""
        if messagebox.askokcancel("Quit", "Do you want to quit the application?"):
            self.logout()

# run app
if __name__ == "__main__":
    root = tk.Tk()
    app = Admin(root)
    root.mainloop()