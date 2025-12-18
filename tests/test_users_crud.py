import pytest

class TestUsersCRUD:
    """Tests for CRUD operations on users table"""
    
    def test_create_user(self, db_connection):
        """Test: Create a new user"""
        cursor = db_connection.cursor()
        
        cursor.execute("""
            INSERT INTO users (username, email, age)
            VALUES (%s, %s, %s)
            RETURNING id
        """, ('testuser', 'test@example.com', 25))
        
        user_id = cursor.fetchone()[0]
        
        assert user_id is not None
        assert user_id > 0
        
        cursor.close()
        print(f"User created with ID: {user_id}")
    
    def test_read_user(self, db_connection):
        """Test: Read user data"""
        cursor = db_connection.cursor()
        
        # Create user first
        cursor.execute("""
            INSERT INTO users (username, email, age)
            VALUES (%s, %s, %s)
            RETURNING id
        """, ('readuser', 'read@example.com', 30))
        user_id = cursor.fetchone()[0]
        
        # Read user
        cursor.execute("""
            SELECT username, email, age FROM users WHERE id = %s
        """, (user_id,))
        
        result = cursor.fetchone()
        
        assert result[0] == 'readuser'
        assert result[1] == 'read@example.com'
        assert result[2] == 30
        
        cursor.close()
        print(f"User read correctly: {result[0]}")
    
    def test_update_user(self, db_connection):
        """Test: Update user data"""
        cursor = db_connection.cursor()
        
        # Create user
        cursor.execute("""
            INSERT INTO users (username, email, age)
            VALUES (%s, %s, %s)
            RETURNING id
        """, ('updateuser', 'update@example.com', 28))
        user_id = cursor.fetchone()[0]
        
        # Update email and age
        cursor.execute("""
            UPDATE users 
            SET email = %s, age = %s 
            WHERE id = %s
        """, ('newemail@example.com', 29, user_id))
        
        # Verify update
        cursor.execute("""
            SELECT email, age FROM users WHERE id = %s
        """, (user_id,))
        
        result = cursor.fetchone()
        
        assert result[0] == 'newemail@example.com'
        assert result[1] == 29
        
        cursor.close()
        print("User updated correctly")
    
    def test_delete_user(self, db_connection):
        """Test: Delete user"""
        cursor = db_connection.cursor()
        
        # Create user
        cursor.execute("""
            INSERT INTO users (username, email, age)
            VALUES (%s, %s, %s)
            RETURNING id
        """, ('deleteuser', 'delete@example.com', 35))
        user_id = cursor.fetchone()[0]
        
        # Delete user
        cursor.execute("""
            DELETE FROM users WHERE id = %s
        """, (user_id,))
        
        # Verify deletion
        cursor.execute("""
            SELECT COUNT(*) FROM users WHERE id = %s
        """, (user_id,))
        
        count = cursor.fetchone()[0]
        
        assert count == 0
        
        cursor.close()
        print("User deleted correctly")
    
    def test_read_all_users(self, db_connection):
        """Test: Read multiple users"""
        cursor = db_connection.cursor()
        
        # Create 3 users
        users_data = [
            ('user1', 'user1@example.com', 20),
            ('user2', 'user2@example.com', 25),
            ('user3', 'user3@example.com', 30)
        ]
        
        for username, email, age in users_data:
            cursor.execute("""
                INSERT INTO users (username, email, age)
                VALUES (%s, %s, %s)
            """, (username, email, age))
        
        # Read all users
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        
        assert count >= 3
        
        cursor.close()
        print(f"{count} users found in DB")
        
        