import numpy as np
import polars as pl
from scipy.stats import norm
from datetime import datetime, time
import time

# Start time for measuring execution time
start_time = time.time()

# Class for managing portfolio data
class Portfolio:
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None  # Initialize an empty dataframe or None
        self.cleaned_df = None  # Initialize cleaned_df as None

    def clean_and_parse(self, today):
        # Read the CSV file into a Polars DataFrame
        self.df = pl.read_csv(self.filepath, try_parse_dates=True)
        print("CSV file read and cleaned successfully.")
        # Fill null values with 0
        self.df = self.df.fill_null(0)

        # Clean and process the data
        self.df = self.df.with_columns(
            pl.when(pl.col("instrument_type") == "option")
            .then((pl.col("expiry").cast(pl.Date) - pl.lit(today)).dt.total_days() / 365)
            .otherwise(pl.col("expiry"))  # Retain original expiry values for non-options
            .alias("expiry")
        )
        

        # Add composite_key
        self.df = self.df.with_columns([
            pl.when(pl.col('instrument_type') == 'future')
            .then(pl.concat_str([pl.col('underlying_asset'), pl.col('expiry').cast(pl.Utf8)]))
            .otherwise(pl.concat_str([pl.col('underlying_asset'), pl.col('underlying_future_expiry').cast(pl.Utf8)]))
            .alias('composite_key')
        ])
        #print("Composite key added to the dataframe.")

        # Set cleaned_df
        self.cleaned_df = self.df.clone()  # Clone the cleaned DataFrame for further processing
        self.reduced_df = self.df.select([
        'composite_key', 'instrument_type', 'option_type', 
        'strike_price', 'volatility',  
        'expiry', 'lot_size', 'quantity'
        ])
        #print("Reduced DataFrame for VaR created.")
        
    # Method to add a row_id column if it doesn't exist
    def add_row_id(self):
        #print("Adding row_id...")
        if "row_id" not in self.df.columns:
            self.df = self.df.with_row_index("row_id")
        return self.df

    def get_unique_assets(self):
        if self.cleaned_df is None:
            raise ValueError("Dataframe is not cleaned. Call 'clean_and_parse()' first.")
        
        unique_combinations = (
            self.cleaned_df.group_by(['underlying_asset', 'instrument_type'])
            .agg(
                pl.when(pl.col('instrument_type') == 'option')
                .then(pl.col('underlying_future_expiry').cast(pl.Date).alias('expiry'))
                .otherwise(pl.col('expiry').cast(pl.Date))
            )
            .select(['underlying_asset', 'instrument_type', 'expiry'])
            .unique()
        )
        
        future_expiries = (
            unique_combinations
            .filter(pl.col('instrument_type') == 'future')
            .select(['underlying_asset', 'expiry'])
            .rename({'expiry': 'future_expiry'})
        )
        
        unique_combinations = (
            unique_combinations
            .join(future_expiries, on='underlying_asset', how='left')
            .with_columns([
                pl.when(pl.col('instrument_type') == 'option')
                .then(
                    pl.when(pl.col('future_expiry').is_null())
                    .then(pl.col('expiry'))
                    .otherwise(pl.col('expiry').list.set_difference(pl.col('future_expiry')))
                )
                .otherwise(pl.col('expiry'))
                .alias('expiry')
            ])
            .drop('future_expiry')
        )
        unique_assets = unique_combinations['underlying_asset'].unique()
        return unique_assets.to_list()

    def calculate_values(self, pricing_model):
        # Ensure row_id exists by calling add_row_id
        self.df = self.add_row_id()

        print("Starting portfolio value calculation...")
        df = self.df

        df_options = df.filter(pl.col("instrument_type") == "option")
        df_options = pricing_model.apply_black_scholes(df_options)

        df = df.join(df_options.select(["row_id", "optp"]), on="row_id", how="left")
        df = df.with_columns([
            pl.when(pl.col("instrument_type") == "future")
            .then(pl.col("quantity") * pl.col("lot_size") * pl.col("underlying_price"))
            .when(pl.col("instrument_type") == "option")
            .then(pl.col("optp") * pl.col("quantity") * pl.col("lot_size"))
            .otherwise(0)
            .alias("current_value")
        ])
        print("Portfolio values calculated.")
        return df

