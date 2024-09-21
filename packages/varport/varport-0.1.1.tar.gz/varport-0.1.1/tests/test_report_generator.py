```python
import unittest
from var_report_generator.report_generator import ReportGenerator

class TestReportGenerator(unittest.TestCase):
    def test_report_generation(self):
        # Set up dummy data
        differences = [100, 200, -150, 50, -50]
        VaR = 75
        portfolio = None  # You would set up a mock portfolio here

        # Test report generation
        report = ReportGenerator(differences, VaR, portfolio)
        report.display_table_and_chart("test_report.pdf")

        # Check if the report was created (or mock the PDF generation)
        self.assertTrue(os.path.exists("test_report.pdf"))

if __name__ == '__main__':
    unittest.main()
