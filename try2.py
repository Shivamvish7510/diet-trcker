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
class User:
    def __init__(self, root):
        self.root = root
        
        self.root.title("Diet Tracker")
        self.root.geometry("800x600")  # Increased size for better layout
        root.wm_iconbitmap("food.ico")
        self.create_user_dashboard()
        root.config(bg="#E3EDEF")
        self.current_user_id = 1  # Default user ID, should be set during login

    def create_user_dashboard(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Header
        self.user = tk.Frame(self.root, bg="#4796BD", height=50)
        self.user.pack(fill="x")
        tk.Label(self.user, bg="#4796BD", fg="white", text="user Dashboard", font=("Arial", 18, "bold")).pack(pady=10, anchor="center")
        
        # Footer
        self.footer = tk.Frame(self.root, bg="#4796BD")  
        self.footer.pack(side="bottom", fill="both")
        tk.Label(self.footer, bg="#4796BD", fg="white", text="shivam copyright ").pack(anchor="center")
        
        # admin dashboard frame
        self.dashboard = tk.Frame(self.root, bg="#FFFFFE", bd=2)
        self.dashboard.pack(side="left", fill="y", anchor="n", padx=(0, 50))

        # Navigation Menu
        self.navigation_menu = tk.Frame(self.dashboard, bg="#FFFFFE")
        self.navigation_menu.pack(side="top", fill="both", expand=True)

        # Menu buttons frame
        self.menu_buttons_frame = tk.Frame(self.navigation_menu, bg="#FFFFFE")
        self.menu_buttons_frame.pack(side="top", fill="x")

        tk.Label(self.menu_buttons_frame, text="Navigation Menu", bg="#4796BD", font=("Arial", 10, "bold")).pack(side="top", fill="x")
        tk.Button(self.menu_buttons_frame, text="Dashboard", font=("Arial", 10), command=self.create_user_dashboard).pack(side="top", fill="x")
        tk.Button(self.menu_buttons_frame, text="Food Diary", command=self.food_diary, font=("Arial", 10)).pack(side="top", fill="x")
        tk.Button(self.menu_buttons_frame, text="Diet Plan", command=self.diet_plan, font=("Arial", 10)).pack(side="top", fill="x")
        tk.Button(self.menu_buttons_frame, text="food table", command=self.display_all_foods, font=("Arial", 10)).pack(side="top", fill="x")

        # Login button frame
        self.login_button_frame = tk.Frame(self.navigation_menu, bg="#FFFFFE")
        self.login_button_frame.pack(side="bottom", fill="x")

        tk.Button(self.login_button_frame, bg="#4796BD", fg="white", text="Log Out", font=("Arial", 10, "bold"), command=self.logout).pack(side="bottom", pady=5, fill="x")

        # Dashboard Statistics
        self.right_side_frame = tk.Frame(self.root, bg="#FFFFFE", bd=2, width=400, height=500)
        self.right_side_frame.pack(side="left", fill="both", expand=True, anchor="ne")

        tk.Label(self.right_side_frame, text="Dashboard Statistics", font=("Arial", 10, "bold")).pack(side="top", fill="x")
        self.display_total_users()
        self.display_total_foods()

    def display_total_users(self):
        try:
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                query = "SELECT COUNT(*) FROM users"
                cursor.execute(query)
                total_users = cursor.fetchone()[0]
                cursor.close()
                conn.close()
                tk.Label(self.right_side_frame, text=f"Total Users: {total_users}", font=("Arial", 10)).pack(side="top", fill="x")
        except Error as e:
            messagebox.showerror("Error", f"Failed to get user count: {e}")

    def display_total_foods(self):
        try:
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                query = "SELECT COUNT(*) FROM foods"
                cursor.execute(query)
                total_foods = cursor.fetchone()[0]
                cursor.close()
                conn.close()
                tk.Label(self.right_side_frame, text=f"Total Foods: {total_foods}", font=("Arial", 10)).pack(side="top", fill="x")
        except Error as e:
            messagebox.showerror("Error", f"Failed to get food count: {e}")

    def food_diary(self):
        # Clear existing widgets in right side frame
        for widget in self.right_side_frame.winfo_children():
            widget.destroy()

        tk.Label(self.right_side_frame, text="Food Diary", font=("Arial", 18, "bold")).pack(pady=10)

        # Create a frame for the treeview and scrollbar
        tree_frame = tk.Frame(self.right_side_frame)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Create a treeview with scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")

        tree = ttk.Treeview(tree_frame, yscrollcommand=scrollbar.set)
        tree['columns'] = ('Date', 'Food', 'Quantity', 'Calories')

        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("Date", anchor=tk.W, width=100)
        tree.column("Food", anchor=tk.W, width=150)
        tree.column("Quantity", anchor=tk.W, width=100)
        tree.column("Calories", anchor=tk.W, width=100)

        tree.heading("#0", text="", anchor=tk.W)
        tree.heading("Date", text="Date", anchor=tk.W)
        tree.heading("Food", text="Food", anchor=tk.W)
        tree.heading("Quantity", text="Quantity (g)", anchor=tk.W)
        tree.heading("Calories", text="Calories", anchor=tk.W)

        try:
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                query = """SELECT log_date, name, quantity, 
                          calories_per_100g * quantity / 100 AS total_calories 
                          FROM Food_Log 
                          INNER JOIN Foods ON Food_Log.food_id = Foods.food_id 
                          WHERE user_id = %s"""
                cursor.execute(query, (self.current_user_id,))
                results = cursor.fetchall()

                for row in results:
                    tree.insert('', 'end', values=row)

                cursor.close()
                conn.close()
        except Error as e:
            messagebox.showerror("Error", f"Failed to get food diary: {e}")

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=tree.yview)

        # Create a frame for buttons
        button_frame = tk.Frame(self.right_side_frame)
        button_frame.pack(pady=10)

        # Create buttons
        add_food_log_button = tk.Button(button_frame, text="Add New Food Log", command=self.add_food_log)
        add_food_log_button.pack(side="left", padx=5)

        delete_food_log_button = tk.Button(button_frame, text="Delete Food Log", command=self.delete_food_log)
        delete_food_log_button.pack(side="left", padx=5)

        update_food_log_button = tk.Button(button_frame, text="Update Food Log", command=self.update_food_log)
        update_food_log_button.pack(side="left", padx=5)

    def add_food_log(self):
        add_food_log_window = tk.Toplevel(self.root)
        add_food_log_window.title("Add New Food Log")
        add_food_log_window.geometry("300x250")

        tk.Label(add_food_log_window, text="User ID:").pack()
        user_id_entry = tk.Entry(add_food_log_window)
        user_id_entry.insert(0, str(self.current_user_id))
        user_id_entry.pack()

        tk.Label(add_food_log_window, text="Food Name:").pack()
        food_name_entry = tk.Entry(add_food_log_window)
        food_name_entry.pack()

        tk.Label(add_food_log_window, text="Quantity (grams):").pack()
        quantity_entry = tk.Entry(add_food_log_window)
        quantity_entry.pack()

        tk.Label(add_food_log_window, text="Date (YYYY-MM-DD):").pack()
        date_entry = tk.Entry(add_food_log_window)
        date_entry.pack()

        add_button = tk.Button(add_food_log_window, text="Add", 
                             command=lambda: [
                                 self.add_food_log_to_database(
                                     user_id_entry.get(), 
                                     food_name_entry.get(), 
                                     quantity_entry.get(), 
                                     date_entry.get()
                                 ),
                                 add_food_log_window.destroy()
                             ])
        add_button.pack(pady=10)

    def delete_food_log(self):
        delete_food_log_window = tk.Toplevel(self.root)
        delete_food_log_window.title("Delete Food Log")
        delete_food_log_window.geometry("300x150")

        tk.Label(delete_food_log_window, text="Food Log ID:").pack()
        food_log_id_entry = tk.Entry(delete_food_log_window)
        food_log_id_entry.pack()

        delete_button = tk.Button(delete_food_log_window, text="Delete", 
                                command=lambda: [
                                    self.delete_food_log_from_database(food_log_id_entry.get()),
                                    delete_food_log_window.destroy()
                                ])
        delete_button.pack(pady=10)

    def update_food_log(self):
        update_food_log_window = tk.Toplevel(self.root)
        update_food_log_window.title("Update Food Log")
        update_food_log_window.geometry("300x300")

        tk.Label(update_food_log_window, text="Food Log ID:").pack()
        food_log_id_entry = tk.Entry(update_food_log_window)
        food_log_id_entry.pack()

        tk.Label(update_food_log_window, text="New Food Name:").pack()
        new_food_name_entry = tk.Entry(update_food_log_window)
        new_food_name_entry.pack()

        tk.Label(update_food_log_window, text="New Quantity (grams):").pack()
        new_quantity_entry = tk.Entry(update_food_log_window)
        new_quantity_entry.pack()

        tk.Label(update_food_log_window, text="New Date (YYYY-MM-DD):").pack()
        new_date_entry = tk.Entry(update_food_log_window)
        new_date_entry.pack()

        update_button = tk.Button(update_food_log_window, text="Update", 
                                command=lambda: [
                                    self.update_food_log_in_database(
                                        food_log_id_entry.get(), 
                                        new_food_name_entry.get(), 
                                        new_quantity_entry.get(), 
                                        new_date_entry.get()
                                    ),
                                    update_food_log_window.destroy()
                                ])
        update_button.pack(pady=10)

    def add_food_log_to_database(self, user_id, food_name, quantity, date):
        try:
            food_id = self.get_food_id(food_name)
            if food_id is None:
                messagebox.showerror("Error", "Food not found")
                return

            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                query = "INSERT INTO Food_Log (user_id, food_id, quantity, log_date) VALUES (%s, %s, %s, %s)"
                params = (user_id, food_id, quantity, date)
                cursor.execute(query, params)
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo("Success", "Food log added successfully")
                self.food_diary()  # Refresh the view
        except Error as e:
            messagebox.showerror("Error", f"Failed to add food log: {e}")

    def delete_food_log_from_database(self, food_log_id):
        try:
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                query = "DELETE FROM Food_Log WHERE log_id = %s"
                params = (food_log_id,)
                cursor.execute(query, params)
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo("Success", "Food log deleted successfully")
                self.food_diary()  # Refresh the view
        except Error as e:
            messagebox.showerror("Error", f"Failed to delete food log: {e}")

    def update_food_log_in_database(self, food_log_id, new_food_name, new_quantity, new_date):
        try:
            food_id = self.get_food_id(new_food_name)
            if food_id is None:
                messagebox.showerror("Error", "Food not found")
                return

            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                query = "UPDATE Food_Log SET food_id = %s, quantity = %s, log_date = %s WHERE log_id = %s"
                params = (food_id, new_quantity, new_date, food_log_id)
                cursor.execute(query, params)
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo("Success", "Food log updated successfully")
                self.food_diary()  # Refresh the view
        except Error as e:
            messagebox.showerror("Error", f"Failed to update food log: {e}")

    def get_food_id(self, food_name):
        try:
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                query = "SELECT food_id FROM Foods WHERE name = %s"
                params = (food_name,)
                cursor.execute(query, params)
                result = cursor.fetchone()
                cursor.close()
                conn.close()
                return result[0] if result else None
        except Error as e:
            messagebox.showerror("Error", f"Failed to get food ID: {e}")
            return None

    def diet_plan(self):
        # Clear existing widgets in right side frame
        for widget in self.right_side_frame.winfo_children():
            widget.destroy()

        tk.Label(self.right_side_frame, text="Diet Plan", font=("Arial", 18, "bold")).pack(pady=10)

        # Create a frame for the treeview and scrollbar
        tree_frame = tk.Frame(self.right_side_frame)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Create a treeview with scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")

        tree = ttk.Treeview(tree_frame, yscrollcommand=scrollbar.set)
        tree['columns'] = ('Date', 'Breakfast', 'Lunch', 'Dinner', 'Snacks')

        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("Date", anchor=tk.W, width=100)
        tree.column("Breakfast", anchor=tk.W, width=150)
        tree.column("Lunch", anchor=tk.W, width=150)
        tree.column("Dinner", anchor=tk.W, width=150)
        tree.column("Snacks", anchor=tk.W, width=150)

        tree.heading("#0", text="", anchor=tk.W)
        tree.heading("Date", text="Date", anchor=tk.W)
        tree.heading("Breakfast", text="Breakfast", anchor=tk.W)
        tree.heading("Lunch", text="Lunch", anchor=tk.W)
        tree.heading("Dinner", text="Dinner", anchor=tk.W)
        tree.heading("Snacks", text="Snacks", anchor=tk.W)

        try:
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                # First check if Diet_Plan table exists
                cursor.execute("SHOW TABLES LIKE 'Diet_Plan'")
                if not cursor.fetchone():
                    # Create the table if it doesn't exist
                    cursor.execute("""
                        CREATE TABLE Diet_Plan (
                            plan_id INT AUTO_INCREMENT PRIMARY KEY,
                            user_id INT NOT NULL,
                            date DATE NOT NULL,
                            breakfast VARCHAR(255),
                            lunch VARCHAR(255),
                            dinner VARCHAR(255),
                            snacks VARCHAR(255),
                            FOREIGN KEY (user_id) REFERENCES Users(user_id),
                            UNIQUE KEY unique_user_date (user_id, date)
                        )
                    """)
                    conn.commit()
                
                # Now query the table
                query = "SELECT date, breakfast, lunch, dinner, snacks FROM Diet_Plan WHERE user_id = %s"
                cursor.execute(query, (self.current_user_id,))
                results = cursor.fetchall()

                for row in results:
                    tree.insert('', 'end', values=row)

                cursor.close()
                conn.close()
        except Error as e:
            messagebox.showerror("Error", f"Failed to get diet plan: {e}")

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=tree.yview)

        # Create a frame for buttons
        button_frame = tk.Frame(self.right_side_frame)
        button_frame.pack(pady=10)

        # Create buttons
        add_plan_button = tk.Button(button_frame, text="Add New Plan", command=self.add_diet_plan)
        add_plan_button.pack(side="left", padx=5)

        update_plan_button = tk.Button(button_frame, text="Update Plan", command=self.update_diet_plan)
        update_plan_button.pack(side="left", padx=5)

        delete_plan_button = tk.Button(button_frame, text="Delete Plan", command=self.delete_diet_plan)
        delete_plan_button.pack(side="left", padx=5)

    def add_diet_plan(self):
        add_plan_window = tk.Toplevel(self.root)
        add_plan_window.title("Add Diet Plan")
        add_plan_window.geometry("300x350")

        tk.Label(add_plan_window, text="Date (YYYY-MM-DD):").pack()
        date_entry = tk.Entry(add_plan_window)
        date_entry.pack()

        tk.Label(add_plan_window, text="Breakfast:").pack()
        breakfast_entry = tk.Entry(add_plan_window)
        breakfast_entry.pack()

        tk.Label(add_plan_window, text="Lunch:").pack()
        lunch_entry = tk.Entry(add_plan_window)
        lunch_entry.pack()

        tk.Label(add_plan_window, text="Dinner:").pack()
        dinner_entry = tk.Entry(add_plan_window)
        dinner_entry.pack()

        tk.Label(add_plan_window, text="Snacks:").pack()
        snacks_entry = tk.Entry(add_plan_window)
        snacks_entry.pack()

        add_button = tk.Button(add_plan_window, text="Add", 
                             command=lambda: [
                                 self.add_diet_plan_to_database(
                                     date_entry.get(),
                                     breakfast_entry.get(),
                                     lunch_entry.get(),
                                     dinner_entry.get(),
                                     snacks_entry.get()
                                 ),
                                 add_plan_window.destroy()
                             ])
        add_button.pack(pady=10)

    def update_diet_plan(self):
        update_plan_window = tk.Toplevel(self.root)
        update_plan_window.title("Update Diet Plan")
        update_plan_window.geometry("300x350")

        tk.Label(update_plan_window, text="Date (YYYY-MM-DD):").pack()
        date_entry = tk.Entry(update_plan_window)
        date_entry.pack()

        tk.Label(update_plan_window, text="Breakfast:").pack()
        breakfast_entry = tk.Entry(update_plan_window)
        breakfast_entry.pack()

        tk.Label(update_plan_window, text="Lunch:").pack()
        lunch_entry = tk.Entry(update_plan_window)
        lunch_entry.pack()

        tk.Label(update_plan_window, text="Dinner:").pack()
        dinner_entry = tk.Entry(update_plan_window)
        dinner_entry.pack()

        tk.Label(update_plan_window, text="Snacks:").pack()
        snacks_entry = tk.Entry(update_plan_window)
        snacks_entry.pack()

        update_button = tk.Button(update_plan_window, text="Update", 
                                command=lambda: [
                                    self.update_diet_plan_in_database(
                                        date_entry.get(),
                                        breakfast_entry.get(),
                                        lunch_entry.get(),
                                        dinner_entry.get(),
                                        snacks_entry.get()
                                    ),
                                    update_plan_window.destroy()
                                ])
        update_button.pack(pady=10)

    def delete_diet_plan(self):
        delete_plan_window = tk.Toplevel(self.root)
        delete_plan_window.title("Delete Diet Plan")
        delete_plan_window.geometry("300x100")

        tk.Label(delete_plan_window, text="Date (YYYY-MM-DD):").pack()
        date_entry = tk.Entry(delete_plan_window)
        date_entry.pack()

        delete_button = tk.Button(delete_plan_window, text="Delete", 
                                command=lambda: [
                                    self.delete_diet_plan_from_database(date_entry.get()),
                                    delete_plan_window.destroy()
                                ])
        delete_button.pack(pady=10)

    def add_diet_plan_to_database(self, date, breakfast, lunch, dinner, snacks):
        try:
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                query = """INSERT INTO Diet_Plan 
                          (user_id, date, breakfast, lunch, dinner, snacks) 
                          VALUES (%s, %s, %s, %s, %s, %s)"""
                params = (self.current_user_id, date, breakfast, lunch, dinner, snacks)
                cursor.execute(query, params)
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo("Success", "Diet plan added successfully")
                self.diet_plan()  # Refresh the view
        except Error as e:
            messagebox.showerror("Error", f"Failed to add diet plan: {e}")

    def update_diet_plan_in_database(self, date, breakfast, lunch, dinner, snacks):
        try:
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                # First check if entry exists
                cursor.execute("SELECT 1 FROM Diet_Plan WHERE user_id = %s AND date = %s", 
                             (self.current_user_id, date))
                if not cursor.fetchone():
                    # If not exists, insert new
                    return self.add_diet_plan_to_database(date, breakfast, lunch, dinner, snacks)
                
                # If exists, update
                query = """UPDATE Diet_Plan 
                          SET breakfast = %s, lunch = %s, dinner = %s, snacks = %s
                          WHERE user_id = %s AND date = %s"""
                params = (breakfast, lunch, dinner, snacks, self.current_user_id, date)
                cursor.execute(query, params)
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo("Success", "Diet plan updated successfully")
                self.diet_plan()  # Refresh the view
        except Error as e:
            messagebox.showerror("Error", f"Failed to update diet plan: {e}")

    def delete_diet_plan_from_database(self, date):
        try:
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                query = "DELETE FROM Diet_Plan WHERE user_id = %s AND date = %s"
                params = (self.current_user_id, date)
                cursor.execute(query, params)
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo("Success", "Diet plan deleted successfully")
                self.diet_plan()  # Refresh the view
        except Error as e:
            messagebox.showerror("Error", f"Failed to delete diet plan: {e}")



    def display_all_foods(self):
            # Clear existing widgets
            for widget in self.right_side_frame.winfo_children():
                widget.destroy()

            # Create a frame to hold the food list
            self.food_list_frame = tk.Frame(self.right_side_frame, bg="#FFFFFE")
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



    def logout(self):
        self.root.destroy()
        self.main_app.on_dashboard_close()

if __name__ == "__main__":
    root = tk.Tk()
    app = User(root)
    root.mainloop()