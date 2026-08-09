
# Real Estate System

The **Real Estate System** is an application designed to streamline the management, rental, listing, and sale of real estate properties. The platform allows real estate agents, property owners, and potential buyers to interact seamlessly, facilitating property searches, listing management, and transactions in a user-friendly and efficient manner.

## Features

- **Property Listings**: Property owners or agents can easily list properties with detailed descriptions, prices, and images.
- **Advanced Search**: Potential buyers can search for properties using various filters like location, price range, property type, and size.
- **User Roles**: The system supports multiple user types such as administrators, property owners, and buyers, each with different permissions.
- **Interactive Map**: Properties are displayed on an interactive map to enhance the user experience and help users find properties by location.
- **Favorites**: Users can save properties to their favorites for quick access later.
- **Messaging**: Direct messaging system between property owners/agents and buyers for inquiries.(TBD)
- **Responsive Design**: Fully responsive, ensuring a seamless experience across desktop, tablet, and mobile devices.
- **Admin Panel**: Comprehensive administrative panel for managing users, properties, transactions, and more.
- **Secure Transactions**: Secure handling of property transactions, ensuring data privacy and integrity.
  
## Technologies Used

- **main**: Django (filters, rest_framework, )
- **Frontend**: JavaScript (React, nextjs)
- **Database**: SQLite for local development, PostgreSQL for production
- **Authentication**: JWT / OAuth for secure login and user management
- **Deployment**: Docker, Nginx, and Gunicorn for scalable production deployment

## Setup and Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/trent130/hello.git
    ```

2. Navigate to the project directory:
    ```bash
    cd hello
    ```
3. setUp a virtual environment:
    ### on window:
    ```bash
    python -m venv .venv
    ```
    ### on linux:
    ```bash
    python -m venv .venv
    ```

4. Install the dependencies:
    ```
    pip install -r requirements.txt
    ```

5. Set up your environment variables:
    ```bash
    cp .env.example .env
    ```
    Update `SECRET_KEY`, allowed hosts, CORS, CSRF, email, and database settings for your environment. Keep `DEBUG=False` in production.

6. Install the frontend dependencies:
    ```bash
    cd frontend
    cp .env.example .env.local
    npm ci
    cd ..
    ```

7. Run the development server:
    ```bash
    python manage.py runserver
    ```

8. In a second terminal, run the frontend:
    ```bash
    cd frontend
    npm run dev
    ```

9. Access the application at `http://localhost:3000`.
Additionally, you'll need the following setup

# Production database setup

This section provides instructions on how to set up PostgreSQL for this project.

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- [PostgreSQL](https://www.postgresql.org/download/) (version 13.X or higher)
- [pgAdmin](https://www.pgadmin.org/download/) (optional, for GUI management)
- [python django](https://djangoproject.com/)(preferably in a a virtual environment)

## Installation

### Step 1: Install PostgreSQL

1. Download the PostgreSQL installer for your operating system from the [official website](https://www.postgresql.org/download/).
2. Run the installer and follow the prompts to complete the installation.
3. During installation, you will be prompted to set a password for the default `postgres` user. Make sure to remember this password.

### Step 2: Start PostgreSQL Service

- **On Windows:**
  - PostgreSQL should start automatically. If not, you can start it from the Services application.
  
- **On macOS:**
  ```bash
  brew services start postgresql
  ```

- **On Linux:**
  ```bash
  sudo systemctl start postgresql
  ```
  or
  ``` bash
  sudo service postgresql start
  ```
### Step 3: Create a Database

1. Open the PostgreSQL command line interface (CLI) or pgAdmin.
2. Connect to the PostgreSQL server using the `postgres` user:
   ```bash
   psql -U postgres
   ```
   Enter the password you set during installation.

3. Create a new database for your project:
   ```sql
   CREATE DATABASE your_database_name;
   ```

4. (Optional) Create a new user with access to the database:
   ```sql
   CREATE USER your_username WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE your_database_name TO your_username;
   ```

### Step 4: Configure Database Connection

Set the database backend through environment variables. SQLite remains the default for local development. For PostgreSQL, use:

```plaintext
DB_ENGINE=django.db.backends.postgresql
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
DB_CONN_MAX_AGE=60
```

The PostgreSQL driver is included in `requirements.txt`. Run migrations after the database is reachable:

```bash
python manage.py migrate --noinput
python manage.py collectstatic --noinput
```

### Step 5: Run Migrations

Run the migrations to set up the database schema:

```bash
# Apply the database schema
python manage.py migrate --noinput
```

## Production operations

- Configure `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, `CSRF_TRUSTED_ORIGINS`, a strong `SECRET_KEY`, and secure cookie/HTTPS settings through the environment.
- Set `USE_S3=True` and the `AWS_*` variables in `.env` when media must survive container replacement. The default filesystem storage is suitable only for a persistent local volume.
- Point the load balancer or process supervisor at `GET /health/`. It returns HTTP 200 only when Django can reach the configured database and HTTP 503 otherwise.
- The repository quality workflow runs migration drift checks, Django checks/tests, frontend linting, TypeScript validation, and the production frontend build on pushes and pull requests.
- Payment and transaction records are read-only until a real payment provider, signed callback endpoint, reconciliation process, and escrow policy are configured. The application does not fabricate successful payments.

## Troubleshooting

- If you encounter issues connecting to the database, ensure that the PostgreSQL service is running and that you are using the correct credentials.
- Check the PostgreSQL logs for any error messages that can help diagnose the problem.

## Additional Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [pgAdmin Documentation](https://www.pgadmin.org/docs/)


Feel free to modify the instructions to better fit your project's needs.
## Contributing

We welcome contributions! If you'd like to contribute, please fork the repository and submit a pull request with your changes. Be sure to update documentation as needed.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
