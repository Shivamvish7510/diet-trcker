import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta


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


class User:
    def __init__(self, root,main_app,user_id=None):
        self.root = root
        self.main_app = main_app
        self.current_user_id = user_id
        
        self.root.title("Diet Tracker")
        self.root.geometry("800x600")
        try:
            self.root.wm_iconbitmap("food.ico")
        except:
            pass  # Handle case where icon file is missing
        self.root.config(bg="#E3EDEF")
        
                        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        root.config(bg="#E3EDEF")
        
        self.create_user_dashboard()

    # def initialize_database_tables(self):
    #     try:
    #         conn = connect_to_database()
    #         if conn:
    #             cursor = conn.cursor()
                
    #             # Check and create Diet_Plan table if needed
    #             cursor.execute("SHOW TABLES LIKE 'Diet_Plan'")
    #             if not cursor.fetchone():
    #                 cursor.execute("""
    #                     CREATE TABLE Diet_Plan (
    #                         plan_id INT AUTO_INCREMENT PRIMARY KEY,
    #                         user_id INT NOT NULL,
    #                         date DATE NOT NULL,
    #                         breakfast VARCHAR(255),
    #                         lunch VARCHAR(255),
    #                         dinner VARCHAR(255),
    #                         snacks VARCHAR(255),
    #                         FOREIGN KEY (user_id) REFERENCES Users(user_id),
    #                         UNIQUE KEY unique_user_date (user_id, date)
    #                     )
    #                 """)
                
    #             # Check and create Water_Intake table if needed
    #             cursor.execute("SHOW TABLES LIKE 'Water_Intake'")
    #             if not cursor.fetchone():
    #                 cursor.execute("""
    #                     CREATE TABLE Water_Intake (
    #                         intake_id INT AUTO_INCREMENT PRIMARY KEY,
    #                         user_id INT NOT NULL,
    #                         amount INT NOT NULL,
    #                         log_date DATETIME NOT NULL,
    #                         FOREIGN KEY (user_id) REFERENCES Users(user_id)
    #                     )
    #                 """)
                
    #             # Add daily_calorie_goal column if it doesn't exist
    #             cursor.execute("""
    #                 SELECT COLUMN_NAME 
    #                 FROM INFORMATION_SCHEMA.COLUMNS 
    #                 WHERE TABLE_NAME = 'Users' AND COLUMN_NAME = 'daily_calorie_goal'
    #             """)
    #             if not cursor.fetchone():
    #                 cursor.execute("ALTER TABLE Users ADD COLUMN daily_calorie_goal INT DEFAULT 2000")
                
    #             conn.commit()
    #             cursor.close()
    #             conn.close()
    #     except Error as e:
    #         messagebox.showerror("Error", f"Failed to initialize database tables: {e}")

    def create_user_dashboard(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Header
        header = tk.Frame(self.root, bg="#4796BD", height=50)
        header.pack(fill="x")
        tk.Label(header, bg="#4796BD", fg="white", text="User Dashboard", 
                font=("Arial", 18, "bold")).pack(pady=10, anchor="center")
        
        # Footer
        footer = tk.Frame(self.root, bg="#4796BD")  
        footer.pack(side="bottom", fill="both")
        tk.Label(footer, bg="#4796BD", fg="white", text="Shivam @ copyright").pack(anchor="center")
        
        # Left navigation menu
        nav_frame = tk.Frame(self.root, bg="#FFFFFE", bd=2)
        nav_frame.pack(side="left", fill="y", anchor="n", padx=(0, 50))

        # Navigation buttons
        tk.Label(nav_frame, text="Navigation Menu", bg="#4796BD", 
                font=("Arial", 10, "bold")).pack(fill="x", pady=5)
        
        buttons = [
            ("Dashboard", self.create_user_dashboard),
            ("Food Diary", self.food_diary),
            ("Diet Plan", self.diet_plan),
            ("Water Tracker", self.water_tracker),
            ("Food Table", self.display_all_foods)
        ]
        
        for text, command in buttons:
            tk.Button(nav_frame, text=text, font=("Arial", 10), 
                     command=command, anchor="w").pack(fill="x", pady=2)
            
        # logout botton    
        tk.Button(nav_frame, bg="#4796BD", fg="white", text="Log Out", font=("Arial", 10, "bold"), command=self.logout).pack(side="bottom", pady=5, fill="x")
        # Main content area
        self.content_frame = tk.Frame(self.root, bg="#F5F5F5")
        self.content_frame.pack(side="left", fill="both", expand=True)
        
        # Load dashboard content
        self.load_dashboard_content()

    def load_dashboard_content(self):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Main container
        container = tk.Frame(self.content_frame, bg="#F5F5F5", padx=20, pady=20)
        container.pack(fill="both", expand=True)

        # Stats row - create this first
        self.stats_frame = tk.Frame(container, bg="#F5F5F5")
        self.stats_frame.pack(fill="x", pady=(0, 20))

        # Now we can safely call get_total_calories()
        cal_frame = self.create_stat_card(self.stats_frame, "Calories Today", "0 / 2000 kcal")
        cal_frame.pack(side="left", fill="both", expand=True, padx=5)

        

       
       
        # Rest of your stats frames...
        rem_frame = self.create_stat_card(self.stats_frame, "Remaining Calories", "2000 kcal")
        rem_frame.pack(side="left", fill="both", expand=True, padx=5)
       
        self.update_calorie_display()

        # water_frame = self.create_stat_card(self.stats_frame, "Water Intake", "0 / 2000 ml")
        # water_frame.pack(side="left", fill="both", expand=True, padx=5)
        # self.update_water_intake()

        water_frame = self.create_stat_card(self.stats_frame, "Water Intake", "0 / 2000 ml")
        water_frame.pack(side="left", fill="both", expand=True, padx=5)
    
    # Store the value label as an instance variable
        for child in water_frame.winfo_children():
            if isinstance(child, tk.Label) and child.cget("text") == "Water Intake":
            # The value label is the second child (index 1)
                self.water_label = water_frame.winfo_children()[1]
                break
        
        self.update_water_intake()

        # Macros Today
        macros_frame = tk.Frame(self.stats_frame, bg="white", bd=1, relief="solid", padx=15, pady=15)
        macros_frame.pack(side="left", fill="both", expand=True, padx=5)
        tk.Label(macros_frame, text="Macros Today", bg="white", font=("Arial", 10, "bold")).pack(anchor="w")
        
        # Protein
        protein_frame = tk.Frame(macros_frame, bg="white")
        protein_frame.pack(fill="x", pady=2)
        tk.Label(protein_frame, text="Protein", bg="white", font=("Arial", 9)).pack(side="left")
        self.protein_label = tk.Label(protein_frame, text="0g", bg="white", font=("Arial", 9))
        self.protein_label.pack(side="right")

        # Carbs
        carbs_frame = tk.Frame(macros_frame, bg="white")
        carbs_frame.pack(fill="x", pady=2)
        tk.Label(carbs_frame, text="Carbs", bg="white", font=("Arial", 9)).pack(side="left")
        self.carbs_label = tk.Label(carbs_frame, text="0g", bg="white", font=("Arial", 9))
        self.carbs_label.pack(side="right")

        # Fat
        fat_frame = tk.Frame(macros_frame, bg="white")
        fat_frame.pack(fill="x", pady=2)
        tk.Label(fat_frame, text="Fat", bg="white", font=("Arial", 9)).pack(side="left")
        self.fat_label = tk.Label(fat_frame, text="0g", bg="white", font=("Arial", 9))
        self.fat_label.pack(side="right")

        # Meals section
        meals_frame = tk.Frame(container, bg="white", bd=1, relief="solid")
        meals_frame.pack(fill="both", expand=True, pady=(0, 20))

        # Meals header
        meals_header = tk.Frame(meals_frame, bg="#F5F5F5")
        meals_header.pack(fill="x", padx=10, pady=10)
        tk.Label(meals_header, text="Your Meals", bg="#F5F5F5", font=("Arial", 12, "bold")).pack(side="left")

        # Meals filter buttons
        filter_frame = tk.Frame(meals_header, bg="#F5F5F5")
        filter_frame.pack(side="right")
        for period in ["All", "Today", "Yesterday", "Week"]:
            tk.Button(filter_frame, text=period, font=("Arial", 8), 
                     command=lambda p=period: self.filter_meals(p)).pack(side="left", padx=2)

        # Meals list
        meals_content = tk.Frame(meals_frame, bg="white")
        meals_content.pack(fill="both", expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(meals_content)
        scrollbar.pack(side="right", fill="y")
        
        self.meals_listbox = tk.Listbox(meals_content, bg="white", bd=0, 
                                      yscrollcommand=scrollbar.set, height=6)
        self.meals_listbox.pack(fill="both", expand=True)
        scrollbar.config(command=self.meals_listbox.yview)
        
        self.meals_listbox.insert("end", "No meals found for the selected period.")
        self.meals_listbox.insert("end", "Add a meal to get started!")

        # Water tracker section
        water_frame = tk.Frame(container, bg="white", bd=1, relief="solid")
        water_frame.pack(fill="x")

        # Water header
        water_header = tk.Frame(water_frame, bg="#F5F5F5")
        water_header.pack(fill="x", padx=10, pady=10)
        tk.Label(water_header, text="Water Tracker", bg="#F5F5F5", font=("Arial", 12, "bold")).pack(side="left")
        tk.Label(water_header, text="Daily Goal: 2000ml", bg="#F5F5F5", font=("Arial", 9)).pack(side="right")

        # Water content
        water_content = tk.Frame(water_frame, bg="white")
        water_content.pack(fill="x", padx=10, pady=(0, 10))

        # Water progress
        water_progress = tk.Frame(water_content, bg="white")
        water_progress.pack(fill="x", pady=5)
        self.water_label = tk.Label(water_progress, text="0ml / 2000ml", bg="white", font=("Arial", 10))
        self.water_label.pack(side="left")

        # Water buttons
        water_buttons = tk.Frame(water_content, bg="white")
        water_buttons.pack(fill="x", pady=5)
        for amount in [50, 100, 250, 500]:
            tk.Button(water_buttons, text=f"{amount}ml", width=5,
                     command=lambda a=amount: self.add_water(a)).pack(side="left", padx=2)

        # Custom water entry
        custom_frame = tk.Frame(water_content, bg="white")
        custom_frame.pack(fill="x", pady=5)
        tk.Label(custom_frame, text="Custom Amount (ml)", bg="white", font=("Arial", 9)).pack(side="left")
        self.water_entry = tk.Entry(custom_frame, width=5)
        self.water_entry.pack(side="left", padx=5)
        self.water_entry.insert(0, "250")
        tk.Button(custom_frame, text="Add", width=5,
                 command=lambda: self.add_water(int(self.water_entry.get()))).pack(side="left")

        # Load actual data
        self.load_dashboard_data()

# calories

    def update_calorie_display(self):
        """Update the calorie display with current data"""
        try:
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                
                # Get total calories consumed today
                today = datetime.now().strftime('%Y-%m-%d')
                query = """SELECT SUM(f.calories_per_100g * fl.quantity / 100) 
                        FROM Food_Log fl 
                        JOIN Foods f ON fl.food_id = f.food_id 
                        WHERE fl.user_id = %s AND DATE(fl.log_date) = %s"""
                cursor.execute(query, (self.current_user_id, today))
                result = cursor.fetchone()
                total_calories = result[0] if result[0] else 0
                
                # Get daily goal
                daily_goal = self.get_daily_calorie_goal()
                
                # Update the labels using our stored references
                if hasattr(self, 'stat_labels'):
                    if 'Calories Today' in self.stat_labels:
                        self.stat_labels['Calories Today'].config(text=f"{total_calories:.0f} / {daily_goal} kcal")
                    if 'Remaining Calories' in self.stat_labels:
                        remaining = max(0, daily_goal - total_calories)
                        self.stat_labels['Remaining Calories'].config(text=f"{remaining:.0f} kcal")
                
                cursor.close()
                conn.close()
        except Error as e:
            messagebox.showerror("Error", f"Failed to update calorie display: {e}")


    def get_daily_calorie_goal(self):
        """Get the user's daily calorie goal from database"""
        try:
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT daily_calorie_goal FROM Users WHERE user_id = %s",
                            (self.current_user_id,))
                result = cursor.fetchone()
                cursor.close()
                conn.close()
                return result[0] if result and result[0] else 2000  # Default to 2000
        except Error as e:
            messagebox.showerror("Error", f"Failed to get calorie goal: {e}")
            return 2000

    def update_water_intake(self):
        """Update the water intake display with current data"""
        try:
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                
                # Get today's date
                today = datetime.now().strftime('%Y-%m-%d')
                
                # Get total water consumed today
                cursor.execute("""SELECT SUM(amount) 
                            FROM Water_Intake 
                            WHERE user_id = %s AND DATE(log_date) = %s""",
                            (self.current_user_id, today))
                water_result = cursor.fetchone()
                water = water_result[0] if water_result and water_result[0] else 0
                
                # Update the water label
                self.water_label.config(text=f"{water} / 2000 ml")
                
                cursor.close()
                conn.close()
        except Error as e:
            messagebox.showerror("Error", f"Failed to update water intake: {e}")

    def add_water(self, amount):
        try:
            if not isinstance(amount, int) or amount <= 0:
                messagebox.showerror("Error", "Please enter a valid positive number")
                return
                
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""INSERT INTO Water_Intake 
                            (user_id, amount, log_date) 
                            VALUES (%s, %s, NOW())""",
                            (self.current_user_id, amount))
                conn.commit()
                cursor.close()
                conn.close()
                self.update_water_intake()  # Update the display
        except Error as e:
            messagebox.showerror("Error", f"Failed to record water intake: {e}")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")

    def create_stat_card(self, parent, title, initial_value):
        frame = tk.Frame(parent, bg="white", bd=1, relief="solid", padx=15, pady=15)
        tk.Label(frame, text=title, bg="white", font=("Arial", 10, "bold")).pack(anchor="w")
        label = tk.Label(frame, text=initial_value, bg="white", font=("Arial", 14))
        label.pack(anchor="w", pady=(5, 0))
        
        # Store references to the labels using the title as key
        if not hasattr(self, 'stat_labels'):
            self.stat_labels = {}
        self.stat_labels[title] = label
        
        return frame

    def load_dashboard_data(self):
        try:
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                
                # Get today's date
                today = datetime.now().strftime('%Y-%m-%d')
                
                # Get user's daily calorie goal
                cursor.execute("SELECT daily_calorie_goal FROM Users WHERE user_id = %s",
                             (self.current_user_id,))
                goal_result = cursor.fetchone()
                daily_goal = goal_result[0] if goal_result and goal_result[0] else 2000
                
                # Get calories consumed today
                cursor.execute("""SELECT 
                              SUM(calories_per_100g * quantity / 100) as calories,
                              SUM(protein_per_100g * quantity / 100) as protein,
                              SUM(carbs_per_100g * quantity / 100) as carbs,
                              SUM(fat_per_100g * quantity / 100) as fat
                              FROM Food_Log 
                              JOIN Foods ON Food_Log.food_id = Foods.food_id 
                              WHERE user_id = %s AND DATE(log_date) = %s""",
                              (self.current_user_id, today))
                nutrition = cursor.fetchone()
                
                calories = nutrition[0] if nutrition and nutrition[0] else 0
                protein = nutrition[1] if nutrition and nutrition[1] else 0
                carbs = nutrition[2] if nutrition and nutrition[2] else 0
                fat = nutrition[3] if nutrition and nutrition[3] else 0
                
                # Update labels
                for widget in self.content_frame.winfo_children():
                    if isinstance(widget, tk.Frame):
                        for child in widget.winfo_children():
                            if isinstance(child, tk.Frame):
                                for label in child.winfo_children():
                                    if isinstance(label, tk.Label) and label.cget("text") == "Calories Today":
                                        label.master.children['!label2'].config(text=f"{calories:.0f} / {daily_goal} kcal")
                                    elif isinstance(label, tk.Label) and label.cget("text") == "Remaining Calories":
                                        label.master.children['!label2'].config(text=f"{max(0, daily_goal - calories):.0f} kcal")
                
                # Update macros
                self.protein_label.config(text=f"{protein:.0f}g")
                self.carbs_label.config(text=f"{carbs:.0f}g")
                self.fat_label.config(text=f"{fat:.0f}g")
                
                # Get water intake
                cursor.execute("""SELECT SUM(amount) 
                              FROM Water_Intake 
                              WHERE user_id = %s AND DATE(log_date) = %s""",
                              (self.current_user_id, today))
                water_result = cursor.fetchone()
                water = water_result[0] if water_result and water_result[0] else 0
                
                # Update water label
                for widget in self.content_frame.winfo_children():
                    if isinstance(widget, tk.Frame):
                        for child in widget.winfo_children():
                            if isinstance(child, tk.Frame):
                                for label in child.winfo_children():
                                    if isinstance(label, tk.Label) and label.cget("text") == "Water Intake":
                                        label.master.children['!label2'].config(text=f"{water} / 2000 ml")
                
                # Get today's meals
                self.filter_meals("Today")
                
                cursor.close()
                conn.close()
                
        except Error as e:
            messagebox.showerror("Error", f"Failed to load dashboard data: {e}")

    def filter_meals(self, period):
        try:
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                
                today = datetime.now().date()
                query = """SELECT Foods.name, quantity, log_date 
                          FROM Food_Log 
                          JOIN Foods ON Food_Log.food_id = Foods.food_id 
                          WHERE user_id = %s"""
                params = [self.current_user_id]
                
                if period == "Today":
                    query += " AND DATE(log_date) = %s"
                    params.append(today.strftime('%Y-%m-%d'))
                elif period == "Yesterday":
                    yesterday = today - timedelta(days=1)
                    query += " AND DATE(log_date) = %s"
                    params.append(yesterday.strftime('%Y-%m-%d'))
                elif period == "Week":
                    start_of_week = today - timedelta(days=today.weekday())
                    query += " AND DATE(log_date) BETWEEN %s AND %s"
                    params.extend([start_of_week.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d')])
                
                query += " ORDER BY log_date"
                
                cursor.execute(query, tuple(params))
                meals = cursor.fetchall()
                
                self.meals_listbox.delete(0, "end")
                if meals:
                    for meal in meals:
                        time_str = meal[2].strftime('%H:%M') if hasattr(meal[2], 'strftime') else meal[2]
                        self.meals_listbox.insert("end", f"{meal[0]} - {meal[1]}g at {time_str}")
                else:
                    self.meals_listbox.insert("end", f"No meals found for {period.lower()}.")
                    self.meals_listbox.insert("end", "Add a meal to get started!")
                
                cursor.close()
                conn.close()
        except Error as e:
            messagebox.showerror("Error", f"Failed to filter meals: {e}")

    def add_water(self, amount):
        try:
            if not isinstance(amount, int) or amount <= 0:
                messagebox.showerror("Error", "Please enter a valid positive number")
                return
                
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""INSERT INTO Water_Intake 
                              (user_id, amount, log_date) 
                              VALUES (%s, %s, NOW())""",
                              (self.current_user_id, amount))
                conn.commit()
                cursor.close()
                conn.close()
                self.load_dashboard_data()  # Refresh the display
        except Error as e:
            messagebox.showerror("Error", f"Failed to record water intake: {e}")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")

    def food_diary(self):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        tk.Label(self.content_frame, text="Food Diary", font=("Arial", 18, "bold")).pack(pady=10)

        # Create a frame for the treeview and scrollbar
        tree_frame = tk.Frame(self.content_frame)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Create a treeview with scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")

        self.food_tree = ttk.Treeview(tree_frame, yscrollcommand=scrollbar.set)
        self.food_tree['columns'] = ('Date', 'Food', 'Quantity', 'Calories')

        self.food_tree.column("#0", width=0, stretch=tk.NO)
        self.food_tree.column("Date", anchor=tk.W, width=100)
        self.food_tree.column("Food", anchor=tk.W, width=150)
        self.food_tree.column("Quantity", anchor=tk.W, width=100)
        self.food_tree.column("Calories", anchor=tk.W, width=100)

        self.food_tree.heading("#0", text="", anchor=tk.W)
        self.food_tree.heading("Date", text="Date", anchor=tk.W)
        self.food_tree.heading("Food", text="Food", anchor=tk.W)
        self.food_tree.heading("Quantity", text="Quantity (g)", anchor=tk.W)
        self.food_tree.heading("Calories", text="Calories", anchor=tk.W)

        self.load_food_logs()

        self.food_tree.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.food_tree.yview)

        # Create a frame for buttons
        button_frame = tk.Frame(self.content_frame)
        button_frame.pack(pady=10)

        # Create buttons
        tk.Button(button_frame, text="Add New Food Log", command=self.add_food_log).pack(side="left", padx=5)
        tk.Button(button_frame, text="Delete Food Log", command=self.delete_food_log).pack(side="left", padx=5)
        tk.Button(button_frame, text="Update Food Log", command=self.update_food_log).pack(side="left", padx=5)

    def load_food_logs(self):
        try:
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                query = """SELECT log_id, log_date, name, quantity, 
                          calories_per_100g * quantity / 100 AS total_calories 
                          FROM Food_Log 
                          INNER JOIN Foods ON Food_Log.food_id = Foods.food_id 
                          WHERE user_id = %s
                          ORDER BY log_date DESC"""
                cursor.execute(query, (self.current_user_id,))
                results = cursor.fetchall()

                self.food_tree.delete(*self.food_tree.get_children())
                for row in results:
                    self.food_tree.insert('', 'end', values=row[1:], iid=row[0])

                cursor.close()
                conn.close()
        except Error as e:
            messagebox.showerror("Error", f"Failed to get food diary: {e}")

    def add_food_log(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Food Log")
        add_window.geometry("300x250")

        tk.Label(add_window, text="Food Name:").pack()
        food_name_entry = tk.Entry(add_window)
        food_name_entry.pack()

        tk.Label(add_window, text="Quantity (grams):").pack()
        quantity_entry = tk.Entry(add_window)
        quantity_entry.pack()

        tk.Label(add_window, text="Date (YYYY-MM-DD):").pack()
        date_entry = tk.Entry(add_window)
        date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        date_entry.pack()

        def save_food_log():
            try:
                food_name = food_name_entry.get()
                quantity = float(quantity_entry.get())
                date = date_entry.get()
                
                food_id = self.get_food_id(food_name)
                if food_id is None:
                    messagebox.showerror("Error", "Food not found")
                    return

                conn = connect_to_database()
                if conn:
                    cursor = conn.cursor()
                    query = """INSERT INTO Food_Log 
                              (user_id, food_id, quantity, log_date) 
                              VALUES (%s, %s, %s, %s)"""
                    cursor.execute(query, (self.current_user_id, food_id, quantity, date))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    
                    messagebox.showinfo("Success", "Food log added successfully")
                    add_window.destroy()
                    self.load_food_logs()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers")
            except Error as e:
                messagebox.showerror("Error", f"Failed to add food log: {e}")

        tk.Button(add_window, text="Save", command=save_food_log).pack(pady=10)

    def delete_food_log(self):
        selected = self.food_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a food log to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this food log?"):
            try:
                conn = connect_to_database()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM Food_Log WHERE log_id = %s", (selected[0],))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    
                    messagebox.showinfo("Success", "Food log deleted successfully")
                    self.load_food_logs()
            except Error as e:
                messagebox.showerror("Error", f"Failed to delete food log: {e}")

    def update_food_log(self):
        selected = self.food_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a food log to update")
            return
        
        log_id = selected[0]
        values = self.food_tree.item(log_id, 'values')
        
        update_window = tk.Toplevel(self.root)
        update_window.title("Update Food Log")
        update_window.geometry("300x300")

        tk.Label(update_window, text="Food Name:").pack()
        food_name_entry = tk.Entry(update_window)
        food_name_entry.insert(0, values[1])
        food_name_entry.pack()

        tk.Label(update_window, text="Quantity (grams):").pack()
        quantity_entry = tk.Entry(update_window)
        quantity_entry.insert(0, values[2])
        quantity_entry.pack()

        tk.Label(update_window, text="Date (YYYY-MM-DD):").pack()
        date_entry = tk.Entry(update_window)
        date_entry.insert(0, values[0])
        date_entry.pack()

        def save_update():
            try:
                food_name = food_name_entry.get()
                quantity = float(quantity_entry.get())
                date = date_entry.get()
                
                food_id = self.get_food_id(food_name)
                if food_id is None:
                    messagebox.showerror("Error", "Food not found")
                    return

                conn = connect_to_database()
                if conn:
                    cursor = conn.cursor()
                    query = """UPDATE Food_Log 
                              SET food_id = %s, quantity = %s, log_date = %s 
                              WHERE log_id = %s"""
                    cursor.execute(query, (food_id, quantity, date, log_id))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    
                    messagebox.showinfo("Success", "Food log updated successfully")
                    update_window.destroy()
                    self.load_food_logs()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers")
            except Error as e:
                messagebox.showerror("Error", f"Failed to update food log: {e}")

        tk.Button(update_window, text="Update", command=save_update).pack(pady=10)

    def get_food_id(self, food_name):
        try:
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT food_id FROM Foods WHERE name = %s", (food_name,))
                result = cursor.fetchone()
                cursor.close()
                conn.close()
                return result[0] if result else None
        except Error as e:
            messagebox.showerror("Error", f"Failed to get food ID: {e}")
            return None

    def diet_plan(self):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        tk.Label(self.content_frame, text="Diet Plan", font=("Arial", 18, "bold")).pack(pady=10)

        # Create a frame for the treeview and scrollbar
        tree_frame = tk.Frame(self.content_frame)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Create a treeview with scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")

        self.diet_tree = ttk.Treeview(tree_frame, yscrollcommand=scrollbar.set)
        self.diet_tree['columns'] = ('Date', 'Breakfast', 'Lunch', 'Dinner', 'Snacks')

        self.diet_tree.column("#0", width=0, stretch=tk.NO)
        self.diet_tree.column("Date", anchor=tk.W, width=100)
        self.diet_tree.column("Breakfast", anchor=tk.W, width=150)
        self.diet_tree.column("Lunch", anchor=tk.W, width=150)
        self.diet_tree.column("Dinner", anchor=tk.W, width=150)
        self.diet_tree.column("Snacks", anchor=tk.W, width=150)

        self.diet_tree.heading("#0", text="", anchor=tk.W)
        self.diet_tree.heading("Date", text="Date", anchor=tk.W)
        self.diet_tree.heading("Breakfast", text="Breakfast", anchor=tk.W)
        self.diet_tree.heading("Lunch", text="Lunch", anchor=tk.W)
        self.diet_tree.heading("Dinner", text="Dinner", anchor=tk.W)
        self.diet_tree.heading("Snacks", text="Snacks", anchor=tk.W)

        self.load_diet_plans()

        self.diet_tree.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.diet_tree.yview)

        # Create a frame for buttons
        button_frame = tk.Frame(self.content_frame)
        button_frame.pack(pady=10)

        # Create buttons
        tk.Button(button_frame, text="Add New Plan", command=self.add_diet_plan).pack(side="left", padx=5)
        tk.Button(button_frame, text="Update Plan", command=self.update_diet_plan).pack(side="left", padx=5)
        tk.Button(button_frame, text="Delete Plan", command=self.delete_diet_plan).pack(side="left", padx=5)

    def load_diet_plans(self):
        try:
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""SELECT plan_id, date, breakfast, lunch, dinner, snacks 
                              FROM Diet_Plan 
                              WHERE user_id = %s
                              ORDER BY date DESC""",
                              (self.current_user_id,))
                results = cursor.fetchall()

                self.diet_tree.delete(*self.diet_tree.get_children())
                for row in results:
                    self.diet_tree.insert('', 'end', values=row[1:], iid=row[0])

                cursor.close()
                conn.close()
        except Error as e:
            messagebox.showerror("Error", f"Failed to get diet plans: {e}")

    def add_diet_plan(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Diet Plan")
        add_window.geometry("300x350")

        tk.Label(add_window, text="Date (YYYY-MM-DD):").pack()
        date_entry = tk.Entry(add_window)
        date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        date_entry.pack()

        tk.Label(add_window, text="Breakfast:").pack()
        breakfast_entry = tk.Entry(add_window)
        breakfast_entry.pack()

        tk.Label(add_window, text="Lunch:").pack()
        lunch_entry = tk.Entry(add_window)
        lunch_entry.pack()

        tk.Label(add_window, text="Dinner:").pack()
        dinner_entry = tk.Entry(add_window)
        dinner_entry.pack()

        tk.Label(add_window, text="Snacks:").pack()
        snacks_entry = tk.Entry(add_window)
        snacks_entry.pack()

        def save_diet_plan():
            try:
                date = date_entry.get()
                breakfast = breakfast_entry.get()
                lunch = lunch_entry.get()
                dinner = dinner_entry.get()
                snacks = snacks_entry.get()

                conn = connect_to_database()
                if conn:
                    cursor = conn.cursor()
                    query = """INSERT INTO Diet_Plan 
                              (user_id, date, breakfast, lunch, dinner, snacks) 
                              VALUES (%s, %s, %s, %s, %s, %s)"""
                    cursor.execute(query, (self.current_user_id, date, breakfast, lunch, dinner, snacks))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    
                    messagebox.showinfo("Success", "Diet plan added successfully")
                    add_window.destroy()
                    self.load_diet_plans()
            except Error as e:
                messagebox.showerror("Error", f"Failed to add diet plan: {e}")

        tk.Button(add_window, text="Save", command=save_diet_plan).pack(pady=10)

    def update_diet_plan(self):
        selected = self.diet_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a diet plan to update")
            return
        
        plan_id = selected[0]
        values = self.diet_tree.item(plan_id, 'values')
        
        update_window = tk.Toplevel(self.root)
        update_window.title("Update Diet Plan")
        update_window.geometry("300x350")

        tk.Label(update_window, text="Date (YYYY-MM-DD):").pack()
        date_entry = tk.Entry(update_window)
        date_entry.insert(0, values[0])
        date_entry.pack()

        tk.Label(update_window, text="Breakfast:").pack()
        breakfast_entry = tk.Entry(update_window)
        breakfast_entry.insert(0, values[1] if values[1] else "")
        breakfast_entry.pack()

        tk.Label(update_window, text="Lunch:").pack()
        lunch_entry = tk.Entry(update_window)
        lunch_entry.insert(0, values[2] if values[2] else "")
        lunch_entry.pack()

        tk.Label(update_window, text="Dinner:").pack()
        dinner_entry = tk.Entry(update_window)
        dinner_entry.insert(0, values[3] if values[3] else "")
        dinner_entry.pack()

        tk.Label(update_window, text="Snacks:").pack()
        snacks_entry = tk.Entry(update_window)
        snacks_entry.insert(0, values[4] if values[4] else "")
        snacks_entry.pack()

        def save_update():
            try:
                date = date_entry.get()
                breakfast = breakfast_entry.get()
                lunch = lunch_entry.get()
                dinner = dinner_entry.get()
                snacks = snacks_entry.get()

                conn = connect_to_database()
                if conn:
                    cursor = conn.cursor()
                    query = """UPDATE Diet_Plan 
                              SET date = %s, breakfast = %s, lunch = %s, 
                                  dinner = %s, snacks = %s
                              WHERE plan_id = %s"""
                    cursor.execute(query, (date, breakfast, lunch, dinner, snacks, plan_id))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    
                    messagebox.showinfo("Success", "Diet plan updated successfully")
                    update_window.destroy()
                    self.load_diet_plans()
            except Error as e:
                messagebox.showerror("Error", f"Failed to update diet plan: {e}")

        tk.Button(update_window, text="Update", command=save_update).pack(pady=10)

    def delete_diet_plan(self):
        selected = self.diet_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a diet plan to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this diet plan?"):
            try:
                conn = connect_to_database()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM Diet_Plan WHERE plan_id = %s", (selected[0],))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    
                    messagebox.showinfo("Success", "Diet plan deleted successfully")
                    self.load_diet_plans()
            except Error as e:
                messagebox.showerror("Error", f"Failed to delete diet plan: {e}")


    def display_all_foods(self):
            # Clear existing widgets
            for widget in self.content_frame.winfo_children():
                widget.destroy()

            # Create a frame to hold the food list
            self.food_list_frame = tk.Frame(self.content_frame, bg="#FFFFFE")
            self.food_list_frame.pack(side="top", fill="both", expand=True)

            # Create a scrollbar
            self.scrollbar = tk.Scrollbar(self.food_list_frame)
            self.scrollbar.pack(side="right", fill="y")

            # Create a table to display the food list
            self.food_list_table = ttk.Treeview(self.food_list_frame, yscrollcommand=self.scrollbar.set)
            self.food_list_table.pack(side="left", fill="both", expand=True)

            # Configure the scrollbar
            self.scrollbar.config(command=self.food_list_table.yview)

            # Define the columns
            self.food_list_table['columns'] = ('Food ID', 'Food Name', 'Calories', 'Portion','Fat','carbohydrates')

            # Format the columns
            self.food_list_table.column("#0", width=0, stretch=tk.NO)
            self.food_list_table.column("Food ID", anchor=tk.W, width=50)
            self.food_list_table.column("Food Name", anchor=tk.W, width=150)
            self.food_list_table.column("Calories", anchor=tk.W, width=50)
            self.food_list_table.column("Portion", anchor=tk.W, width=50)
            self.food_list_table.column("Fat", anchor=tk.W, width=50)
            self.food_list_table.column("carbohydrates", anchor=tk.W, width=50)

            # Create the headings
            self.food_list_table.heading("#0", text="", anchor=tk.W)
            self.food_list_table.heading("Food ID", text="Food ID", anchor=tk.W)
            self.food_list_table.heading("Food Name", text="Food Name", anchor=tk.W)
            self.food_list_table.heading("Calories", text="Calories", anchor=tk.W)
            self.food_list_table.heading("Portion", text="Portion", anchor=tk.W)
            self.food_list_table.heading("Fat", text="Fat", anchor=tk.W)
            self.food_list_table.heading("carbohydrates", text="carbohydrates", anchor=tk.W)

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
                self.food_list_table.insert('', 'end', values=(food[0], food[1], food[2], food[3] ,food[4] ,food[5] ))
   
            tk.Button(self.content_frame,text="add to food diary",command=self.add_to_food_diary).pack(side="bottom",padx=10,pady=10)


    def add_to_food_diary(self):
        # Get the selected food item
        selected = self.food_list_table.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a food item to add to your diary")
            return

        # Get the food item details
        food_id = self.food_list_table.item(selected, 'values')[0]
        food_name = self.food_list_table.item(selected, 'values')[1]
        calories = self.food_list_table.item(selected, 'values')[2]
        portion = self.food_list_table.item(selected, 'values')[3]
        fat = self.food_list_table.item(selected, 'values')[4]
        carbohydrates = self.food_list_table.item(selected, 'values')[5]

        # Create a new window to input quantity and date
        add_window = tk.Toplevel(self.root)
        add_window.title("Add to Food Diary")
        add_window.geometry("300x200")

        tk.Label(add_window, text="Food Name:").pack()
        tk.Label(add_window, text=food_name).pack()

        tk.Label(add_window, text="Quantity (grams):").pack()
        quantity_entry = tk.Entry(add_window)
        quantity_entry.pack()

        tk.Label(add_window, text="Date (YYYY-MM-DD):").pack()
        date_entry = tk.Entry(add_window)
        date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        date_entry.pack()


        def save_food_diary():
            try:
                quantity = float(quantity_entry.get())
                date = date_entry.get()

                conn = connect_to_database()
                if conn:
                    cursor = conn.cursor()
                    query = """INSERT INTO Food_Log 
                            (user_id, food_id, quantity, log_date) 
                            VALUES (%s, %s, %s, %s)"""
                    cursor.execute(query, (self.current_user_id, food_id, quantity, date))
                    conn.commit()
                    cursor.close()
                    conn.close()

                    messagebox.showinfo("Success", "Food diary entry added successfully")
                    add_window.destroy()
                    self.create_user_dashboard()  # Call create_user_dashboard instead of load_dashboard_data
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers")
            except Error as e:
                messagebox.showerror("Error", f"Failed to add food diary entry: {e}")

        tk.Button(add_window, text="Save", command=save_food_diary).pack(pady=10)




    def water_tracker(self):
        # This is already implemented in the dashboard
        self.create_user_dashboard()

    def logout(self):
        self.root.destroy()
        
        self.main_app.on_dashboard_close()

    def on_close(self):
        """Handle window close event"""
        if messagebox.askokcancel("Quit", "Do you want to quit the application?"):
            self.logout()

if __name__ == "__main__":
    root = tk.Tk()
    app = User(root)  # Pass the user_id here
    root.mainloop()
