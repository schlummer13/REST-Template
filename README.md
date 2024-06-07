
# FastAPI REST Template

Welcome to my FastAPI REST Template! This API is suitable for small applications and provides basic functionalities like login, registration, password recovery, contact forms, and more. The project serves as a training exercise for creating and managing a REST API with FastAPI.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Mail Functionality](#mail-functionality)
- [Database](#database)
- [Website](#website)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/schlummer13/REST-Template
    ```

2. Install the required packages:
    ```bash
    pip install -r app/requirements.txt
    ```

## Usage

Start the application with uvicorn:
```bash
uvicorn app.main:app --reload
```

## Mail Functionality

When endpoints such as registration are called, a confirmation email is sent to the user. The mail functionality is already integrated and configured.

## Database

The default database is SQLite, and database operations are performed using Peewee. The database can be changed if needed.

## Website

For more information, please visit my website: [somebot.de](https://www.somebot.de)

## License

This project is licensed under the terms of the MIT license. For more details, see the `LICENSE` file.

---

This project is intended for training purposes and serves as a foundation for creating and managing a REST API with FastAPI and Peewee.
