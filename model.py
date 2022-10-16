import datetime

import psycopg2


class PostgreDB:
    def __init__(self, db="postgres") -> None:
        self.conn = self.connect_db(db=db)

    def connect_db(
        self,
        db: str = "postgres"
    ) -> psycopg2.extensions.connection:
        """ A function for connecting postgre db

        Args:
            db (str): The db name

        Returns:
            psycopg2.extensions.connection: An instance of db connected.

        Raises:
            psycopg2.DatabaseError: If no connection to db is found.
        """
        try:
            # (To Do) Rewrite it by using logs.
            print('Connecting to the PostgreSQL database...')
            return psycopg2.connect(
                f"host=postgres\
                port=5432\
                dbname={db}\
                user=postgre\
                password=postgre"
            )

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def create_table(self) -> None:
        """ A function for creating table
        If any table doesn't exist, Use it for creating some table.
        """
        create_logs_table_query = "\
            create table logs(\
                id integer,\
                name varchar(10),\
                status varchar(10),\
                money integer,\
                time TIMESTAMP\
            )"
        create_total_table_query = "\
            create table total(\
                id integer,\
                name varchar(10),\
                all_money integer\
            )"
        with self.conn.cursor() as cursor:
            cursor.execute(create_logs_table_query)
            cursor.execute(create_total_table_query)
            self.conn.commit()

    def insert_logs(
        self,
        records: tuple[str, str, int, datetime.datetime.timestamp]
    ) -> None:
        """ A function for inserting data to logs table.

        Args:
            records (list(tuple(str, str, int, datetime.datetime.timestamp))):
                Data for inserting to the table called logs.
        """
        insert_logs_query = "\
            insert into logs(\
                name, status, money, time\
            )\
            values(%s, %s, %s, %s)"
        with self.conn.cursor() as cursor:
            cursor.executemany(insert_logs_query, records)
            self.conn.commit()

    def update_total(self, user: str, money: int) -> None:
        """ A function for inserting data to total table.

        Args:
            records (list(tuple(str, int))):
                Data for inserting to the table called total.
        """
        count_total_query = f"\
            select count(name = '{user}') from total"
        insert_total_query = "\
            insert into total(\
                name, all_money\
            )\
            values(%s, %s)"
        update_total_query = f"\
            update total\
            set all_money = {money}\
            where name = '{user}'"
        with self.conn.cursor() as cursor:
            cursor.execute(count_total_query)
            num_record = cursor.fetchone()
            if num_record[0]:
                cursor.execute(update_total_query)
                self.conn.commit()
            else:
                cursor.executemany(insert_total_query, [(user, money)])
                self.conn.commit()

    def fetch_from_logs(
        self,
        user: str,
        num: int
    ) -> list[list[tuple[str, int, datetime.datetime.timestamp]]]:
        """ A function for fetching some data from logs table

        Args:
            user (str): User name
            num (int): Number of cases retrieved from DB
        """
        try:
            fetch_from_logs_query = f"\
                select\
                    status, money, time\
                from\
                    logs\
                where\
                    name='{user}'\
                limit\
                    {num}"
            with self.conn.cursor() as cursor:
                cursor.execute(fetch_from_logs_query)
                return cursor.fetchall()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def fetch_from_total(self, user: str) -> list[int]:
        """ A function for fetching some data from total table

        Args:
            user (str): User name
        """
        fetch_from_logs_query = \
            f"select all_money from total where name='{user}'"
        with self.conn.cursor() as cursor:
            cursor.execute(fetch_from_logs_query)
            return cursor.fetchone()

    def close_connection(self) -> None:
        """ A function for closing connection to db.
        If all process is done, Use it for closing connection to db.
        """
        self.conn.close()
        # (To Do) Rewrite it by using logs.
        print("Close the PostgreSQL database...")
