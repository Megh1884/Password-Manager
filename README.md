# Secure Password Manager

A secure password manager application with master password authentication and a modern GUI.

## Features

- User registration with phone number and master password
- Master password authentication for secure access
- Store website credentials securely
- Modern, attractive graphical user interface
- Command-line interface option
- Password hashing using SHA-256
- SQLite database for local storage

## Project Structure

- **password_manager.py** - Command-line version of the password manager
- **password_manager_gui.py** - Graphical user interface version
- **requirements.txt** - Required dependencies

## Requirements

- Python 3.7 or higher
- Required Python packages (install using `pip install -r requirements.txt`):
  - tkinter (included with Python)
  - customtkinter
  - pillow

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Megh1884/Password-Manager.git
cd Password-Manager
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

### GUI Version

1. Run the GUI application:
```bash
python password_manager_gui.py
```

2. Register with your phone number and create a master password
3. Add passwords for different websites
4. View your passwords by authenticating with your master password

### Command-Line Version

1. Run the command-line application:
```bash
python password_manager.py
```

2. Follow the text-based menu to:
   - Register a new user
   - Add new passwords
   - View your saved passwords
   - Exit the application

## Security Features

- Master password authentication
- Password hashing with SHA-256
- Secure local storage with SQLite
- Database file excluded from Git repository
- Passwords are masked in the interface

## Screenshots

(Add screenshots of your application here)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## About

This project was created as a cybersecurity demonstration for secure password management. It shows how to implement basic security features like password hashing and master password authentication. 