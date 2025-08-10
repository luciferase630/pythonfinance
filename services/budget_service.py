from budget.budget_setting import BudgetSetting


class BudgetService:
    """Service layer for budget operations"""

    def __init__(self, username: str) -> None:
        # Avoid opening window by default
        self.setting = BudgetSetting(username, isWindowOpen=False)

    def clear_budget(self) -> None:
        self.setting.clear_budget()

    def load_budget(self) -> dict:
        return self.setting.load_budget()
