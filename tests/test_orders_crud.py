import pytest
from decimal import Decimal

class TestOrdersCRUD:
    """Tests for CRUD operations on orders table"""
    
    def test_create_order(self, db_connection):
        """Test: Create an order"""
        cursor = db_connection.cursor()
        
        # Create user first
        cursor.execute("""
            INSERT INTO users (username, email, age)
            VALUES (%s, %s, %s)
            RETURNING id
        """, ('buyeruser', 'buyer@example.com', 28))
        user_id = cursor.fetchone()[0]
        
        # Create order
        cursor.execute("""
            INSERT INTO orders (user_id, product_name, quantity, total_price)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (user_id, 'Laptop', 1, 999.99))
        
        order_id = cursor.fetchone()[0]
        
        assert order_id is not None
        assert order_id > 0
        
        cursor.close()
        print(f"Order created with ID: {order_id}")
    
    def test_read_order_with_user(self, db_connection):
        """Test: Read order with user data (JOIN)"""
        cursor = db_connection.cursor()
        
        # Create user
        cursor.execute("""
            INSERT INTO users (username, email, age)
            VALUES (%s, %s, %s)
            RETURNING id
        """, ('joinuser', 'join@example.com', 32))
        user_id = cursor.fetchone()[0]
        
        # Create order
        cursor.execute("""
            INSERT INTO orders (user_id, product_name, quantity, total_price)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (user_id, 'Mouse', 2, 50.00))
        order_id = cursor.fetchone()[0]
        
        # JOIN to read order with user
        cursor.execute("""
            SELECT o.id, o.product_name, o.quantity, o.total_price,
                   u.username, u.email
            FROM orders o
            JOIN users u ON o.user_id = u.id
            WHERE o.id = %s
        """, (order_id,))
        
        result = cursor.fetchone()
        
        assert result[1] == 'Mouse'
        assert result[4] == 'joinuser'
        assert result[5] == 'join@example.com'
        
        cursor.close()
        print("JOIN orders + users works correctly")
    
    def test_calculate_total_orders_by_user(self, db_connection):
        """Test: Calculate total orders by user (SUM)"""
        cursor = db_connection.cursor()
        
        # Create user
        cursor.execute("""
            INSERT INTO users (username, email, age)
            VALUES (%s, %s, %s)
            RETURNING id
        """, ('totaluser', 'total@example.com', 40))
        user_id = cursor.fetchone()[0]
        
        # Create multiple orders
        orders = [
            ('Product A', 1, 100.00),
            ('Product B', 2, 50.00),
            ('Product C', 1, 150.00)
        ]
        
        for product, qty, price in orders:
            cursor.execute("""
                INSERT INTO orders (user_id, product_name, quantity, total_price)
                VALUES (%s, %s, %s, %s)
            """, (user_id, product, qty, price))
        
        # Calculate total
        cursor.execute("""
            SELECT SUM(total_price) as total
            FROM orders
            WHERE user_id = %s
        """, (user_id,))
        
        total = cursor.fetchone()[0]
        
        assert float(total) == 300.00
        
        cursor.close()
        print(f"Total calculated: ${total}")
        