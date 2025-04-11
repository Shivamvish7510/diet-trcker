import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from mysql.connector import Error


def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="----------",
            database="DietTracker3"
        )
        return conn
    except Error as e:
        messagebox.showerror("Error", f"Failed to connect to the database: {e}")
        return None

# Main Application Class
class Admin:
    def __init__(self, root , main_app):
        self.root = root
        self.main_app = main_app 
        self.root.title("Diet Tracker")
        self.root.geometry("600x400")
        root.wm_iconbitmap("food.ico")
        self.create_admin_dashboard()
        root.config(bg="#E3EDEF")

    def create_admin_dashboard(self):
        # Create User Dashboard Frame
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Header
        self.user = tk.Frame(self.root, bg="#4796BD", height=50)  # Set a fixed height
        self.user.pack(fill="x")
        tk.Label(self.user, bg="#4796BD", fg="white", text="Admin Dashboard", font=("Arial", 18, "bold")).pack(pady=10, anchor="center")
        
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
        tk.Button(self.menu_buttons_frame, text="Users",command=self.display_all_users, font=("Arial", 10)).pack(side="top", fill="x")
        tk.Button(self.menu_buttons_frame, text="Food", font=("Arial", 10),command=self.display_all_foods).pack(side="top", fill="x")
        tk.Button(self.menu_buttons_frame, text="add new food", font=("Arial", 10) , command=self.add_new_food).pack(side="top", fill="x")
        tk.Button(self.menu_buttons_frame, text="Add new user",command=self.add_new_user, font=("Arial", 10)).pack(side="top", fill="x")
        tk.Button(self.menu_buttons_frame, text="update User",command=self.update_user, font=("Arial", 10)).pack(side="top", fill="x")
        tk.Button(self.menu_buttons_frame, text="Delete user",command=self.delete_user, font=("Arial", 10)).pack(side="top", fill="x")

        # Login button frame
        self.login_button_frame = tk.Frame(self.navigation_menu, bg="#FFFFFE")
        self.login_button_frame.pack(side="bottom", fill="x")

        tk.Button(self.login_button_frame, bg="#4796BD", fg="white",text="Log Out",command=self.logout ,font=("Arial", 10,"bold")).pack(side="bottom",pady=5, fill="x")


        # Dashboard Statistics

        self.right_side_frame = tk.Frame(self.root, bg="#FFFFFE", bd=2,width=400, height=500)
        self.right_side_frame.pack(side="left", fill="both",expand=True, anchor="ne")

        tk.Label(self.right_side_frame, text="Dashboard Statistics", font=("Arial", 10, "bold")).pack(side="top", fill="x")
        self.display_total_users()  # Call the function to display total users
        self.display_total_foods()
        

        scrollbar = tk.Scrollbar(self.right_side_frame)
        scrollbar.pack(side="right", fill="y")

    def display_total_users(self):
        conn = connect_to_database()
        cursor = conn.cursor()
        
        # Query to retrieve total number of users
        query = "SELECT COUNT(*) FROM users"
        cursor.execute(query)
        total_users = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        # Update Dashboard Statistics label
        tk.Label(self.right_side_frame, text=f"Total Users: {total_users}", font=("Arial", 10)).pack(side="top", fill="x")

    def display_total_foods(self):
            conn = connect_to_database()
            cursor = conn.cursor()
            
            
            query = "SELECT COUNT(*) FROM foods"
            cursor.execute(query)
            total_foods = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            
            # Update Dashboard Statistics label
            tk.Label(self.right_side_frame, text=f"Total Foods: {total_foods}", font=("Arial", 10)).pack(side="top", fill="x")

    def display_all_users(self):
        # Clear existing widgets
        for widget in self.right_side_frame.winfo_children():
            widget.destroy()

        # Create a frame to hold the user list
        self.user_list_frame = tk.Frame(self.right_side_frame, bg="#FFFFFE")
        self.user_list_frame.pack(side="top", fill="both", expand=True)

        # Create a scrollbar
        self.scrollbar = tk.Scrollbar(self.user_list_frame)
        self.scrollbar.pack(side="right", fill="y")

        # Create a horizontal scrollbar
        self.x_scrollbar = tk.Scrollbar(self.user_list_frame, orient=tk.HORIZONTAL)
        self.x_scrollbar.pack(side="bottom", fill="x")
        

        # Create a table to display the user list
        self.user_list_table = ttk.Treeview(self.user_list_frame,
                                            xscrollcommand=self.x_scrollbar.set, 
                                            yscrollcommand=self.scrollbar.set)
        self.user_list_table.pack(side="left", fill="both", expand=True)

        # Configure the scrollbar
        self.x_scrollbar.config(command=self.user_list_table.xview)
        self.scrollbar.config(command=self.user_list_table.yview)
       
        # Define the columns
        self.user_list_table['columns'] = ('ID', 'Name', 'Email', 'Password', 'daily_calorie_goal', 'Role')

        # Format the columns
        self.user_list_table.column("#0", width=0, stretch=tk.NO)
        self.user_list_table.column("ID", anchor=tk.W, width=50)
        self.user_list_table.column("Name", anchor=tk.W, width=150)
        self.user_list_table.column("Email", anchor=tk.W, width=200)
        self.user_list_table.column("Password", anchor=tk.W, width=250)
        self.user_list_table.column("daily_calorie_goal", anchor=tk.W)
        self.user_list_table.column("Role", anchor=tk.W)

        # Create the headings
        self.user_list_table.heading("#0", text="", anchor=tk.W)
        self.user_list_table.heading("ID", text="ID", anchor=tk.W)
        self.user_list_table.heading("Name", text="Name", anchor=tk.W)
        self.user_list_table.heading("Email", text="Email", anchor=tk.W)
        self.user_list_table.heading("Password", text="Password", anchor=tk.W)
        self.user_list_table.heading("daily_calorie_goal", text="daily calorie goal", anchor=tk.W)
        self.user_list_table.heading("Role", text="Role", anchor=tk.W)

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
            self.user_list_table.insert('', 'end', values=(user[0], user[1], user[2],user[3],user[4],user[5]))



    def add_new_user(self):
        # Clear existing widgets
        for widget in self.right_side_frame.winfo_children():
            widget.destroy()

        # Create a frame to hold the input fields
        self.input_fields_frame = tk.Frame(self.right_side_frame, bg="#FFFFFE")
        self.input_fields_frame.pack(side="top", fill="both", expand=True)

        # Create input fields
        tk.Label(self.input_fields_frame, text="Name:", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(self.input_fields_frame, font=("Arial", 10))
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.input_fields_frame, text="Email:", font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=5)
        self.email_entry = tk.Entry(self.input_fields_frame, font=("Arial", 10))
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.input_fields_frame, text="Password:", font=("Arial", 10)).grid(row=2, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(self.input_fields_frame, font=("Arial", 10), show="*")
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.input_fields_frame, text="Daily Calorie Goal:", font=("Arial", 10)).grid(row=3, column=0, padx=5, pady=5)
        self.daily_calorie_goal_entry = tk.Entry(self.input_fields_frame, font=("Arial", 10))
        self.daily_calorie_goal_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.input_fields_frame, text="Role:", font=("Arial", 10)).grid(row=4, column=0, padx=5, pady=5)
        self.role_entry = tk.Entry(self.input_fields_frame, font=("Arial", 10))
        self.role_entry.grid(row=4, column=1, padx=5, pady=5)

        # Create a button to submit the form
        tk.Button(self.input_fields_frame, bg="#4796BD", fg="white",text="Add User", font=("Arial", 10,"bold"), command=self.submit_add_user_form).grid(row=5, column=1, padx=5, pady=5)


    def submit_add_user_form(self):
        # Retrieve input values
        name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        daily_calorie_goal = self.daily_calorie_goal_entry.get()
        role = self.role_entry.get()

        # Insert into database
        conn = connect_to_database()
        cursor = conn.cursor()
        query = "INSERT INTO users (name, email, password, daily_calorie_goal, role) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (name, email, password, daily_calorie_goal, role))
        conn.commit()
        cursor.close()
        conn.close()

        # Clear input fields
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.daily_calorie_goal_entry.delete(0, tk.END)
        self.role_entry.delete(0, tk.END)

        # show message box
        messagebox.showinfo("Success", "User added successfully")


    def update_user(self):
        # Clear existing widgets
        for widget in self.right_side_frame.winfo_children():
            widget.destroy()

        # Create a frame to hold the input fields
        self.input_fields_frame = tk.Frame(self.right_side_frame, bg="#FFFFFE")
        self.input_fields_frame.pack(side="top", fill="both", expand=True)

        # Create input fields
        tk.Label(self.input_fields_frame, text="User ID:", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5)
        self.user_id_entry = tk.Entry(self.input_fields_frame, font=("Arial", 10))
        self.user_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.input_fields_frame, text="Name:", font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(self.input_fields_frame, font=("Arial", 10))
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.input_fields_frame, text="Email:", font=("Arial", 10)).grid(row=2, column=0, padx=5, pady=5)
        self.email_entry = tk.Entry(self.input_fields_frame, font=("Arial", 10))
        self.email_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.input_fields_frame, text="Password:", font=("Arial", 10)).grid(row=3, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(self.input_fields_frame, font=("Arial", 10), show="*")
        self.password_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.input_fields_frame, text="Daily Calorie Goal:", font=("Arial", 10)).grid(row=4, column=0, padx=5, pady=5)
        self.daily_calorie_goal_entry = tk.Entry(self.input_fields_frame, font=("Arial", 10))
        self.daily_calorie_goal_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(self.input_fields_frame, text="Role:", font=("Arial", 10)).grid(row=5, column=0, padx=5, pady=5)
        self.role_entry = tk.Entry(self.input_fields_frame, font=("Arial", 10))
        self.role_entry.grid(row=5, column=1, padx=5, pady=5)

        # Create a button to submit the form
        tk.Button(self.input_fields_frame, bg="#4796BD", fg="white", text="Update User", font=("Arial", 10, "bold"), command=self.submit_update_user_form).grid(row=6, column=1, padx=5, pady=5)
        

    def submit_update_user_form(self):
        try:
            # Retrieve input values
            user_id = self.user_id_entry.get()
            name = self.name_entry.get()
            email = self.email_entry.get()
            password = self.password_entry.get()
            daily_calorie_goal = self.daily_calorie_goal_entry.get()
            role = self.role_entry.get()

            # Validate input values
            if not all([user_id, name, email, password, daily_calorie_goal, role]):
                messagebox.showerror("Error", "Please fill in all required fields")
                return

            # Update user in database
            conn = connect_to_database()
            cursor = conn.cursor()
            query = "UPDATE users SET name = %s, email = %s, password = %s, daily_calorie_goal = %s, role = %s WHERE user_id = %s"
            cursor.execute(query, (name, email, password, daily_calorie_goal, role, user_id))
            conn.commit()
            cursor.close()
            conn.close()

            # Clear input fields
            self.user_id_entry.delete(0, tk.END)
            self.name_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.daily_calorie_goal_entry.delete(0, tk.END)
            self.role_entry.delete(0, tk.END)

            messagebox.showinfo("Success", "User detail updated successfully")

        except Error as e:
            messagebox.showerror("Error", f"Failed to update user: {e}")


    def delete_user(self):
        # Clear existing widgets
        for widget in self.right_side_frame.winfo_children():
            widget.destroy()

        # Create a frame to hold the input fields
        self.input_fields_frame = tk.Frame(self.right_side_frame, bg="#FFFFFE")
        self.input_fields_frame.pack(side="top", fill="both", expand=True)

        # Create input fields
        tk.Label(self.input_fields_frame, text="User ID:", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5)
        self.user_id_entry = tk.Entry(self.input_fields_frame, font=("Arial", 10))
        self.user_id_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(self.input_fields_frame, text="Email:", font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=5)
        self.email_entry = tk.Entry(self.input_fields_frame, font=("Arial", 10))
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)

        # Create a button to submit the form
        tk.Button(self.input_fields_frame, bg="#4796BD", fg="white", text="Delete User", font=("Arial", 10, "bold"), command=self.submit_delete_user_form).grid(row=3, column=1, padx=5, pady=5)


    def submit_delete_user_form(self):
        try:
            # Retrieve input values
            user_id = self.user_id_entry.get()
            email = self.email_entry.get()

            # Validate input values
            if not user_id:
                messagebox.showerror("Error", "Please enter a user ID")
                return

            # Delete user from database
            conn = connect_to_database()
            cursor = conn.cursor()
            query = "DELETE FROM users WHERE user_id = %s and email=%s"
            cursor.execute(query, (user_id,email))
            conn.commit()
            cursor.close()
            conn.close()

            # Clear input fields
            self.user_id_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            
            messagebox.showinfo("User Deleted", f"User with ID {user_id} has been deleted successfully.")
        except Error as e:
            messagebox.showerror("Error", f"Failed to delete user: {e}")
        
    
    def add_new_food(self):
        # Clear existing widgets
        for widget in self.right_side_frame.winfo_children():
            widget.destroy()

        # Create a frame to hold the input fields
        self.input_fields_frame = tk.Frame(self.right_side_frame, bg="#FFFFFE")
        self.input_fields_frame.pack(side="top", fill="both", expand=True)

        # Create input fields
        tk.Label(self.input_fields_frame, text="Food Name:", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5)
        self.food_name_entry = tk.Entry(self.input_fields_frame, font=("Arial", 10))
        self.food_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.input_fields_frame, text="Calories:", font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=5)
        self.calories_entry = tk.Entry(self.input_fields_frame, font=("Arial", 10))
        self.calories_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.input_fields_frame, text="Portion:", font=("Arial", 10)).grid(row=2, column=0, padx=5, pady=5)
        self.portion_entry = tk.Entry(self.input_fields_frame, font=("Arial", 10))
        self.portion_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.input_fields_frame, text="fat_per_100g:", font=("Arial", 10)).grid(row=3, column=0, padx=5, pady=5)
        self.fat_entry = tk.Entry(self.input_fields_frame, font=("Arial", 10))
        self.fat_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.input_fields_frame, text="carbs_per_100g:", font=("Arial", 10)).grid(row=4, column=0, padx=5, pady=5)
        self.carb_entry = tk.Entry(self.input_fields_frame, font=("Arial", 10))
        self.carb_entry.grid(row=4, column=1, padx=5, pady=5)

        # Create a button to submit the form
        tk.Button(self.input_fields_frame, bg="#4796BD", fg="white", text="Add Food", font=("Arial", 10, "bold"), command=self.submit_add_food_form).grid(row=5, column=1, padx=5, pady=5)


    def submit_add_food_form(self):
        # Retrieve input values
        food_name = self.food_name_entry.get()
        calories = self.calories_entry.get()
        portion = self.portion_entry.get()
        fat = self.fat_entry.get()
        carb = self.carb_entry.get()

        # Validate input values
        if not all([food_name, calories, portion,]):
            messagebox.showerror("Error", "Please fill in all required fields")
            return

        # Insert into database
        conn = connect_to_database()
        cursor = conn.cursor()
        query = "INSERT INTO food (food_name, calories, portion) VALUES (%s, %s, %s,%s,%s)"
        cursor.execute(query, (food_name, calories, portion,fat,carb))
        conn.commit()
        cursor.close()
        conn.close()

        # Clear input fields
        self.food_name_entry.delete(0, tk.END)
        self.calories_entry.delete(0, tk.END)
        self.portion_entry.delete(0, tk.END)
        self.fat_entry.delete(0, tk.END)
        self.carb_entry.delete(0, tk.END)

        # Show message box
        messagebox.showinfo("Success", "Food added successfully")

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
          
# run app
if __name__ == "__main__":
    root = tk.Tk()
    app = Admin(root)
    root.mainloop()
