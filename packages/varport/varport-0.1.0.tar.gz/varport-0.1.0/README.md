# VARPORT

VARPORT is a Python library to calculate Value at Risk (VaR) of a derivatives portfolio and generate reports .

## Features

- Compute VaR using Monte Carlo simulations
- Generate PDF reports with portfolio summaries and charts
- Supports options and futures portfolios

## Installation

```bash


#usage

pip install varport
from varport import ReportGenerator, MainVaRProcessor
import numpy as np

# Load your portfolio from a CSV file
portfolio_file = 'C:/xxx/portfolio.csv'

# Example user input for mu and Sigma
mu = np.array([0.05, 0.03, 0.07, 0.04, 0.06])  # Example mu vector (expected returns)
Sigma = np.array([[0.1, 0.02, 0.03, 0.01, 0.04],  # Example covariance matrix
                  [0.02, 0.08, 0.01, 0.03, 0.02],
                  [0.03, 0.01, 0.09, 0.02, 0.01],
                  [0.01, 0.03, 0.02, 0.07, 0.02],
                  [0.04, 0.02, 0.01, 0.02, 0.08]])

# Initialize MainVaRProcessor with the portfolio file path
var_processor = MainVaRProcessor(filepath=portfolio_file)

# Process the portfolio with user-provided mu and Sigma to calculate VaR and differences
portfolio, VaR, differences = var_processor.process(mu=mu, Sigma=Sigma)

# Generate the report with the calculated differences and VaR
report = ReportGenerator(differences=differences, VaR=VaR, portfolio=portfolio)

# Generate and save the PDF report
report.display_table_and_chart(pdf_filename="VaR_Report_Test.pdf")

print("Report generated successfully!")
