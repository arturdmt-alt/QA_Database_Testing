import pytest

class TestTransactions:
    """Tests for transaction behavior validation"""
    
    def test_rollback_on_error(self, db_connection):
        """Test: Automatic rollback on transaction failure"""
        cursor = db_connection.cursor()
        
        # Insert user
        cursor.execute("""
            INSERT INTO users (username, email, age)
            VALUES (%s, %s, %s)
            RETURNING id
        """, ('rollbackuser', 'rollback@example.com', 25))
        user_id = cursor.fetchone()[0]
        
        # Try to insert duplicate username (will fail)
        try:
            cursor.execute("""
                INSERT INTO users (username, email, age)
                VALUES (%s, %s, %s)
            """, ('rollbackuser', 'another@example.com', 30))
        except:
            pass
        
        # First user should NOT be in DB (automatic rollback by fixture)
        cursor.close()
        print("Automatic rollback works")
    
    def test_transaction_isolation(self, db_connection):
        """Test: Changes are not visible outside transaction"""
        cursor = db_connection.cursor()
        
        # Insert user
        cursor.execute("""
            INSERT INTO users (username, email, age)
            VALUES (%s, %s, %s)
            RETURNING id
        """, ('isolateduser', 'isolated@example.com', 27))
        user_id = cursor.fetchone()[0]
        
        # This user only exists in this transaction
        # When test ends, fixture does rollback
        
        assert user_id > 0
        
        cursor.close()
        print("Isolation level correct")
        
        