class MonteCarloSimulator:

    def __init__(self, portfolio_df):
        self.portfolio_df = portfolio_df

    def simulate_prices(self, mu, Sigma, num_simulations):
        # Step 1: Simulate returns using multivariate normal distribution
        returns_sim = np.random.multivariate_normal(mu, Sigma, num_simulations)
        returns_sim_df = pl.DataFrame(returns_sim, schema=self.portfolio_df["underlying_asset"].unique().to_list())

        # Step 2: Extract unique composite_key values from the portfolio
        unique_columns = [str(col) for col in self.portfolio_df["composite_key"].unique().to_list() if col is not None]
        converted_returns_sim_df = pl.DataFrame()

        # Step 3: Map the simulated returns to the corresponding composite keys
        for composite in unique_columns:
            underlying_asset = ''.join(filter(str.isalpha, composite))  # Extract the underlying asset name
            if underlying_asset in returns_sim_df.columns:
                converted_returns_sim_df = converted_returns_sim_df.with_columns(
                    returns_sim_df[underlying_asset].alias(composite)
                )
            else:
                print(f"Warning: No matching column found for {underlying_asset} in returns_sim_df")

        # Step 4: Get initial prices for each composite_key from the portfolio_df
        initial_prices = {}
        for col in unique_columns:
            filtered_df = self.portfolio_df.filter(pl.col("composite_key") == col)
            if filtered_df.height > 0:
                initial_prices[col] = filtered_df.select("underlying_price")[0, 0]
            else:
                print(f"Warning: No price found for {col}. Using None.")
                initial_prices[col] = None

        # Step 5: Convert the initial prices into a DataFrame
        initial_prices_reshaped = pl.DataFrame([initial_prices])

        # Step 6: Calculate the simulated prices by applying the exponential of returns to the initial prices
        price_simulations_array = np.exp(converted_returns_sim_df.to_numpy()) * initial_prices_reshaped.to_numpy()

        # Step 7: Convert the simulated prices array back into a DataFrame
        price_simulations_df = pl.DataFrame(
            price_simulations_array,
            schema=initial_prices_reshaped.columns
        )
        price_simulations_df = price_simulations_df.transpose(
                     include_header=True, 
                     header_name="composite_key", 
                     column_names=[f"simprice_{i}" for i in range(returns_sim_df.height)]
                 )

        return price_simulations_df
        



# Class for handling pricing models, including Black-Scholes
class PricingModels:
    def __init__(self, today, risk_free_rate=0.05):
        self.today = today
        self.risk_free_rate = risk_free_rate

    def black_scholes(self, S, K, r, T, sigma, option_type):
        d1 = (np.log(S/K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        option_price = np.where(option_type == 'c',
                                (S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)),
                                np.where(option_type == 'p',
                                         (K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)), 0))
        return option_price

    def apply_black_scholes(self, df):
        df = df.with_columns([
            ((pl.col("expiry").cast(pl.Date) - pl.lit(self.today)).dt.total_days() / 365).alias("T")
        ])

        df = df.with_columns([
            pl.when(pl.col("option_type").str.to_lowercase() == "call")
            .then(pl.lit('c'))
            .otherwise(pl.lit('p'))
            .alias("option_type_code")
        ])

        option_prices = self.black_scholes(
            df['underlying_price'].to_numpy(),
            df['strike_price'].to_numpy(),
            self.risk_free_rate,
            df['T'].to_numpy(),
            df['volatility'].to_numpy(),
            df['option_type_code'].to_numpy()
        )
        return df.with_columns(pl.Series("optp", option_prices))


