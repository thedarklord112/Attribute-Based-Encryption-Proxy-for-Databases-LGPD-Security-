# 🛡️ The "Please Don't Sue Us" Attribute-Based Database Crypto Proxy

```text
      _____________________________________
     /                                    /|
    /      [ INCOMING SQL QUERY ]        / |
   /   "INSERT INTO users VALUES (...)" /  |
  /____________________________________/   |
  |                                    |   |
  |    🔒 CRYPTO ENGINE INTERCEPT     |   |
  |   Data processed via AES-256-GCM   |   | 
  |                                    |   /
  |  [ ROLE: ADMIN ]   -> Cleartext    |  /
  |  [ ROLE: SUPPORT ] -> XXXX-XXXX    | /
  |____________________________________|/
```

A production-grade, highly secure, and paranoid database proxy simulator that intercepts SQL queries to enforce automated encryption and **Attribute-Based Access Control (ABAC)**. 

Did your marketing team just ask for full database access "just to look at something"? Did your intern accidentally print clear-text credit cards into the production logs? Or are you just trying to avoid paying millions in corporate privacy fines (LGPD/GDPR) and stay out of jail? 

**This proxy is your legal shield. Welcome to stress-free database compliance.**

---

## ⚡ Why Use This? (Before the auditors show up)

- **Paranoid AES-256-GCM Encryption**: We don't just hide data; we seal it with military-grade authenticated primitives. It generates random nonces for every single insertion. Even if a hacker steals your raw database files, all they will see is random garbage text.
- **The "Intern Proof" Tamper Detector**: If someone logs directly into the PostgreSQL server and tries to manually alter an encrypted credit card number to bypass the system, the GCM validation engine detects the change instantly and throws an absolute fit (blocks the decryption loop). 
- **Mind-Reading SQL Interceptor**: Scans incoming queries mid-flight to detect where the sensitive fields are hiding. It automatically strips data on `INSERT` and hooks into `SELECT` statements dynamically.
- **The Customer Support Blinder**: Implements rigid Attribute-Based Access Control. If the logged-in user is an `admin`, they see the raw credit card. If they are a `support` agent, they get a nicely obfuscated string like `XXXX-XXXX-XXXX-1234`. Because let's be honest, customer support doesn't need to know the customer's full tax ID to reset a password.

---

## 📂 Inside the High-Security Vault

```text
├── src/
│   ├── config.py         # The target hitlist (which columns to lock down)
│   ├── crypto_engine.py  # The heavy cryptography algorithms (Don't touch unless you have a PhD)
│   ├── query_parser.py   # The SQL parsing agent (No regex spaghetti here)
│   └── proxy.py          # The corporate router deciding who gets clear-text or mask filters
└── tests/
    └── test_proxy.py     # Automated unit tests proving to your legal team that you are safe
```

---

## 🛠️ Quick Start (Before the data leak happens)

Here is how you inject this defensive layer into your database application layer:

```python
from src.proxy import DatabaseCryptoProxy

# 1. Boot up the defense system
security_gate = DatabaseCryptoProxy()

# 2. An unsuspecting query arrives from the frontend application
raw_sql = "INSERT INTO users (name, credit_card, ssn_tax_id) VALUES (%s, %s, %s)"
highly_sensitive_payload = ["John Doe", "1234567890123456", "00011122233"]

# 3. Intercept and turn sensitive data into meaningless hex garbage before saving to Postgres
db_safe_values = security_gate.process_incoming_insert(raw_sql, highly_sensitive_payload)
print(f"What goes into the DB: {db_safe_values}") 
# Output: ['John Doe', 'a7f3b89e21...', 'c3d4e5f6a1...']

# 4. Fetch data back and dynamic route based on corporate roles
mock_db_row = [{"name": "John Doe", "credit_card": db_safe_values[1], "ssn_tax_id": db_safe_values[2]}]
select_sql = "SELECT credit_card, ssn_tax_id FROM users"

# Scenario A: CEO / Admin looks at the profile
boss_view = security_gate.process_outgoing_results(select_sql, "users", mock_db_row, user_role="admin")
print(f"Boss View: {boss_view[0]['credit_card']}") # 1234567890123456 (Cleartext)

# Scenario B: Untrusted Outsource Support Agent looks at the profile
support_view = security_gate.process_outgoing_results(select_sql, "users", mock_db_row, user_role="support")
print(f"Support View: {support_view[0]['credit_card']}") # XXXX-XXXX-XXXX-3456 (Safely Masked!)
```

---

## 🧪 Testing the Fort Knox Defense

To run the automated tests and prove to your Compliance Officer that you actually deserve your salary:

```bash
python -m unittest discover -s tests
```

## 🔒 Serious Security Disclaimer
The `.env` or configuration file contains the master cryptographic keys. **Never commit your actual production master hex keys to public GitHub source control.** If you leak the key, the encryption becomes as useful as a screen door on a submarine. Always use corporate secret management engines when deploying this to live infrastructure.

## 📄 License
This security suite configuration is open-source and free to protect your company under the **MIT License**. Use it to save your database, protect your clients, or just flex your cybersecurity skills on LinkedIn.


Oh, congratulations on finishing the read. Now, please open an issue explaining what you understood, bcs even I don't know anymore lol ;)
