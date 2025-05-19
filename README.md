# MedicalScan

A medical prescription scanning and management application built with Kivy and KivyMD.

## Features

- User authentication (login, signup, password reset)
- Prescription scanning and OCR
- Prescription history and details view
- User profile management
- Settings customization

## Setup

1. Clone the repository
   ```
   git clone https://github.com/SagitaKDX/MedicalScan.git
   cd MedicalScan
   ```

2. Create a virtual environment
   ```
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Run the application
   ```
   python main.py
   ```

## Requirements

- Python 3.7+
- Kivy
- KivyMD
- Other dependencies listed in requirements.txt

## Tech Stack

- **Frontend**: Kivy/KivyMD (Python-based UI framework)
- **Backend**: Python
- **Database**: MySQL (XAMPP)
- **Email Service**: SMTP

## Project Structure

```
MedicalScan/
├── assets/              # Static assets (images, icons)
├── controllers/         # Application controllers
├── models/             # Data models
├── services/           # Business logic and services
├── views/              # UI components and screens
│   ├── components/     # Reusable UI components
│   └── screens/        # Application screens
├── main.py            # Application entry point
├── medical.kv         # Kivy UI definitions
├── styles.kv          # Global styles
├── themes.py          # Theme configurations
├── test.py           # Test application
├── .env              # Environment variables
└── database.sql      # Database schema
```

## Development

### Screen Structure
- Login Screen
- Signup Screen
- Verification Screen
- Home Screen
- History Screen
- Prescription Detail Screen
- Scan Screen

### UI Components
- Custom Text Input
- Password Field
- Primary Button
- Text Button
- Navigation Bar

### Theme
The application uses a custom theme with the following color scheme:
- Primary Color: #406D96
- Primary Dark: #2F3A56
- Background: #F5F5F5
- Error: #FF4444
- Text: #333333
- Hint: #999999

## Database Configuration

The application uses MySQL database through XAMPP. Make sure to:

1. Start XAMPP Control Panel
2. Enable MySQL server
3. Create database named 'mediscan'
4. Import the database schema from database.sql
5. Configure database credentials in .env file

## Testing

The project includes a test application (`test.py`) that can be used for development and testing purposes. It provides a simplified environment for testing specific features.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.