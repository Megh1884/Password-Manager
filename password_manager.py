import sqlite3
import re
import os
import hashlib

class PasswordManager:
    def __init__(self):
        self.init_database()

    def validate_phone_number(self, phone_number):
        # Remove any spaces or special characters
        phone_number = re.sub(r'[^0-9+]', '', phone_number)
            
        # Basic validation
        if len(phone_number) < 10:
            print("\nError: Phone number is too short")
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
                print("\nUpdating database schema...")
                # Create a new users table with updated schema
                cursor.execute('''
                    CREATE TABLE users_new (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        phone_number TEXT UNIQUE,
                        master_password TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # For existing users, we'll need them to set a master password
                print("\nNOTE: Database schema has been updated.")
                print("Existing users will need to re-register with a master password.")
                
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
            print("\nError: Master password must be at least 6 characters long")
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
            print("Registration successful!")
            return True
        except sqlite3.IntegrityError:
            print("Phone number already registered")
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
                print("Phone number not registered")
                return False
            
            user_id, stored_password = user
            
            # Hash the provided password and compare
            if self.hash_password(master_password) == stored_password:
                return user_id
            else:
                print("Invalid master password")
                return False
                
        except Exception as e:
            print(f"Error: {str(e)}")
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
            print("Password saved successfully!")
            return True
        except Exception as e:
            print(f"Error: {str(e)}")
            return False

    def view_passwords(self, phone_number, master_password):
        # Authenticate user before viewing passwords
        user_id = self.authenticate_user(phone_number, master_password)
        if not user_id:
            return False
        
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
            
            if not passwords:
                print("No passwords saved yet")
                return True
            
            print("\nYour saved passwords:")
            print("-" * 50)
            for website, username, password in passwords:
                print(f"Website: {website}")
                print(f"Username: {username}")
                print(f"Password: {password}")
                print("-" * 50)
            
            return True
        except Exception as e:
            print(f"Error: {str(e)}")
            return False

def main():
    # Check if this might be the first run
    if not os.path.exists('passwords.db'):
        print("\n" + "="*60)
        print("WELCOME TO PASSWORD MANAGER")
        print("="*60)
        print("\nThis application allows you to securely store and retrieve your passwords.")
        print("You'll need to create a master password to protect all your saved passwords.")
        print("="*60)
        print("\nPress Enter to continue...")
        input()
        
    pm = PasswordManager()
    
    while True:
        print("\n===== Password Manager =====")
        print("1. Register")
        print("2. Add Password")
        print("3. View Passwords")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == "1":
            phone = input("Enter your phone number: ")
            master_password = input("Create a master password (min 6 characters): ")
            confirm_password = input("Confirm master password: ")
            
            if master_password != confirm_password:
                print("Passwords do not match!")
                continue
                
            pm.register_user(phone, master_password)
            
        elif choice == "2":
            phone = input("Enter your registered phone number: ")
            master_password = input("Enter your master password: ")
            website = input("Enter website: ")
            username = input("Enter username: ")
            password = input("Enter password: ")
            pm.add_password(phone, master_password, website, username, password)
            
        elif choice == "3":
            phone = input("Enter your registered phone number: ")
            master_password = input("Enter your master password: ")
            pm.view_passwords(phone, master_password)
                
        elif choice == "4":
            print("\nThank you for using Password Manager. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 