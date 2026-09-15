class ProxyConfig:
    # 256-bit Key in Hex (32 bytes) for AES-GCM
    # In production, this should be loaded securely from environment variables
    MASTER_KEY_HEX = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
    
    # Target tables and columns that hold encrypted sensitive payload data
    PROTECTED_COLUMNS = {
        "users": ["credit_card", "ssn_tax_id"]
    }
    
    # Access Control Matrix mapping roles to clear-text permissions
    AUTHORIZED_ROLES = ["admin", "compliance_officer"]
