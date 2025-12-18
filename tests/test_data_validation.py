import pytest
from psycopg2 import IntegrityError

class TestDataValidation:
    """Tests for database constraint validation"""
    
    def test_unique_username_constraint(self, db_connection):
        """Test: Duplicate username should fail"""
        cursor = db_connection.cursor()
        
        # Create first user
        cursor.execute("""
            INSERT INTO users (username, email, age)
            VALUES (%s, %s, %s)
        """, ('uniqueuser', 'first@example.com', 25))
        
        # Try to create duplicate username
        with pytest.raises(IntegrityError):
            cursor.execute("""
                INSERT INTO users (username, email, age)
                VALUES (%s, %s, %s)
            """, ('uniqueuser', 'second@example.com', 30))
        
        cursor.close()
        print("UNIQUE username constraint works")
    
    def test_unique_email_constraint(self, db_connection):
        """Test: Duplicate email should fail"""
        cursor = db_connection.cursor()
        
        # Create first user
        cursor.execute("""
            INSERT INTO users (username, email, age)
            VALUES (%s, %s, %s)
        """, ('user1', 'same@example.com', 25))
        
        # Try to create duplicate email
        with pytest.raises(IntegrityError):
            cursor.execute("""
                INSERT INTO users (username, email, age)
                VALUES (%s, %s, %s)
            """, ('user2', 'same@example.com', 30))
        
        cursor.close()
        print("UNIQUE email constraint works")
    
    def test_not_null_username(self, db_connection):
        """Test: NULL username should fail"""
        cursor = db_connection.cursor()
        
        with pytest.raises(IntegrityError):
            cursor.execute("""
                INSERT INTO users (username, email, age)
                VALUES (%s, %s, %s)
            """, (None, 'test@example.com', 25))
        
        cursor.close()
        print("NOT NULL username constraint works")
    
    def test_foreign_key_constraint(self, db_connection):
        """Test: Order with non-existent user_id should fail"""
        cursor = db_connection.cursor()
        
        # Try to create order with non-existent user_id
        with pytest.raises(IntegrityError):
            cursor.execute("""
                INSERT INTO orders (user_id, product_name, quantity, total_price)
                VALUES (%s, %s, %s, %s)
            """, (99999, 'Test Product', 1, 10.00))
        
        cursor.close()
        print("FOREIGN KEY constraint works")
    
    def test_check_constraint_quantity(self, db_connection):
        """Test: Quantity less than or equal to 0 should fail"""
        cursor = db_connection.cursor()
        
        # Create user first
        cursor.execute("""
            INSERT INTO users (username, email, age)
            VALUES (%s, %s, %s)
            RETURNING id
        """, ('orderuser', 'order@example.com', 25))
        user_id = cursor.fetchone()[0]
        
        # Try to create order with negative quantity
        with pytest.raises(IntegrityError):
            cursor.execute("""
                INSERT INTO orders (user_id, product_name, quantity, total_price)
                VALUES (%s, %s, %s, %s)
            """, (user_id, 'Test Product', -5, 10.00))
        
        cursor.close()
        print("CHECK quantity constraint works")
    
    def test_cascade_delete(self, db_connection):
        """Test: Deleting user should delete their orders (CASCADE)"""
        cursor = db_connection.cursor()
        
        # Create user
        cursor.execute("""
            INSERT INTO users (username, email, age)
            VALUES (%s, %s, %s)
            RETURNING id
        """, ('cascadeuser', 'cascade@example.com', 30))
        user_id = cursor.fetchone()[0]
        
        # Create order for that user
        cursor.execute("""
            INSERT INTO orders (user_id, product_name, quantity, total_price)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (user_id, 'Test Product', 2, 20.00))
        order_id = cursor.fetchone()[0]
        
        # Delete user
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        
        # Verify order was also deleted
        cursor.execute("SELECT COUNT(*) FROM orders WHERE id = %s", (order_id,))
        count = cursor.fetchone()[0]
        
        assert count == 0
        
        cursor.close()
        print("CASCADE DELETE works correctly")
        
