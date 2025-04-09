# Secure Password Manager

A secure password manager application with phone number verification and OTP-based authentication.

## Features

- User registration with phone number
- OTP-based authentication
- Secure password storage
- Modern and attractive GUI
- Easy password management

## Requirements

- Python 3.7 or higher
- Required Python packages (install using `pip install -r requirements.txt`):
  - customtkinter
  - pillow
  - twilio (for OTP functionality)

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

1. Run the application:
```bash
python password_manager.py
```

2. Register with your phone number
3. Login with your registered phone number
4. You'll receive an OTP for verification
5. After successful verification, you can:
   - Add new passwords
   - View your saved passwords
   - Logout

## Security Features

- Phone number verification
- OTP-based authentication
- Secure password storage in SQLite database
- Passwords are masked in the interface

## Note

For OTP functionality to work, you'll need to:
1. Sign up for a Twilio account
2. Get your Account SID and Auth Token
3. Update the Twilio credentials in the code

Currently, the OTP is printed to the console for testing purposes. In a production environment, you would use Twilio to send actual SMS messages.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 