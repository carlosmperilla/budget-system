import unittest
from budget_system import ParserTableName

class ParserTableNameTest(unittest.TestCase):
    
    def setUp(self) -> None:
        self.file_name = 'test_table_one_storeone_[15-05-22].csv'
        self.parser_table = ParserTableName(self.file_name)

    def test_get_name_of_the_store(self):
        store_name = self.parser_table.get_store_name()
        self.assertEqual(store_name, 'storeone')

    def test_get_date_of_purchase(self):
        table_date = self.parser_table.get_table_date()
        self.assertEqual(table_date, '15-05-22')

    def test_get_name_of_the_store_and_date_of_purchase(self):
        store_name, table_date = self.parser_table.get_all()
        self.assertEqual(store_name, 'storeone')
        self.assertEqual(table_date, '15-05-22')

if __name__ == '__main__':
    unittest.main(verbosity=2)