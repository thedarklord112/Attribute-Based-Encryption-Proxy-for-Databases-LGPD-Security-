import unittest
from src.proxy import DatabaseCryptoProxy

class TestDatabaseCryptoProxy(unittest.TestCase):
    def setUp(self):
        self.proxy = DatabaseCryptoProxy()
        self.mock_insert_query = "INSERT INTO users (name, credit_card, ssn_tax_id) VALUES (%s, %s, %s)"
        self.mock_select_query = "SELECT name, credit_card, ssn_tax_id FROM users"
        self.raw_card = "1234567890123456"
        self.raw_ssn = "00011122233"

    def test_end_to_end_encryption_and_rbac_masking(self):
        # 1. Simulate data interception before writing to database
        raw_values = ["John Doe", self.raw_card, self.raw_ssn]
        db_encrypted_values = self.proxy.process_incoming_insert(self.mock_insert_query, raw_values)

        # Assert data was successfully encrypted into hex and is no longer exposed in cleartext
        self.assertNotEqual(db_encrypted_values[1], self.raw_card)
        self.assertNotEqual(db_encrypted_values[2], self.raw_ssn)

        # Simulate how rows are saved inside a standard PostgreSQL instance
        mock_db_table_state = [{
            "name": "John Doe",
            "credit_card": db_encrypted_values[1],
            "ssn_tax_id": db_encrypted_values[2]
        }]

        # 2. Assert Admin Role receives full clear-text decrypted output payload
        admin_output = self.proxy.process_outgoing_results(
            self.mock_select_query, "users", mock_db_table_state, user_role="admin"
        )
        self.assertEqual(admin_output[0]["credit_card"], self.raw_card)
        self.assertEqual(admin_output[0]["ssn_tax_id"], self.raw_ssn)

        # 3. Assert Support Role receives partial data masking constraints
        support_output = self.proxy.process_outgoing_results(
            self.mock_select_query, "users", mock_db_table_state, user_role="support"
        )
        self.assertEqual(support_output[0]["credit_card"], "XXXX-XXXX-XXXX-3456")
        self.assertEqual(support_output[0]["ssn_tax_id"], "XXX-XX-233")

if __name__ == "__main__":
    unittest.main()