# Class for Value at Risk (VaR) calculations
# Class for Value at Risk (VaR) calculations
class VaRCalculator:
    def __init__(self, today, risk_free_rate=0.05):
        self.today = today
        self.risk_free_rate = risk_free_rate
        self.stored_results = []

    # Custom function that processes the DataFrame with Black-Scholes calculations and sums the product
    def custom_function(self, df, today):  # <-- Add 'self'
        # Step 1: Filter and select required columns for options
        #print("Before filtering options, DF head:")
        #print(df.head())
        option = df.filter(pl.col("instrument_type") == "option").select([
            'option_type', 'strike_price', 'volatility', 'underlying_price', 'expiry', 'lot_size', 'quantity'
        ])
        #print("After filtering for options, option DF head:")
        #print(option.head())
        # Step 2: Filter and select required columns for futures
        future = df.filter(pl.col("instrument_type") == "future").select([
            'underlying_price', 'lot_size', 'quantity'
        ])

        # Calculate the total value for futures
        future = future.with_columns(
            (pl.col("lot_size") * pl.col("quantity") * pl.col("underlying_price")).alias("total_value")
        )

        # Step 3: Drop null values for options
        option = option.drop_nulls()

        # Step 4: Ensure correct types
        option = option.with_columns([
            pl.col("expiry").cast(pl.Float64),
            pl.col("volatility").cast(pl.Float64),
            pl.col("underlying_price").cast(pl.Float64),
            pl.col("strike_price").cast(pl.Float64),
        ])
        #print("option")
        #print(option.head())
        #print("future")
        #print(future.head())
        # Step 5: Compute d1 and d2 for Black-Scholes pricing
        expiry_sqrt = pl.col("expiry").sqrt()
        option = option.with_columns([
        (((pl.col("underlying_price") / pl.col("strike_price")).log() +
          (pl.lit(self.risk_free_rate) + 0.5 * pl.col("volatility")**2) * pl.col("expiry")) /
         (pl.col("volatility") * expiry_sqrt)).alias("d1")
        ])

        option = option.with_columns([
            (pl.col("d1") - pl.col("volatility") * expiry_sqrt).alias("d2")])

        # Step 6: Convert to numpy arrays for Black-Scholes calculation
        d1_np = option["d1"].to_numpy()
        d2_np = option["d2"].to_numpy()

        # Compute call and put prices
        call_prices = option["underlying_price"].to_numpy() * norm.cdf(d1_np) - \
                      option["strike_price"].to_numpy() * np.exp(
                          -self.risk_free_rate * option["expiry"].to_numpy()
                      ) * norm.cdf(d2_np)

        put_prices = option["strike_price"].to_numpy() * np.exp(
            -self.risk_free_rate * option["expiry"].to_numpy()
        ) * norm.cdf(-d2_np) - option["underlying_price"].to_numpy() * norm.cdf(-d1_np)

        # Step 7: Add option prices based on type
        option_prices = np.where(option["option_type"] == "call", call_prices, put_prices)

        # Add the calculated option prices to the DataFrame
        option = option.with_columns(pl.Series("option_price", option_prices))

        # Step 8: Compute the total value for options and sum
        option = option.with_columns(
            (pl.col("option_price") * pl.col("lot_size") * pl.col("quantity")).alias("total_value")
        )
        #print("option head")
        #print(option.head())
        #print("future head")
        #print(future.head())
        # Sum both options and futures total values
        total_option_value = option["total_value"].sum()
        total_future_value = future["total_value"].sum()

        # Return the final total value
        total_value = total_option_value + total_future_value
        #print(f"Total value: {total_value}")
        del(option)
        del(future)
        return total_value
  
    def process_columns(self, reduced_df, sdf):
        #print("inside process columns")
        #print("Reduced DataFrame (reduced_df):")
        #print(reduced_df.head())
        #print("Simulated prices DataFrame (sdf):")
        #print(sdf.head())

        # Get all columns of sdf except the first one (composite_key)
        columns_to_join = sdf.columns[1:]

        # Process each column eagerly using the custom_function
        total_sums = [
            self.stored_results.append(
                # Join reduced_df with the selected price simulation column
                self.custom_function(
                    reduced_df.join(
                        sdf.select([pl.col("composite_key"), pl.col(col).alias("underlying_price")]),  # Join on composite_key and alias the column
                        on="composite_key",  # Join key
                        how="inner"  # Inner join
                    ), 
                    self.today
                )
            ) and print(f"Processing column {idx}/{len(columns_to_join)}", "\nDataFrame passed to custom_function:", 
                        reduced_df.join(
                            sdf.select([pl.col("composite_key"), pl.col(col).alias("underlying_price")]), 
                            on="composite_key", 
                            how="inner"
                        ).head()  # Print only the first few rows for readability
            )  # Print progress and the DataFrame passed to custom_function
            for idx, col in enumerate(columns_to_join, start=1)
        ]

        return total_sums

    def calculate_var(self, current_val, p=0.01, s=10000):
        differences = [result - current_val for result in self.stored_results]
        #sorted_differences = sorted(differences)
        differences = np.array(differences)  # Convert to numpy array if it's a list
        VaR = np.percentile(differences, 1)
        #VaR = -sorted_differences[int(np.ceil(p * s)) - 1]
        return VaR


