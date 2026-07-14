# CS50W Commerce - Project Setup and Database Seeding

This guide explains how to set up the project locally and populate it with dummy test data.

## 1. Install Dependencies

Before running the project for the first time, install the required packages:

```bash
python3 -m pip install -r requirements.txt
```

## 2. Create and Apply Database Migrations

To initialize the SQLite database, run the following commands:

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

## 3. Seed the Database with Dummy Data

The project includes a custom management command that populates the database with Harry Potter themed wizards, categories, listings, and pre-populates them with random bids and comments.

Run the following command:

```bash
python3 manage.py seed_data
```

### Pre-created Test Accounts

All created accounts use the same password: `test`

* **Harry Potter** – harry@hogwarts.edu
* **Ron Weasley** – ron@hogwarts.edu
* **Hermione Granger** – hermione@hogwarts.edu
* **Draco Malfoy** – malfoy@hogwarts.edu

## 4. Run the Local Development Server

Start the local development server:

```bash
python3 manage.py runserver
```

The application will be accessible at http://127.0.0.1:8000/.
