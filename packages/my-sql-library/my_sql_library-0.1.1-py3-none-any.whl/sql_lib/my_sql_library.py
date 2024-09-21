# Create a new file: my_sql_library.py

class SQLQuery:
    def __init__(self, pre_sql: str, sql: str, post_sql: str):
        self.pre_sql = pre_sql
        self.sql = sql
        self.post_sql = post_sql

    def get_full_query(self):
        """
        Concatenates pre_sql, sql, and post_sql into a single query.
        """
        return f"{self.pre_sql}\n{self.sql}\n{self.post_sql}"

    def __repr__(self):
        return f"SQLQuery(pre_sql='{self.pre_sql}', sql='{self.sql}', post_sql='{self.post_sql}')"
