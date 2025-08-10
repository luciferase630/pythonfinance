import os
import sys
import tempfile
import unittest

from services.finance_service import FinanceService


class TestFinanceService(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.old_meipass = getattr(sys, '_MEIPASS', None)
        sys._MEIPASS = self.tmpdir.name
        os.makedirs(os.path.join(self.tmpdir.name, 'FinancialData'), exist_ok=True)
        self.service = FinanceService('tester')

    def tearDown(self):
        if self.old_meipass is None:
            del sys._MEIPASS
        else:
            sys._MEIPASS = self.old_meipass
        self.tmpdir.cleanup()

    def test_add_get_save_clear(self):
        entry = {"date": "2024-01-01", "type": "income", "amount": 100, "note": "test"}
        self.service.add_entry(entry)
        self.assertEqual(self.service.get_entries(), [entry])

        csv_path = os.path.join(self.tmpdir.name, 'out.csv')
        excel_path = os.path.join(self.tmpdir.name, 'out.xlsx')
        self.service.save_to_csv(csv_path)
        self.service.save_to_excel(excel_path)
        self.assertTrue(os.path.exists(csv_path))
        self.assertTrue(os.path.exists(excel_path))

        self.service.clear_all_entries()
        self.assertEqual(self.service.get_entries(), [])


if __name__ == "__main__":
    unittest.main()
