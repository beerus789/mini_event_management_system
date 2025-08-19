
# Mini Event Management System

This project is a Mini Event Management System API designed with clean architecture, scalability, and data integrity in mind.

## Features
- Event creation and management
- User registration and authentication
- API endpoints for CRUD operations
- Modular code structure (core, db, models, repositories, services, api)

## Project Structure
```
assesment/
  app/
    main.py
    requirements.txt
    api/
    core/
    db/
    models/
    repositories/
    services/
    tests/
  event.db
```

## Setup Instructions
1. **Clone the repository:**
   ```powershell
   git clone <repo-url>
   cd mini_event_management_system
   ```
2. **Create and activate a virtual environment (optional but recommended):**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```powershell
   pip install -r assesment/app/requirements.txt
   ```
4. **Run the application:**
   ```powershell
   python assesment/app/main.py
   ```

## Database
The default database is `event.db` (SQLite). You can change the configuration in `assesment/app/db/database.py`.

## Testing
Tests are located in `assesment/app/tests/`. To run tests:
```powershell
pytest assesment/app/tests/
```

## Contributing
Feel free to fork the repository and submit pull requests.