# Main class to run the entire process
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
        print(f"Value at Risk (VaR): {VaR}")
        # Get the differences for reporting
        differences = [result - current_val for result in var_calculator.stored_results]

        return portfolio, VaR, differences

    def validate_covariance_matrix(self, Sigma):
        if not np.allclose(Sigma, Sigma.T):
            raise ValueError("Covariance matrix is not symmetric.")
        eigvals = np.linalg.eigvals(Sigma)
        if np.any(eigvals < 0):
            raise ValueError("Covariance matrix is not positive semi-definite.")
#works good
import os
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from fpdf import FPDF
import io
import tempfile
from datetime import datetime
import pandas as pd

class ReportGenerator(FPDF):
    def __init__(self, differences, VaR, portfolio):
        super().__init__()
        self.differences = differences
        self.VaR = VaR
        self.portfolio = portfolio

    def header(self):
        # Add a report header to the PDF with a background color
        self.set_fill_color(100, 149, 237)  # Cornflower Blue
        self.set_text_color(255, 255, 255)  # White text
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Value at Risk (VaR) Report', ln=True, align='C', fill=True)
        self.ln(10)
        self.set_text_color(0, 0, 0)  # Reset text color to black

    def footer(self):
        # Add a footer with the date and time
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cell(0, 10, f'Report generated on: {date_time}', align='C')

    def display_table_and_chart(self, pdf_filename="VaR_Report_with_Tables.pdf"):
        # Generate the VaR chart and save it as a temporary file
        chart_image_path = self.display_var_chart()

        # Generate the PDF with the chart and portfolio summary
        self.generate_pdf(chart_image_path, pdf_filename)

        # Remove the temporary image file after generating the PDF
        if os.path.exists(chart_image_path):
            os.remove(chart_image_path)

    def display_var_chart(self):
        # Use Seaborn to create a histogram
        sns.set(style="whitegrid")
        fig, ax = plt.subplots(figsize=(10, 6))

        # Create histogram for differences with Seaborn
        sns.histplot(self.differences, bins=50, kde=True, color='lightblue', ax=ax)

        # Add a vertical line for VaR
        plt.axvline(self.VaR, color='red', linestyle='--', label=f"VaR = {self.VaR:.2f}")

        # Set labels and title
        ax.set_title("Value at Risk (VaR) Chart", fontsize=16)
        ax.set_xlabel("Change in Portfolio PnL (Differences)", fontsize=12)
        ax.set_ylabel("Frequency / Probability", fontsize=12)
        ax.legend()

        # Save the plot to a temporary file
        temp_chart_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        plt.savefig(temp_chart_file.name, format='png')
        temp_chart_file.close()  # Close the file so FPDF can access it
        plt.close()  # Close the plot to free up memory

        return temp_chart_file.name

    def generate_pdf(self, chart_image_path, pdf_filename):
        # Add a page
        self.add_page()

        # Add VaR text
        self.set_font('Arial', 'B', 12)
        self.cell(200, 10, f"VaR = {self.VaR:.2f}", ln=True)

        # Add the chart to the PDF from the saved image file
        self.set_font('Arial', 'B', 12)
        self.cell(200, 10, 'VaR Chart', ln=True)
        self.image(chart_image_path, x=10, y=self.get_y(), w=190)
        self.ln(120)  # Adjust for space after the chart

        # Add portfolio summary tables
        self.add_portfolio_summary()

        # Save the PDF file
        self.output(pdf_filename)
        print(f"PDF report generated: {pdf_filename}")

    def add_portfolio_summary(self):
        # Extract portfolio details
        unique_assets = self.portfolio.get_unique_assets()
        num_rows = self.portfolio.df.height
        num_options = self.portfolio.df.filter(pl.col("instrument_type") == "option").height
        num_futures = self.portfolio.df.filter(pl.col("instrument_type") == "future").height
        num_calls = self.portfolio.df.filter(pl.col("option_type") == "call").height
        num_puts = self.portfolio.df.filter(pl.col("option_type") == "put").height

        # Add the summary table header
        self.set_font('Arial', 'B', 12)
        self.cell(200, 10, 'Portfolio Summary', ln=True)

        # Add table headers with borders and background color
        self.set_fill_color(135, 206, 250)  # Light Sky Blue
        self.set_text_color(0, 0, 0)  # Black text for the table
        self.set_font('Arial', 'B', 10)
        self.cell(50, 8, 'Metric', border=1, align='C', fill=True)
        self.cell(140, 8, 'Value', border=1, align='C', fill=True)
        self.ln()

        # Add portfolio summary data
        summary_data = [
            ('Number of Rows', num_rows),
            ('Number of Unique Assets', len(unique_assets)),
            ('Assets', ', '.join(unique_assets)),
            ('Number of Options', num_options),
            ('Number of Calls', num_calls),
            ('Number of Puts', num_puts),
            ('Number of Futures', num_futures),
        ]

        # Set font for table content and reduce font size
        self.set_font('Arial', '', 9)
        for metric, value in summary_data:
            self.cell(50, 8, metric, border=1, align='L')
            self.cell(140, 8, str(value), border=1, align='L')
            self.ln()

# Usage

if __name__ == "__main__":
    filepath = "C:/Users/raghu/Documents/financial_instruments.csv"
    
    mu = np.array([0.05, 0.08, 0.03, 0.09, 0.05])  # 5 assets
    Sigma = np.array([[0.1, 0.02, 0.03, 0.01, 0.04],
                      [0.02, 0.3, 0.04, 0.02, 0.03],
                      [0.03, 0.04, 0.5, 0.03, 0.02],
                      [0.01, 0.02, 0.03, 0.8, 0.01],
                      [0.04, 0.03, 0.02, 0.01, 0.76]])

    processor = MainVaRProcessor(filepath)
    portfolio, VaR, differences = processor.process(mu=mu, Sigma=Sigma)
    # After running the VaR process, assuming 'differences', 'VaR', and 'portfolio' are available

    report = ReportGenerator(differences=differences, VaR=VaR, portfolio=portfolio)
    report.display_table_and_chart()  # This will display the table and chart on screen

    # Calculate execution time
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution Time: {execution_time} seconds")
