from decimal import Decimal
from psycopg import Connection, Cursor, sql
from psycopg.rows import dict_row
from datetime import datetime

class Expense_repository:

    def __init__(self, conn: Connection) -> None:
        self.conn = conn
        self.table = "expenses"

    def register_expense(self, register_date: str, 
                         payment_date: str, amount: int, 
                         payment_description: str, type_of_payment: str,
                         user_email: str):
        with self.conn.cursor() as cursor:
            insert = sql.SQL(
                """
                    INSERT INTO {table}
                    (register_date, payment_date, amount, 
                    payment_description, type_of_payment, user_email)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
            ).format(table=sql.Identifier(self.table))

            try:
                cursor.execute(insert, (register_date, 
                            payment_date, Decimal(amount), 
                            payment_description, type_of_payment,
                            user_email))
            
                self.conn.commit()
                return True
            except Exception as e:
                print(e)
                self.conn.rollback()
                return False
        
    def get_users_expenses(self, user_email: str) -> list:
        with self.conn.cursor(row_factory=dict_row) as cursor:
            query = sql.SQL(
                """
                    SELECT id, amount, payment_date, payment_description, register_date, type_of_payment
                    FROM {table}
                    WHERE user_email = %s
                """
            ).format(table=sql.Identifier(self.table))

            cursor.execute(query, (user_email,))

            data = cursor.fetchall()

        return data
    
    def get_users_expenses_by_date(self, user_email: str, date, specified_data: bool):
        with self.conn.cursor(row_factory=dict_row) as cursor:
            if not specified_data:
                query = sql.SQL(
                    """
                        SELECT id, amount, payment_date, payment_description, register_date, type_of_payment
                        FROM {table}
                        WHERE DATE_TRUNC('month', payment_date) = DATE_TRUNC('month', %s::date) AND user_email = %s
                    """
                ).format(table=sql.Identifier(self.table))

            else:
                query = sql.SQL(
                    """
                        SELECT id, amount, payment_date, payment_description, register_date, type_of_payment
                        FROM {table}
                        WHERE payment_date = %s AND user_email = %s
                    """
                ).format(table=sql.Identifier(self.table))

            cursor.execute(query, (datetime.strptime(date, "%Y-%m-%d"), user_email))

            data = cursor.fetchall()

        return data
        
 
