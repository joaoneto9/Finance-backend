from decimal import Decimal
from psycopg import Connection, sql
from psycopg.rows import dict_row

class Expense_repository:

    def __init__(self, conn: Connection) -> None:
        self.conn = conn
        self.table = "expenses"

    def register_expense(self, register_date: str, 
                         paymant_date: str, amount: int, 
                         payment_description: str, type_of_payment: str,
                         user_email: str):
        with self.conn.cursor() as cursor:
            insert = sql.SQL(
                """
                    INSERT INTO {table}
                    (register_date, paymant_date, amount, 
                    payment_description, type_of_paymant, user_email)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
            ).format(table=sql.Identifier(self.table))

            try:
                cursor.execute(insert, (register_date, 
                            paymant_date, Decimal(amount), 
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
                    SELECT * 
                    FROM {table}
                    WHERE user_email = %s
                """
            ).format(table=sql.Identifier(self.table))

            cursor.execute(query, (user_email,))

            data = cursor.fetchall()

        return data

