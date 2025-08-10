from finance.Finance_Data import FinanceData


class FinanceService:
    """Service layer for operations on finance data"""

    def __init__(self, username: str) -> None:
        self.data = FinanceData(username)

    def add_entry(self, entry: dict) -> None:
        self.data.add_entry(entry)

    def get_entries(self):
        return self.data.get_entries()

    def clear_all_entries(self) -> None:
        self.data.clear_all_entries()

    def save_to_csv(self, file_path: str) -> None:
        self.data.save_to_csv(file_path)

    def save_to_excel(self, file_path: str) -> None:
        self.data.save_to_excel(file_path)
