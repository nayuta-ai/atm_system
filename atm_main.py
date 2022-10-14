"""Python 3.10, PEP8"""
import datetime
from typing import Any
from model import PostgreDB


class ATM:
    def __init__(self, user: str) -> None:
        """ An initialize function
        Create an instance for a user and connect to DB.

        Args:
            user (str): an user
        """
        self.user = user
        self.db = PostgreDB()

    def withdraw(self, money: int):
        """ A function for withdrawing

        Args:
            money (int): Money to be withdrawn
        """
        all_money = self.fetch_money()
        if all_money < money:
            raise ValueError("Deposit limit exceeded.")
        all_money -= money
        dt_now = datetime.datetime.now()
        self.insert_data(
            "logs", [(
                self.user,
                "withdraw",
                money,
                dt_now.strftime('%Y-%m-%d %H:%M:%S')
            )]
        )
        self.insert_data("total", [(self.user, all_money)])

    def deposit(self, money: int):
        """ A function for depositing

        Args:
            money (int): Money to be deposited
        """
        all_money = self.fetch_money()

        all_money += money
        dt_now = datetime.datetime.now()
        self.insert_data(
            "logs", [(
                self.user,
                "deposit",
                money,
                dt_now.strftime('%Y-%m-%d %H:%M:%S')
            )]
        )
        self.insert_data("total", [(self.user, all_money)])

    def fetch_logs(
        self,
        record: int
    ) -> list[tuple([str, int, datetime.datetime.timestamp])]:
        """ A function for fetching data from logs table
        Args:
            record (int): The number of record fetched
        Returns:
            list[list[str]]: Log information
                ([status("deposit" or "withdraw"), money, time])
        """
        return self.db.fetch_from_logs(user=self.user, num=record)

    def fetch_money(self) -> int:
        """ A function for fetching data from total table
        Returns:
            int: Total money deposited by the user in the bank
        """
        record = self.db.fetch_from_total(user=self.user)
        if not record:
            return 0
        else:
            return record[0]

    def insert_data(self, table: str, content: list[tuple[(any)]]) -> None:
        """ A function for inserting some data into DB

        Args:
            table (str): an target table
            content (list(any)): A data to insert
                (If insert it into logs table,
                it is list(tuple(str, str, int, datetime.datetime.timestamp)),
                If insert it into total table, it is list(tuple(str, int)))

        """
        if table == "logs":
            self.db.insert_logs(records=content)
        elif table == "total":
            self.db.insert_total(records=content)


if __name__ == "__main__":
    atm = ATM("user")
    atm.deposit(100)
    atm.deposit(100)
    atm.withdraw(0)
    atm.fetch_logs(1)


"""DB
logs (table 1)
column: user, status(deposit, withdraw), money, time
row: record

total (table 2)
column: user, all_money
"""
