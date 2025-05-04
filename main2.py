import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from mysql.connector import Error
from admin import Admin
from user import User


# Connect to MySQL Database
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


class DietTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Diet Tracker")
        self.root.geometry("600x400")
        root.wm_iconbitmap("food.ico")
        self.root.resizable(False, False)
        root.config(bg="#E3EDEF")
        

        self.conn = connect_to_database()
        if self.conn:
            self.cursor = self.conn.cursor()
            self.create_login_ui()
        else:
            messagebox.showerror("Error", "Failed to connect to the database. Exiting...")
            self.root.destroy()

    def create_login_ui(self):
        # Clear existing widgets
        self.clear_widgets()

        # Database checking button
        tk.Button(
            self.root,
            bg="#4796BD",
            fg="white",
            text="Check Database Connection",
            font=("Arial", 10, "bold"),
            command=self.check_database_connection
        ).pack(side="top", pady=5, padx=5, anchor="e")

        tk.Label(self.root, text="Diet Tracker", bg="#E3EDEF", font=("Arial", 18)).pack(side="bottom", padx=10, anchor="w")

        # Shadow frame
        self.shadow_frame = tk.Frame(self.root, bg="#b0b0b0")
        self.shadow_frame.place(x=50, y=50, width=540, height=310)

        # Login frame
        self.login_frame = tk.Frame(self.root, bg="#FFFFFE", bd=2)
        self.login_frame.place(x=40, y=40, width=540, height=310)

        # Load the image
        try:
            image = tk.PhotoImage(file="health.png")
            image = image.subsample(3, 3)
            image_label = tk.Label(self.login_frame, image=image)
            image_label.image = image  # Keep a reference to the image
            image_label.pack(side="left")
        except:
            pass  # Skip if image not found

        tk.Label(self.login_frame, bg="#FFFFFE", text="Login", font=("Arial", 18, "bold")).pack(anchor="center", pady="10")

        # Role dropdown
        tk.Label(self.login_frame, bg="#FFFFFE", text="Role:", font=("Arial", 10, "bold")).pack(side="top")
        self.role_var = tk.StringVar()
        self.role_dropdown = ttk.Combobox(self.login_frame, textvariable=self.role_var, values=["user", "admin"])
        self.role_dropdown.pack(side="top")
        self.role_dropdown.current(0)  # Set default value to "user"

        # Email and Password Entry Fields
        tk.Label(self.login_frame, bg="#FFFFFE", text="Email:").pack(side="top")
        self.email_entry = tk.Entry(self.login_frame, bg="#f6f5f5")
        self.email_entry.pack(side="top")

        tk.Label(self.login_frame, bg="#FFFFFE", text="Password:").pack(side="top")
        self.password_entry = tk.Entry(self.login_frame, show="*", bg="#f6f5f5")
        self.password_entry.pack(side="top")

        # Submit button
        tk.Button(
            self.login_frame,
            bg="#4796BD",
            fg="white",
            text="Submit",
            font=("Arial", 10, "bold"),
            command=self.submit_button_clicked
        ).pack(side="top", pady=10)

        # New user registration
        tk.Label(self.login_frame, bg="#FFFFFE", text="New User?").pack(side="left")
        tk.Button(
            self.login_frame,
            bg="#4796BD",
            fg="white",
            text="Register",
            font=("Arial", 10, "bold"),
            command=self.create_register_ui
        ).pack(side="right")

    def submit_button_clicked(self):
        # Retrieve user inputs
        role = self.role_var.get()  # Get selected role from dropdown
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Validate inputs
        if not email or not password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Query the database to check credentials
        try:
            query = "SELECT * FROM users WHERE email = %s AND password = %s AND role = %s"
            self.cursor.execute(query, (email, password, role))
            user = self.cursor.fetchone()

            if user:
                messagebox.showinfo("Success", "Login successful!")
                # Store user ID for later use
                self.current_user_id = user[0]
                # Proceed to the next screen (e.g., dashboard)
                self.show_dashboard(role)
            else:
                messagebox.showerror("Error", "Invalid email, password, or role.")
        except Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

    def show_dashboard(self, role):
        # Clear existing widgets
        self.clear_widgets()
        

        # Create a new window for the dashboard
        dashboard_window = tk.Toplevel(self.root)
        dashboard_window.protocol("WM_DELETE_WINDOW", self.on_dashboard_close)
        
        # Display dashboard based on role
        if role == "admin":
            admin_app = Admin(dashboard_window, self)
        else:
            user_app = User(dashboard_window, self)
            user_app.current_user_id = self.current_user_id

        # Hide the main window
        self.root.withdraw()

    def get_db_connection(self):
        """Get a database connection, reconnecting if needed"""
        try:
            if not hasattr(self, 'conn') or not self.conn.is_connected():
                self.conn = connect_to_database()
                if self.conn:
                    self.cursor = self.conn.cursor()
            return self.conn
        except Error as e:
            messagebox.showerror("Error", f"Database connection error: {e}")
            return None

    def on_dashboard_close(self):
        # Show the main window again
        self.root.deiconify()
        # Reinitialize the login UI
        self.create_login_ui()

    def check_database_connection(self):
        try:
            # Attempt to reconnect to the database
            self.conn.ping(reconnect=True)
            messagebox.showinfo("Success", "Database connection is active!")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to connect to the database: {err}")

    def create_register_ui(self):
        # Clear existing widgets
        self.clear_widgets()

        # Back button
        tk.Button(self.root, text="Back to Login", 
                 bg="#4796BD",
                 fg="white",
                 font=("Arial", 10, "bold"),
                 command=self.create_login_ui).pack(side="top", anchor="w", pady=5, padx=5)

        # Shadow frame
        self.shadow_frame = tk.Frame(self.root, bg="#b0b0b0")
        self.shadow_frame.place(x=50, y=50, width=540, height=310)

        # Register frame
        self.register_frame = tk.Frame(self.root, bg="#FFFFFE", bd=2)
        self.register_frame.place(x=40, y=40, width=540, height=310)

        # Load the image
        try:
            image = tk.PhotoImage(file="shiv.png")
            image = image.subsample(3, 3)
            image_label = tk.Label(self.register_frame, image=image)
            image_label.image = image  # Keep a reference to the image
            image_label.pack(side="right")
        except:
            pass  # Skip if image not found

        tk.Label(self.register_frame, bg="#FFFFFE", text="Welcome !!", font=("Arial", 18, "bold")).pack(anchor="center", pady="10")

        tk.Label(self.register_frame, bg="#FFFFFE", text="Name:").pack()
        self.name_entry = tk.Entry(self.register_frame, bg="#f6f5f5")
        self.name_entry.pack()

        tk.Label(self.register_frame, bg="#FFFFFE", text="Email:").pack()
        self.email_entry = tk.Entry(self.register_frame, bg="#f6f5f5")
        self.email_entry.pack()

        tk.Label(self.register_frame, bg="#FFFFFE", text="Password:").pack()
        self.password_entry = tk.Entry(self.register_frame, bg="#f6f5f5", show="*")
        self.password_entry.pack()

        tk.Label(self.register_frame, bg="#FFFFFE", text="Daily Calorie Goal:").pack()
        self.calorie_goal_entry = tk.Entry(self.register_frame, bg="#f6f5f5")
        self.calorie_goal_entry.pack()

        # Add a dropdown for role selection
        tk.Label(self.register_frame, bg="#FFFFFE", text="Role:", font=("Arial", 10, "bold")).pack()
        self.role_var = tk.StringVar()
        self.role_dropdown = ttk.Combobox(self.register_frame, textvariable=self.role_var, values=["user", "admin"])
        self.role_dropdown.pack()
        self.role_dropdown.current(0)  # Set default value to "user"

        # Button section
        tk.Button(self.register_frame, text="Register",
                 bg="#4796BD",
                 fg="white",                  
                 font=("Arial", 10, "bold"),
                 command=self.register_user).pack(pady=10)
        
        tk.Label(self.root, text="Register", bg="#E3EDEF", font=("Arial", 18)).pack(side="bottom", padx=10, anchor="center")

    def register_user(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        calorie_goal = self.calorie_goal_entry.get()
        role = self.role_var.get()  # Get selected role from dropdown

        if not all([name, email, password, calorie_goal]):
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            # Check if email already exists
            self.cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
            if self.cursor.fetchone():
                messagebox.showerror("Error", "Email already registered!")
                return

            self.cursor.execute("""
                INSERT INTO Users (name, email, password, daily_calorie_goal, role)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, email, password, calorie_goal, role))

            self.conn.commit()
            messagebox.showinfo("Success", "User registered successfully!")
            self.create_login_ui()
        except Error as e:
            messagebox.showerror("Error", f"Registration failed: {e}")

    def clear_widgets(self):
        # Clears all widgets from the root window.
        for widget in self.root.winfo_children():
            widget.destroy()

# Run the App
if __name__ == "__main__":
    root = tk.Tk()
    app = DietTrackerApp(root)
    root.mainloop()