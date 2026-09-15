from typing import Dict, Any, List
from src.crypto_engine import CryptoEngine
from src.query_parser import SQLQueryInterceptor
from src.config import ProxyConfig

class DatabaseCryptoProxy:
    def __init__(self):
        self.engine = CryptoEngine(ProxyConfig.MASTER_KEY_HEX)
        self.interceptor = SQLQueryInterceptor()

    def process_incoming_insert(self, query: str, values: List[Any]) -> List[Any]:
        """Intercepts an INSERT statement and encrypts sensitive fields before database storage."""
        table, columns = self.interceptor.parse_insert(query)
        if not table or table not in ProxyConfig.PROTECTED_COLUMNS:
            return values

        protected_fields = ProxyConfig.PROTECTED_COLUMNS[table]
        encrypted_values = list(values)

        for idx, col in enumerate(columns):
            if col in protected_fields and idx < len(encrypted_values):
                # Encrypt data straight into an obfuscated hex string
                encrypted_values[idx] = self.engine.encrypt_data(str(encrypted_values[idx]))

        return encrypted_values

    def apply_mask(self, field_name: str, value: str) -> str:
        """Applies partial masking formats depending on field constraints."""
        if not value:
            return value
        if field_name == "credit_card":
            # Masking format: XXXX-XXXX-XXXX-1234
            return f"XXXX-XXXX-XXXX-{value[-4:]}" if len(value) >= 4 else "XXXX-INVALID"
        if field_name == "ssn_tax_id":
            # Masking format: XXX-XX-6789
            return f"XXX-XX-{value[-4:]}" if len(value) >= 4 else "XXX-INVALID"
        return "XXXX-MASKED"

    def process_outgoing_results(self, query: str, table: str, database_rows: List[Dict[str, Any]], user_role: str) -> List[Dict[str, Any]]:
        """Intercepts selected database output rows and decrypts/masks based on attribute-roles."""
        protected_fields = self.interceptor.identify_select_columns(query, table)
        if not protected_fields or not database_rows:
            return database_rows

        is_authorized = user_role.lower() in ProxyConfig.AUTHORIZED_ROLES
        processed_rows = []

        for row in database_rows:
            new_row = dict(row)
            for field in protected_fields:
                if field in new_row:
                    encrypted_hex = new_row[field]
                    # 1. Decrypt raw ciphertext
                    decrypted_text = self.engine.decrypt_data(encrypted_hex)
                    
                    # 2. Decide routing based on RBAC attributes
                    if is_authorized:
                        new_row[field] = decrypted_text
                    else:
                        new_row[field] = self.apply_mask(field, decrypted_text)
                        
            processed_rows.append(new_row)

        return processed_rows
