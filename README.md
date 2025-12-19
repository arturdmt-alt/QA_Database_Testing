# Database Testing Framework - PostgreSQL

![Tests](https://img.shields.io/badge/tests-16%20passing-brightgreen)
![Python](https://img.shields.io/badge/python-3.11-blue)
![PostgreSQL](https://img.shields.io/badge/postgresql-18-blue)
![pytest](https://img.shields.io/badge/pytest-9.0-orange)

Professional database testing framework using pytest and PostgreSQL with comprehensive CRUD, validation, and transaction testing.

## Features

- CRUD operation testing for users and orders
- Data validation testing with constraints
- Transaction isolation with automatic rollback
- Complex SQL queries including JOINs and aggregations
- Professional test organization and fixtures
- Comprehensive HTML reporting

## Test Coverage

| Test Suite | Description | Tests |
|------------|-------------|-------|
| Users CRUD | Create, read, update, delete users | 5 tests |
| Data Validation | Constraints, foreign keys, cascades | 6 tests |
| Orders CRUD | Orders with JOINs and aggregations | 3 tests |
| Transactions | Rollback and isolation testing | 2 tests |

**Total: 16 tests passing in less than 1 second**

## Tech Stack

- Python 3.11
- pytest 9.0
- PostgreSQL 18
- psycopg2-binary
- python-dotenv
- pytest-html

## Database Schema
```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    age INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders table
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    product_name VARCHAR(100) NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    total_price DECIMAL(10,2) NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Installation

**Clone and setup:**
```bash
git clone https://github.com/arturdmt-alt/QA_Database_Testing.git
cd QA_Database_Testing
```

**Create virtual environment:**
```bash
python -m venv venv
```

**Activate virtual environment:**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Setup PostgreSQL (Option A: Local):**
- Install from postgresql.org

**Setup PostgreSQL (Option B: Docker - Recommended):**
```bash
docker run --name qa-postgres -e POSTGRES_PASSWORD=testpass -p 5432:5432 -d postgres:15
```

**Configure environment:**

Create `.env` file:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_password
```

## Running Tests
```bash
# Run all tests
pytest tests/ -v

# Run with HTML report
pytest tests/ -v --html=reports/report.html --self-contained-html

# Run specific test file
pytest tests/test_users_crud.py -v

# Run with verbose output
pytest tests/ -v -s
```

## Key Implementation Details

### Test Isolation with Automatic Rollback

Each test runs in its own transaction that automatically rolls back after completion:
```python
@pytest.fixture(scope='function')
def db_connection():
    conn = DatabaseConfig.get_connection()
    conn.autocommit = False
    
    yield conn
    
    # Automatic rollback after each test
    conn.rollback()
    conn.close()
```

**Benefits:**
- Tests do not interfere with each other
- No manual cleanup needed
- Fast test execution
- Database stays clean between tests

### Database Schema Setup

Schema is created once before all tests and cleaned up after:
```python
@pytest.fixture(scope='session', autouse=True)
def setup_test_database():
    conn = DatabaseConfig.get_connection()
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute("""CREATE TABLE IF NOT EXISTS users...""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS orders...""")
    
    conn.commit()
    yield
    
    # Cleanup
    cursor.execute("DROP TABLE IF EXISTS orders CASCADE")
    cursor.execute("DROP TABLE IF EXISTS users CASCADE")
    conn.commit()
```

### Constraint Testing

Tests validate all database constraints:
- UNIQUE constraints on username and email
- NOT NULL constraints
- FOREIGN KEY relationships
- CHECK constraints on quantity
- CASCADE DELETE behavior

### Complex SQL Queries

Tests include advanced SQL operations:
- JOINs between users and orders
- Aggregate functions (SUM, COUNT)
- Transaction isolation
- Multi-row operations

## Test Results
```
tests/test_data_validation.py::TestDataValidation::test_unique_username_constraint PASSED
tests/test_data_validation.py::TestDataValidation::test_unique_email_constraint PASSED
tests/test_data_validation.py::TestDataValidation::test_not_null_username PASSED
tests/test_data_validation.py::TestDataValidation::test_foreign_key_constraint PASSED
tests/test_data_validation.py::TestDataValidation::test_check_constraint_quantity PASSED
tests/test_data_validation.py::TestDataValidation::test_cascade_delete PASSED
tests/test_orders_crud.py::TestOrdersCRUD::test_create_order PASSED
tests/test_orders_crud.py::TestOrdersCRUD::test_read_order_with_user PASSED
tests/test_orders_crud.py::TestOrdersCRUD::test_calculate_total_orders_by_user PASSED
tests/test_transactions.py::TestTransactions::test_rollback_on_error PASSED
tests/test_transactions.py::TestTransactions::test_transaction_isolation PASSED
tests/test_users_crud.py::TestUsersCRUD::test_create_user PASSED
tests/test_users_crud.py::TestUsersCRUD::test_read_user PASSED
tests/test_users_crud.py::TestUsersCRUD::test_update_user PASSED
tests/test_users_crud.py::TestUsersCRUD::test_delete_user PASSED
tests/test_users_crud.py::TestUsersCRUD::test_read_all_users PASSED

================= 16 passed in 0.96s =================
```

View full HTML report: `reports/report.html`

## Test Execution Evidence

### Terminal Output
![Terminal Tests](./screenshots/terminal_report_database.jpg)

### HTML Report Summary
![HTML Report](./screenshots/html_report_data_base2.jpg)

### Environment Details
![Environment](./screenshots/html_report_data_base.jpg)


## Project Structure

## Project Structure
```
QA_Database_Testing/
├── config/
│   ├── __init__.py   
│   └── database.py               # Database connection configuration
├── tests/
│   ├── test_users_crud.py        # User CRUD operations
│   ├── test_data_validation.py   # Constraint validation
│   ├── test_orders_crud.py       # Orders with JOINs
│   └── test_transactions.py      # Transaction testing
├── screenshots/                  # Test execution evidence
├── reports/                      # HTML test reports
├── conftest.py                   # Pytest fixtures
├── .env                          # Database credentials
├── .gitignore
├── requirements.txt
└── README.md
```

## Author

**Artur Dmytriyev**  
QA Automation Engineer

[LinkedIn](https://www.linkedin.com/in/arturdmytriyev/) 
[GitHub](https://github.com/arturdmt-alt)

## Project Notes

This framework demonstrates:
- Professional database testing patterns
- Transaction isolation strategies
- Comprehensive constraint validation
- Complex SQL query testing
- Clean code organization with fixtures
- Production-ready test automation

Designed for QA positions requiring database testing expertise at companies like EA Games, Google, and enterprise organizations.

## Future Enhancements

- CI/CD integration with GitHub Actions
- Docker Compose for complete environment setup
- Additional test coverage for stored procedures
- Performance testing for large datasets
- Integration with test management tools

---

Last updated: December 2025
