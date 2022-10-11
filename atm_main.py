"""Python 3.10, PEP8"""
import datetime


class ATM:
    def __init__(self, user: str) -> None:
        self.user = user

    def withdraw(self, money: int):
        all_money = self.fetch_money()
        if all_money < money:
            raise ValueError("Deposit limit exceeded.")
        all_money -= money
        dt_now = datetime.datetime.now()
        self.insert_data("table1", [self.user, "withdraw", str(money), dt_now.strftime('%Y-%m-%d %H:%M:%S')])
        self.insert_data("total", [self.user, str(all_money)])

    def deposit(self, money: int):
        all_money = self.fetch_money()
        all_money += money
        dt_now = datetime.datetime.now()
        self.insert_data("table1", [self.user, "deposit", str(money), dt_now.strftime('%Y-%m-%d %H:%M:%S')])
        self.insert_data("total", [self.user, str(all_money)])

    def fetch_logs(self, record: int) -> list[list[str]]:
        """
        Args:
            user (str): user name
            record (int): the number of record fetched
        Returns:
            list[list[str]]: log information ([status("deposit" or "withdraw"), money, time])
        """
        # To Do
        pass

    def fetch_money(self) -> int:
        # To Do
        pass

    def insert_data(self, table: str, content: list[str]) -> None:
        pass

"""DB
logs (table 1)
column: user, status(deposit, withdraw), money, time
row: record

total (table 2)
column: user, all_money
"""