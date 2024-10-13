import numpy as np
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
from sktime.forecasting.arima import ARIMA

# SQLAlchemy connection setup
DATABASE_URL = "postgresql+psycopg2://postgres:Cmorikas77@192.168.8.6:5433/MetalPrices"
engine = create_engine(DATABASE_URL)

class Model:
    def __init__(self, tickers: list[str], x_size: int, y_size: int) -> None:
        self.tickers = tickers
        self.x_size = x_size
        self.y_size = y_size
        self.models: dict[str, ARIMA] = {}

    def fetch_real_data(self) -> pd.DataFrame:
        """Fetch real data from metal_prices_ml table in PostgreSQL."""
        query = """
        SELECT timestamp, "XAUUSD", "XAGUSD", "XPTUSD", "XPDUSD" 
        FROM metal_prices_ml
        ORDER BY timestamp DESC
        LIMIT 12;
        """
        data = pd.read_sql(query, con=engine)
        return data

    def train(self, /, use_generated_data: bool = False) -> None:
        if use_generated_data:
            # For testing purposes, use generated sample data
            data, _, _ = generate_sample_data(self.tickers, self.x_size, self.y_size)
        else:
            # Fetch real data from the PostgreSQL database
            data = self.fetch_real_data()

        for ticker in self.tickers:
            dataset = data[ticker].values
            model = ARIMA(order=(1, 1, 0), with_intercept=True, suppress_warnings=True)
            model.fit(dataset)
            self.models[ticker] = model

    def save(self, path_to_dir: str | Path) -> None:
        """Save the trained models to a directory."""
        path_to_dir = Path(path_to_dir)
        path_to_dir.mkdir(parents=True, exist_ok=True)
        for ticker in self.tickers:
            full_path = path_to_dir / ticker
            self.models[ticker].save(full_path)