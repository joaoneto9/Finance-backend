import os
from typing import Any
from webbrowser import get
from psycopg.rows import dict_row, DictRow
from psycopg import Connection, sql
from cryptography.fernet import Fernet

class User_repository:

    def __init__(self, conn: Connection) -> None:
        self.conn = conn
        self.table = "users"
        self.cripter = Fernet(key=os.getenv("SECRET_KEY", "SECRET_KEY").encode()) # não posso perder a chave
        
    def login_user(self, email: str, password: str) -> dict[str, Any] | None:
        with self.conn.cursor(row_factory=dict_row) as cur:
            query = sql.SQL(
                """
                    SELECT *
                    FROM {table}
                    WHERE email = %s
                """
            ).format(table=sql.Identifier(self.table))
            
            cur.execute(query, (email,))

            line: dict[str, Any] | None = cur.fetchone()

            if line is None:
                Exception("seu email ainda não tem cadastro")
            elif self.cripter.decrypt(line['user_password'].encode()).decode() != password:
                Exception("senha incorreta")

            return line 


    def register_user(self, username: str, email: str, password: str) -> bool:
        with self.conn.cursor() as cur:
            try:
                query = sql.SQL("""
                    SELECT email 
                    FROM {table}
                    WHERE email = %s
                """).format(table=sql.Identifier(self.table))

                cur.execute(query, (email,))

                line = cur.fetchone()

                if line is not None:
                    return False
                    
                # inserção de um usuário

                insert = sql.SQL(
                    """
                        INSERT INTO {table} (username, email, user_password) 
                        VALUES (%s, %s, %s)
                    """).format(table=sql.Identifier(self.table))

                cur.execute(insert, (username, email, 
                                     self.cripter.encrypt(password.encode()).decode())) # encript the password
                
                self.conn.commit()
                return True
            
            except Exception as e:
                self.conn.rollback()
                return False
