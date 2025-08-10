import os
import sys
import tempfile
import unittest

from services.budget_service import BudgetService


class TestBudgetService(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.old_meipass = getattr(sys, '_MEIPASS', None)
        sys._MEIPASS = self.tmpdir.name
        os.makedirs(os.path.join(self.tmpdir.name, 'budgetData'), exist_ok=True)
        self.service = BudgetService('tester')

    def tearDown(self):
        if self.old_meipass is None:
            del sys._MEIPASS
        else:
            sys._MEIPASS = self.old_meipass
        self.tmpdir.cleanup()

    def test_load_and_clear_budget(self):
        default_budget = {
            "month": {"income_budget": 0, "expense_budget": 0},
            "year": {"income_budget": 0, "expense_budget": 0},
        }
        self.assertEqual(self.service.load_budget(), default_budget)

        self.service.setting.data["month"] = {"income_budget": 1000, "expense_budget": 500}
        self.service.setting.save_budget()
        self.assertEqual(self.service.load_budget()["month"]["income_budget"], 1000)

        self.service.clear_budget()
        self.assertEqual(self.service.load_budget(), default_budget)


if __name__ == "__main__":
    unittest.main()
