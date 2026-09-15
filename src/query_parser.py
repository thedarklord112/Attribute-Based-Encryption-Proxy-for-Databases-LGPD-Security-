import re
from typing import Dict, Any, List, Tuple
from src.config import ProxyConfig

class SQLQueryInterceptor:
    def __init__(self):
        # Regex to capture basic INSERT statements: INSERT INTO table (cols) VALUES (vals)
        self.insert_regex = re.compile(
            r"INSERT\s+INTO\s+(\w+)\s*\((.*?)\)\s*VALUES\s*\((.*?)\)", 
            re.IGNORECASE
        )

    def parse_insert(self, query: str) -> Tuple[str, List[str]]:
        """Scans an INSERT query to find table and target columns."""
        match = self.insert_regex.search(query)
        if not match:
            return "", []
        
        table = match.group(1).lower()
        columns = [c.strip().lower() for c in match.group(2).split(",")]
        return table, columns

    def identify_select_columns(self, query: str, table: str) -> List[str]:
        """Identifies which protected columns are being requested in a SELECT query."""
        query_lower = query.lower()
        protected = ProxyConfig.PROTECTED_COLUMNS.get(table, [])
        
        # Simple projection check to find fields in the SQL string
        requested_protected_fields = []
        for field in protected:
            if field in query_lower or "*" in query_lower:
                requested_protected_fields.append(field)
                
        return requested_protected_fields
