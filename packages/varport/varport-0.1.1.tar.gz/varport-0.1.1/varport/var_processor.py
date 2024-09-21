import polars as pl
from datetime import datetime
import numpy as np
from .report_generator import Portfolio, MonteCarloSimulator, VaRCalculator
class MainVaRProcessor:
    def __init__(self, filepath):
        self.filepath = filepath

    def process(self, mu=None, Sigma=None):
        today = datetime.now().date()

        # Initialize the Portfolio and Pricing Model
        portfolio = Portfolio(self.filepath)
        portfolio.clean_and_parse(today)
        unique_assets = portfolio.get_unique_assets()
        num_assets = len(unique_assets)

        # If mu and Sigma are not provided, create them with the correct dimensions
        if mu is None:
            mu = np.zeros(num_assets)  # Create a default mu vector of zeros
        if Sigma is None:
            Sigma = np.eye(num_assets)  # Create a default identity matrix for Sigma

        # Ensure the size of mu and Sigma match the number of unique assets
        if len(mu) != num_assets or Sigma.shape != (num_assets, num_assets):
            raise ValueError(f"Dimensions of mu or Sigma do not match the number of unique assets ({num_assets}).")

        # Validate the covariance matrix
        self.validate_covariance_matrix(Sigma)

        # Pass the cleaned_df to the simulator
        simulator = MonteCarloSimulator(portfolio.cleaned_df)
        price_simulations_df = simulator.simulate_prices(mu, Sigma, 10000)

        # Initialize and run VaR calculation
        var_calculator = VaRCalculator(today)
        var_calculator.process_columns(portfolio.reduced_df, price_simulations_df)
        #print("portfolio.reduced_df is ",portfolio.reduced_df.head())

        # Calculate current value and VaR
        current_val = var_calculator.custom_function(portfolio.cleaned_df, today)
        VaR = var_calculator.calculate_var(current_val)
        #print(f"Value at Risk (VaR): {VaR}")
        # Get the differences for reporting
        differences = [result - current_val for result in var_calculator.stored_results]

        return portfolio, VaR, differences

    def validate_covariance_matrix(self, Sigma):
        if not np.allclose(Sigma, Sigma.T):
            raise ValueError("Covariance matrix is not symmetric.")
        eigvals = np.linalg.eigvals(Sigma)
        if np.any(eigvals < 0):
            raise ValueError("Covariance matrix is not positive semi-definite.")