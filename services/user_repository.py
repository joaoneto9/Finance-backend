import os
from tkinter import E
import psycopg

with psycopg.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_FINANCE_DATABASE_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_USER_PASSWORD")
) as conn:
    with conn.cursor() as cur:

        def save_user(username: str, email: str, password: str) -> bool:
            # verificação de existencia de um usuario com email
            try:
                cur.execute("""
                    SELECT email 
                    FROM user_db
                    WHERE email = %s
                """, (email,))

                line = cur.fetchone()

                if line is not None:
                    return False
                
                # inserção de um usuário
                cur.execute(
                    """
                    INSERT INTO user_db (username, email, password) 
                    VALUES (%s, %s, %s)
                    """, (username, email, password)
                )
            
                conn.commit()
                return True
            except Exception as e:
                conn.rollback()
                return False
        
        def get_username_by_email(email: str) -> str:
            try:
                cur.execute("""
                    SELECT username
                    FROM user_db
                    WHERE email == %s
                """, (email,))

                row = cur.fetchone()

                if row is None:
                    return ""
                
                return row[0]
            except Exception as e:
                return ""
