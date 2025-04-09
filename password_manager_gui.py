import sqlite3
import re
import os
import hashlib
import tkinter as tk
from tkinter import messagebox, ttk, simpledialog

class PasswordManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Set color scheme
        self.bg_color = "#2c3e50"
        self.fg_color = "white"
        self.button_color = "#3498db"
        self.root.configure(bg=self.bg_color)
        
        # Initialize the database
        self.pm = PasswordManager()
        
        # Show main screen
        self.show_main_screen()
    
    def show_main_screen(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create title
        title = tk.Label(self.root, text="Password Manager", font=("Arial", 24, "bold"), 
                        bg=self.bg_color, fg=self.fg_color)
        title.pack(pady=30)
        
        # Create buttons
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(pady=20)
        
        register_btn = tk.Button(button_frame, text="Register", font=("Arial", 12),
                               bg=self.button_color, fg=self.fg_color, width=20,
                               command=self.show_register_screen)
        register_btn.pack(pady=10)
        
        add_pwd_btn = tk.Button(button_frame, text="Add Password", font=("Arial", 12),
                              bg=self.button_color, fg=self.fg_color, width=20,
                              command=self.show_add_password_screen)
        add_pwd_btn.pack(pady=10)
        
        view_pwd_btn = tk.Button(button_frame, text="View Passwords", font=("Arial", 12),
                               bg=self.button_color, fg=self.fg_color, width=20,
                               command=self.show_view_passwords_screen)
        view_pwd_btn.pack(pady=10)
        
        exit_btn = tk.Button(button_frame, text="Exit", font=("Arial", 12),
                           bg="#e74c3c", fg=self.fg_color, width=20,
                           command=self.root.destroy)
        exit_btn.pack(pady=10)
    
    def show_register_screen(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create title
        title = tk.Label(self.root, text="Register", font=("Arial", 20, "bold"), 
                        bg=self.bg_color, fg=self.fg_color)
        title.pack(pady=20)
        
        # Create input frame
        input_frame = tk.Frame(self.root, bg=self.bg_color)
        input_frame.pack(pady=10)
        
        # Phone number
        phone_label = tk.Label(input_frame, text="Phone Number:", font=("Arial", 12),
                             bg=self.bg_color, fg=self.fg_color)
        phone_label.grid(row=0, column=0, sticky="w", pady=5, padx=5)
        
        self.phone_entry = tk.Entry(input_frame, font=("Arial", 12), width=20)
        self.phone_entry.grid(row=0, column=1, pady=5, padx=5)
        
        # Master password
        pwd_label = tk.Label(input_frame, text="Master Password:", font=("Arial", 12),
                           bg=self.bg_color, fg=self.fg_color)
        pwd_label.grid(row=1, column=0, sticky="w", pady=5, padx=5)
        
        self.pwd_entry = tk.Entry(input_frame, font=("Arial", 12), width=20, show="*")
        self.pwd_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Confirm password
        confirm_label = tk.Label(input_frame, text="Confirm Password:", font=("Arial", 12),
                              bg=self.bg_color, fg=self.fg_color)
        confirm_label.grid(row=2, column=0, sticky="w", pady=5, padx=5)
        
        self.confirm_entry = tk.Entry(input_frame, font=("Arial", 12), width=20, show="*")
        self.confirm_entry.grid(row=2, column=1, pady=5, padx=5)
        
        # Button frame
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(pady=20)
        
        register_btn = tk.Button(button_frame, text="Register", font=("Arial", 12),
                               bg=self.button_color, fg=self.fg_color, width=15,
                               command=self.register_user)
        register_btn.pack(side=tk.LEFT, padx=10)
        
        back_btn = tk.Button(button_frame, text="Back", font=("Arial", 12),
                           bg="#e74c3c", fg=self.fg_color, width=15,
                           command=self.show_main_screen)
        back_btn.pack(side=tk.LEFT, padx=10)
    
    def register_user(self):
        phone = self.phone_entry.get()
        password = self.pwd_entry.get()
        confirm = self.confirm_entry.get()
        
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match!")
            return
        
        if self.pm.register_user(phone, password):
            messagebox.showinfo("Success", "Registration successful!")
            self.show_main_screen()
    
    def show_add_password_screen(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create title
        title = tk.Label(self.root, text="Add Password", font=("Arial", 20, "bold"), 
                        bg=self.bg_color, fg=self.fg_color)
        title.pack(pady=20)
        
        # Create input frame
        input_frame = tk.Frame(self.root, bg=self.bg_color)
        input_frame.pack(pady=10)
        
        # Phone number
        phone_label = tk.Label(input_frame, text="Phone Number:", font=("Arial", 12),
                             bg=self.bg_color, fg=self.fg_color)
        phone_label.grid(row=0, column=0, sticky="w", pady=5, padx=5)
        
        self.phone_entry = tk.Entry(input_frame, font=("Arial", 12), width=20)
        self.phone_entry.grid(row=0, column=1, pady=5, padx=5)
        
        # Master password
        pwd_label = tk.Label(input_frame, text="Master Password:", font=("Arial", 12),
                           bg=self.bg_color, fg=self.fg_color)
        pwd_label.grid(row=1, column=0, sticky="w", pady=5, padx=5)
        
        self.pwd_entry = tk.Entry(input_frame, font=("Arial", 12), width=20, show="*")
        self.pwd_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Website
        website_label = tk.Label(input_frame, text="Website:", font=("Arial", 12),
                               bg=self.bg_color, fg=self.fg_color)
        website_label.grid(row=2, column=0, sticky="w", pady=5, padx=5)
        
        self.website_entry = tk.Entry(input_frame, font=("Arial", 12), width=20)
        self.website_entry.grid(row=2, column=1, pady=5, padx=5)
        
        # Username
        username_label = tk.Label(input_frame, text="Username:", font=("Arial", 12),
                                bg=self.bg_color, fg=self.fg_color)
        username_label.grid(row=3, column=0, sticky="w", pady=5, padx=5)
        
        self.username_entry = tk.Entry(input_frame, font=("Arial", 12), width=20)
        self.username_entry.grid(row=3, column=1, pady=5, padx=5)
        
        # Password
        password_label = tk.Label(input_frame, text="Password:", font=("Arial", 12),
                                bg=self.bg_color, fg=self.fg_color)
        password_label.grid(row=4, column=0, sticky="w", pady=5, padx=5)
        
        self.password_entry = tk.Entry(input_frame, font=("Arial", 12), width=20, show="*")
        self.password_entry.grid(row=4, column=1, pady=5, padx=5)
        
        # Button frame
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(pady=20)
        
        save_btn = tk.Button(button_frame, text="Save", font=("Arial", 12),
                           bg=self.button_color, fg=self.fg_color, width=15,
                           command=self.add_password)
        save_btn.pack(side=tk.LEFT, padx=10)
        
        back_btn = tk.Button(button_frame, text="Back", font=("Arial", 12),
                           bg="#e74c3c", fg=self.fg_color, width=15,
                           command=self.show_main_screen)
        back_btn.pack(side=tk.LEFT, padx=10)
    
    def add_password(self):
        phone = self.phone_entry.get()
        master_password = self.pwd_entry.get()
        website = self.website_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not all([phone, master_password, website, username, password]):
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if self.pm.add_password(phone, master_password, website, username, password):
            messagebox.showinfo("Success", "Password saved successfully!")
            self.show_main_screen()
    
    def show_view_passwords_screen(self):
        # Ask for phone number and password
        phone = simpledialog.askstring("Authentication", "Enter your phone number:", parent=self.root)
        if not phone:
            return
            
        master_password = simpledialog.askstring("Authentication", "Enter your master password:", 
                                               parent=self.root, show='*')
        if not master_password:
            return
        
        # Authenticate and get passwords
        user_id = self.pm.authenticate_user(phone, master_password)
        if not user_id:
            messagebox.showerror("Error", "Authentication failed")
            return
            
        passwords = self.pm.get_passwords(user_id)
        
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create title
        title = tk.Label(self.root, text="Your Passwords", font=("Arial", 20, "bold"), 
                        bg=self.bg_color, fg=self.fg_color)
        title.pack(pady=20)
        
        if not passwords:
            no_pwd_label = tk.Label(self.root, text="No passwords saved yet", 
                                  font=("Arial", 14), bg=self.bg_color, fg=self.fg_color)
            no_pwd_label.pack(pady=20)
        else:
            # Create password list frame with scrollbar
            container = tk.Frame(self.root, bg=self.bg_color)
            container.pack(fill="both", expand=True, padx=20, pady=10)
            
            # Create canvas for scrolling
            canvas = tk.Canvas(container, bg=self.bg_color, highlightthickness=0)
            scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
            
            scroll_frame = tk.Frame(canvas, bg=self.bg_color)
            scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            
            canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Add password entries
            for i, (website, username, password) in enumerate(passwords):
                pwd_frame = tk.Frame(scroll_frame, bg="#34495e", bd=1, relief=tk.RAISED)
                pwd_frame.pack(fill="x", padx=5, pady=5)
                
                website_label = tk.Label(pwd_frame, text=f"Website: {website}", 
                                      font=("Arial", 12), bg="#34495e", fg=self.fg_color)
                website_label.pack(anchor="w", padx=10, pady=2)
                
                username_label = tk.Label(pwd_frame, text=f"Username: {username}", 
                                       font=("Arial", 12), bg="#34495e", fg=self.fg_color)
                username_label.pack(anchor="w", padx=10, pady=2)
                
                password_label = tk.Label(pwd_frame, text=f"Password: {password}", 
                                       font=("Arial", 12), bg="#34495e", fg=self.fg_color)
                password_label.pack(anchor="w", padx=10, pady=2)
        
        # Back button
        back_btn = tk.Button(self.root, text="Back", font=("Arial", 12),
                           bg="#e74c3c", fg=self.fg_color, width=15,
                           command=self.show_main_screen)
        back_btn.pack(pady=20)

class PasswordManager:
    def __init__(self):
        self.init_database()

    def validate_phone_number(self, phone_number):
        # Remove any spaces or special characters
        phone_number = re.sub(r'[^0-9+]', '', phone_number)
            
        # Basic validation
        if len(phone_number) < 10:
            return False
            
        return True

    def init_database(self):
        # Check if database exists
        db_exists = os.path.exists('passwords.db')
        
        # Connect to database
        conn = sqlite3.connect('passwords.db')
        cursor = conn.cursor()
        
        if db_exists:
            # Check if master_password column exists in users table
            cursor.execute("PRAGMA table_info(users)")
            columns = [col[1] for col in cursor.fetchall()]
            
            if 'master_password' not in columns:
                # Create a new users table with updated schema
                cursor.execute('''
                    CREATE TABLE users_new (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        phone_number TEXT UNIQUE,
                        master_password TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Drop old table and rename new one
                cursor.execute("DROP TABLE users")
                cursor.execute("ALTER TABLE users_new RENAME TO users")
                
                # Also recreate the passwords table to ensure foreign key constraints
                cursor.execute("DROP TABLE IF EXISTS passwords")
                cursor.execute('''
                    CREATE TABLE passwords (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        website TEXT,
                        username TEXT,
                        password TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                ''')
        else:
            # Create users table with master_password field
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    phone_number TEXT UNIQUE,
                    master_password TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create passwords table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS passwords (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    website TEXT,
                    username TEXT,
                    password TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
        
        conn.commit()
        conn.close()

    def hash_password(self, password):
        # Simple password hashing using SHA-256
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, phone_number, master_password):
        if not self.validate_phone_number(phone_number):
            return False
        
        if len(master_password) < 6:
            return False
            
        try:
            # Hash the master password before storing it
            hashed_password = self.hash_password(master_password)
            
            conn = sqlite3.connect('passwords.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (phone_number, master_password) VALUES (?, ?)", 
                          (phone_number, hashed_password))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def authenticate_user(self, phone_number, master_password):
        try:
            conn = sqlite3.connect('passwords.db')
            cursor = conn.cursor()
            
            # Get the stored hashed password
            cursor.execute("SELECT id, master_password FROM users WHERE phone_number = ?", (phone_number,))
            user = cursor.fetchone()
            conn.close()
            
            if not user:
                return False
            
            user_id, stored_password = user
            
            # Hash the provided password and compare
            if self.hash_password(master_password) == stored_password:
                return user_id
            else:
                return False
                
        except Exception as e:
            return False

    def add_password(self, phone_number, master_password, website, username, password):
        # Authenticate user before adding password
        user_id = self.authenticate_user(phone_number, master_password)
        if not user_id:
            return False
            
        try:
            conn = sqlite3.connect('passwords.db')
            cursor = conn.cursor()
            
            # Save password
            cursor.execute(
                "INSERT INTO passwords (user_id, website, username, password) VALUES (?, ?, ?, ?)",
                (user_id, website, username, password)
            )
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            return False
            
    def get_passwords(self, user_id):
        try:
            conn = sqlite3.connect('passwords.db')
            cursor = conn.cursor()
            
            # Get passwords
            cursor.execute(
                "SELECT website, username, password FROM passwords WHERE user_id = ?",
                (user_id,)
            )
            passwords = cursor.fetchall()
            
            conn.close()
            return passwords
        except Exception as e:
            return []

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerGUI(root)
    root.mainloop() 