#For suite-test and smoke-test
from unittest import TestLoader, TestSuite, TextTestRunner

#For cleaning data.
from shutil import rmtree

#Base Folder for Budget System.
from pre_requirements import BASE_FOLDER

#Basic tests
from test_parsertablename import ParserTableNameTest
from test_creation_and_addition import CreationAndAdditionTest
from test_purchaselist import PurchaseListTest
from test_spentclass import SpentTest
from test_visualization import VisualizationTest

#We load the basic tests.
parsertablename_tests = TestLoader().loadTestsFromTestCase(ParserTableNameTest)
creation_and_addition_tests = TestLoader().loadTestsFromTestCase(CreationAndAdditionTest)
purchaselist_tests = TestLoader().loadTestsFromTestCase(PurchaseListTest)
spentclass_tests = TestLoader().loadTestsFromTestCase(SpentTest)
visualization_tests = TestLoader().loadTestsFromTestCase(VisualizationTest)

def cleaning() -> None:
    """
        Delete files for clean testing.
    """
    rmtree(BASE_FOLDER)

#We build the test suite.
smoke_test = TestSuite([
    parsertablename_tests,
    creation_and_addition_tests,
    purchaselist_tests,
    spentclass_tests,
    visualization_tests
])

#We store the generated report.
runner = TextTestRunner()

#We run the smoke test.
runner.run(smoke_test)
cleaning()
