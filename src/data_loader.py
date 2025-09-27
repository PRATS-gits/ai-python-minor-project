"""
Data Loader Module - Optimized for Housing.csv Analysis
===============================================

This module provides optimized data loading using Polars for 10x performance 
improvement over Pandas. Handles mixed data types (numerical, boolean, categorical)
with memory-efficient processing.

Features:
- Polars-based loading with type casting
- Boolean conversion for yes/no values
- Categorical handling for furnishingstatus
- Data validation and integrity checks
- Memory profiling capabilities

Author: Data Scientist Agent
Created for: Housing Data Exploration Mini-Project
"""

import polars as pl
import numpy as np
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HousingDataLoader:
    """
    Optimized data loader for Housing.csv using Polars for high-performance processing.
    """
    
    def __init__(self, file_path: str):
        """
        Initialize the data loader with file path.
        
        Args:
            file_path (str): Path to Housing.csv file
        """
        self.file_path = Path(file_path)
        self.data: Optional[pl.DataFrame] = None
        self.schema_info: Dict = {}
        
    def load_data(self) -> pl.DataFrame:
        """
        Load Housing.csv with optimized Polars processing and type casting.
        
        Returns:
            pl.DataFrame: Loaded and processed housing data
        """
        try:
            logger.info(f"Loading data from {self.file_path}")
            
            # Load data with Polars (10x faster than pandas)
            self.data = pl.read_csv(
                self.file_path,
                infer_schema_length=1000,  # Analyze first 1000 rows for schema
                try_parse_dates=False,     # No dates in housing data
                null_values=["", "NA", "NULL", "null"]  # Handle null values
            )
            
            logger.info(f"Data loaded successfully: {self.data.shape[0]} rows, {self.data.shape[1]} columns")
            
            # Process mixed data types
            self.data = self._process_data_types()
            
            # Validate data integrity
            self._validate_data()
            
            return self.data
            
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    def _process_data_types(self) -> pl.DataFrame:
        """
        Process mixed data types for optimal performance and analysis.
        
        Returns:
            pl.DataFrame: Data with processed types
        """
        logger.info("Processing data types for optimization...")
        
        # Define boolean columns (yes/no values)
        boolean_columns = [
            'mainroad', 'guestroom', 'basement', 
            'hotwaterheating', 'airconditioning', 'prefarea'
        ]
        
        # Convert yes/no to boolean for efficient processing
        processed_data = self.data.with_columns([
            pl.col(col).map_elements(
                lambda x: True if x == 'yes' else False,
                return_dtype=pl.Boolean
            ).alias(col)
            for col in boolean_columns
        ])
        
        # Ensure numerical columns are properly typed
        numerical_columns = ['price', 'area', 'bedrooms', 'bathrooms', 'stories', 'parking']
        processed_data = processed_data.with_columns([
            pl.col(col).cast(pl.Int64)
            for col in numerical_columns
        ])
        
        # Keep furnishingstatus as categorical string for analysis
        # (furnished, semi-furnished, unfurnished)
        processed_data = processed_data.with_columns(
            pl.col('furnishingstatus').cast(pl.Categorical)
        )
        
        logger.info("Data type processing completed")
        return processed_data
    
    def _validate_data(self) -> None:
        """
        Validate data integrity and check for issues.
        """
        logger.info("Validating data integrity...")
        
        # Check for null values
        null_counts = self.data.null_count()
        total_nulls = null_counts.sum_horizontal().item()
        
        if total_nulls > 0:
            logger.warning(f"Found {total_nulls} null values")
            print("Null value counts by column:")
            print(null_counts)
        else:
            logger.info("No null values found - data integrity confirmed")
        
        # Check for outliers in price (basic validation)
        price_min = self.data['price'].min()
        price_max = self.data['price'].max()
        logger.info(f"Price range validated: ${price_min:,} - ${price_max:,}")
        
        # Validate categorical values
        furnishing_values = self.data['furnishingstatus'].unique().to_list()
        expected_furnishing = ['furnished', 'semi-furnished', 'unfurnished']
        
        if set(furnishing_values).issubset(set(expected_furnishing)):
            logger.info(f"Furnishingstatus values confirmed: {furnishing_values}")
        else:
            logger.warning(f"Unexpected furnishingstatus values: {furnishing_values}")
    
    def get_data_summary(self) -> Dict:
        """
        Get comprehensive data summary for exploration.
        
        Returns:
            Dict: Data summary with statistics
        """
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        summary = {
            'shape': self.data.shape,
            'columns': self.data.columns,
            'dtypes': dict(zip(self.data.columns, [str(dtype) for dtype in self.data.dtypes])),
            'memory_usage_mb': self.data.estimated_size() / (1024 * 1024),
            'price_range': {
                'min': self.data['price'].min(),
                'max': self.data['price'].max(),
                'mean': self.data['price'].mean(),
                'median': self.data['price'].median()
            },
            'furnishing_distribution': (
                self.data['furnishingstatus']
                .value_counts()
                .sort('count', descending=True)
                .to_dict(as_series=False)
            ),
            'boolean_columns_summary': {
                col: {
                    'true_count': self.data[col].sum(),
                    'false_count': self.data[col].count() - self.data[col].sum()
                }
                for col in ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea']
            }
        }
        
        return summary
    
    def get_sample_data(self, n: int = 5) -> pl.DataFrame:
        """
        Get sample data for inspection.
        
        Args:
            n (int): Number of rows to sample
            
        Returns:
            pl.DataFrame: Sample data
        """
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() first.")
            
        return self.data.head(n)


# Utility functions for easy access
def load_housing_data(file_path: str = "data/Housing.csv") -> Tuple[pl.DataFrame, Dict]:
    """
    Quick utility to load housing data with summary.
    
    Args:
        file_path (str): Path to Housing.csv
        
    Returns:
        Tuple[pl.DataFrame, Dict]: Loaded data and summary
    """
    loader = HousingDataLoader(file_path)
    data = loader.load_data()
    summary = loader.get_data_summary()
    
    return data, summary


def validate_installation() -> bool:
    """
    Validate that all required dependencies are installed and working.
    
    Returns:
        bool: True if all dependencies are working
    """
    try:
        import polars as pl
        import numpy as np
        import matplotlib.pyplot as plt
        import seaborn as sns
        import scipy
        
        logger.info("All dependencies validated successfully!")
        logger.info(f"Polars version: {pl.__version__}")
        logger.info(f"NumPy version: {np.__version__}")
        
        return True
        
    except ImportError as e:
        logger.error(f"Dependency validation failed: {str(e)}")
        return False


if __name__ == "__main__":
    # Test the data loader
    print("Testing Housing Data Loader...")
    
    # Validate installation
    if not validate_installation():
        print("❌ Installation validation failed!")
        exit(1)
    
    print("✅ Installation validated!")
    
    # Test data loading
    try:
        file_path = "/home/prats/Playground/Internships/Elewayte/mini-project/data/Housing.csv"
        data, summary = load_housing_data(file_path)
        
        print(f"\n📊 Data loaded successfully!")
        print(f"Shape: {summary['shape']}")
        print(f"Memory usage: {summary['memory_usage_mb']:.2f} MB")
        print(f"Price range: ${summary['price_range']['min']:,} - ${summary['price_range']['max']:,}")
        
        print("\n🏠 Sample data:")
        print(data.head(3))
        
        print("\n✅ Phase 1 validation completed!")
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")