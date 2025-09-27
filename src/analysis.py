"""
Analysis Module - Optimized Housing Data Analysis Functions
========================================================

This module provides compute-optimized analysis functions for housing data
using Polars for high-performance processing. Includes price binning, 
statistical computations, and relationship analysis.

Features:
- Price range binning (0-25L, 26-50L, 51-75L, 76-100L, >100L)
- AC vs no-AC average price analysis
- Parking-price relationship simulations
- Area-prefarea price gap calculations
- Vectorized operations for scalability

Author: Data Scientist Agent
Created for: Housing Data Exploration Mini-Project (Phase 2)
"""

import polars as pl
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging
from tqdm import tqdm

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HousingAnalyzer:
    """
    Optimized housing data analyzer using Polars for high-performance processing.
    """
    
    def __init__(self, data: pl.DataFrame):
        """
        Initialize analyzer with housing data.
        
        Args:
            data (pl.DataFrame): Housing data loaded with Polars
        """
        self.data = data
        self.price_lakhs = data['price'] / 100000  # Convert to lakhs for analysis
        
    def analyze_price_ranges(self) -> Dict:
        """
        Analyze price ranges and count houses in each bin (Objective 1).
        Bins: 0-25L, 26-50L, 51-75L, 76-100L, >100L
        
        Returns:
            Dict: Price range analysis with counts and percentages
        """
        logger.info("🏠 Analyzing price ranges...")
        
        # Define price bins in lakhs
        bins = [0, 25, 50, 75, 100, float('inf')]
        labels = ['0-25L', '26-50L', '51-75L', '76-100L', '>100L']
        
        # Use Polars for efficient binning
        price_ranges = []
        counts = []
        
        for i in range(len(bins) - 1):
            if i == len(bins) - 2:  # Last bin (>100L)
                count = self.data.filter(pl.col('price') / 100000 > bins[i]).height
            else:
                count = self.data.filter(
                    (pl.col('price') / 100000 >= bins[i]) & 
                    (pl.col('price') / 100000 < bins[i+1])
                ).height
            
            price_ranges.append(labels[i])
            counts.append(count)
        
        total_houses = sum(counts)
        percentages = [(count / total_houses) * 100 for count in counts]
        
        result = {
            'ranges': price_ranges,
            'counts': counts,
            'percentages': percentages,
            'total_houses': total_houses,
            'bins_lakhs': bins[:-1],  # Exclude infinity
            'summary': dict(zip(price_ranges, counts))
        }
        
        logger.info(f"✅ Price range analysis complete: {total_houses} houses analyzed")
        return result
    
    def analyze_ac_prices(self) -> Dict:
        """
        Analyze average house prices for AC vs no-AC houses (Objective 2).
        
        Returns:
            Dict: AC analysis with averages and statistics
        """
        logger.info("❄️ Analyzing AC vs no-AC prices...")
        
        # Use Polars groupby for efficient aggregation
        ac_analysis = self.data.group_by('airconditioning').agg([
            pl.col('price').mean().alias('avg_price'),
            pl.col('price').count().alias('count'),
            pl.col('price').std().alias('std_price'),
            pl.col('price').min().alias('min_price'),
            pl.col('price').max().alias('max_price')
        ]).sort('airconditioning')
        
        # Extract results
        ac_results = ac_analysis.to_dict(as_series=False)
        
        result = {
            'ac_yes': {
                'avg_price': ac_results['avg_price'][1],  # True (AC=yes)
                'count': ac_results['count'][1],
                'std_price': ac_results['std_price'][1],
                'min_price': ac_results['min_price'][1],
                'max_price': ac_results['max_price'][1]
            },
            'ac_no': {
                'avg_price': ac_results['avg_price'][0],  # False (AC=no)
                'count': ac_results['count'][0],
                'std_price': ac_results['std_price'][0],
                'min_price': ac_results['min_price'][0],
                'max_price': ac_results['max_price'][0]
            },
            'price_difference': ac_results['avg_price'][1] - ac_results['avg_price'][0],
            'percentage_difference': ((ac_results['avg_price'][1] - ac_results['avg_price'][0]) / ac_results['avg_price'][0]) * 100
        }
        
        logger.info(f"✅ AC analysis complete: AC houses ₹{result['ac_yes']['avg_price']:,.0f}, No-AC ₹{result['ac_no']['avg_price']:,.0f}")
        return result
    
    def simulate_parking_price_relationship(self) -> Dict:
        """
        Simulate relationship between parking spaces and house prices (Objective 3).
        
        Returns:
            Dict: Parking-price relationship analysis
        """
        logger.info("🚗 Simulating parking-price relationship...")
        
        # Analyze parking distribution and average prices
        parking_analysis = self.data.group_by('parking').agg([
            pl.col('price').mean().alias('avg_price'),
            pl.col('price').count().alias('count'),
            pl.col('price').std().alias('std_price')
        ]).sort('parking')
        
        # Calculate correlation coefficient using Polars
        correlation = self.data.select(
            pl.corr('parking', 'price').alias('correlation')
        ).item()
        
        # Extract results
        parking_results = parking_analysis.to_dict(as_series=False)
        
        result = {
            'parking_spaces': parking_results['parking'],
            'avg_prices': parking_results['avg_price'],
            'counts': parking_results['count'],
            'std_prices': parking_results['std_price'],
            'correlation': correlation,
            'relationship_strength': self._interpret_correlation(correlation),
            'price_per_parking_space': []
        }
        
        # Calculate price increase per additional parking space
        for i in range(1, len(result['avg_prices'])):
            price_increase = result['avg_prices'][i] - result['avg_prices'][i-1]
            result['price_per_parking_space'].append(price_increase)
        
        logger.info(f"✅ Parking analysis complete: Correlation = {correlation:.3f}")
        return result
    
    def analyze_area_prefarea_gap(self) -> Dict:
        """
        Calculate price gap between <5000sqft & no prefarea vs ≥5000sqft & prefarea (Objective 4).
        
        Returns:
            Dict: Area-prefarea price gap analysis
        """
        logger.info("📐 Analyzing area-prefarea price gap...")
        
        # Filter for small houses without preferred area
        small_no_pref = self.data.filter(
            (pl.col('area') < 5000) & (pl.col('prefarea') == False)
        )
        
        # Filter for large houses with preferred area
        large_with_pref = self.data.filter(
            (pl.col('area') >= 5000) & (pl.col('prefarea') == True)
        )
        
        # Calculate statistics for both groups
        small_stats = small_no_pref.select([
            pl.col('price').mean().alias('avg_price'),
            pl.col('price').count().alias('count'),
            pl.col('price').std().alias('std_price'),
            pl.col('area').mean().alias('avg_area')
        ])
        
        large_stats = large_with_pref.select([
            pl.col('price').mean().alias('avg_price'),
            pl.col('price').count().alias('count'),
            pl.col('price').std().alias('std_price'),
            pl.col('area').mean().alias('avg_area')
        ])
        
        # Extract results
        if small_stats.height > 0 and large_stats.height > 0:
            small_avg = small_stats['avg_price'][0]
            large_avg = large_stats['avg_price'][0]
            price_gap = large_avg - small_avg
            percentage_gap = (price_gap / small_avg) * 100
        else:
            small_avg = large_avg = price_gap = percentage_gap = 0
        
        result = {
            'small_no_prefarea': {
                'avg_price': small_avg if small_stats.height > 0 else 0,
                'count': small_stats['count'][0] if small_stats.height > 0 else 0,
                'avg_area': small_stats['avg_area'][0] if small_stats.height > 0 else 0
            },
            'large_with_prefarea': {
                'avg_price': large_avg if large_stats.height > 0 else 0,
                'count': large_stats['count'][0] if large_stats.height > 0 else 0,
                'avg_area': large_stats['avg_area'][0] if large_stats.height > 0 else 0
            },
            'price_gap': price_gap,
            'percentage_gap': percentage_gap,
            'gap_interpretation': self._interpret_price_gap(percentage_gap)
        }
        
        logger.info(f"✅ Area-prefarea analysis complete: Gap = ₹{price_gap:,.0f} ({percentage_gap:.1f}%)")
        return result
    
    def _interpret_correlation(self, correlation: float) -> str:
        """Interpret correlation coefficient strength."""
        abs_corr = abs(correlation)
        if abs_corr >= 0.7:
            return "Strong"
        elif abs_corr >= 0.4:
            return "Moderate"
        elif abs_corr >= 0.2:
            return "Weak"
        else:
            return "Very Weak"
    
    def _interpret_price_gap(self, percentage_gap: float) -> str:
        """Interpret price gap percentage."""
        if percentage_gap >= 50:
            return "Very Large Gap"
        elif percentage_gap >= 25:
            return "Large Gap"
        elif percentage_gap >= 10:
            return "Moderate Gap"
        else:
            return "Small Gap"
    
    def get_complete_analysis(self) -> Dict:
        """
        Run complete analysis for all objectives.
        
        Returns:
            Dict: Complete analysis results
        """
        logger.info("🚀 Running complete housing analysis...")
        
        with tqdm(total=4, desc="Analysis Progress") as pbar:
            # Objective 1: Price ranges
            price_ranges = self.analyze_price_ranges()
            pbar.update(1)
            
            # Objective 2: AC analysis
            ac_analysis = self.analyze_ac_prices()
            pbar.update(1)
            
            # Objective 3: Parking simulation
            parking_analysis = self.simulate_parking_price_relationship()
            pbar.update(1)
            
            # Objective 4: Area-prefarea gap
            area_gap = self.analyze_area_prefarea_gap()
            pbar.update(1)
        
        complete_results = {
            'objective_1_price_ranges': price_ranges,
            'objective_2_ac_analysis': ac_analysis,
            'objective_3_parking_simulation': parking_analysis,
            'objective_4_area_gap': area_gap,
            'summary': {
                'total_houses': len(self.data),
                'price_range_min_max': (self.data['price'].min(), self.data['price'].max()),
                'analysis_completed': True
            }
        }
        
        logger.info("✅ Complete analysis finished successfully!")
        return complete_results


# Utility functions for easy access
def quick_price_range_analysis(data: pl.DataFrame) -> Dict:
    """
    Quick utility for price range analysis (Objective 1).
    
    Args:
        data (pl.DataFrame): Housing data
        
    Returns:
        Dict: Price range analysis
    """
    analyzer = HousingAnalyzer(data)
    return analyzer.analyze_price_ranges()


def validate_analysis_functions() -> bool:
    """
    Validate that analysis functions are working correctly.
    
    Returns:
        bool: True if validation passes
    """
    try:
        # Create sample data for testing
        sample_data = pl.DataFrame({
            'price': [2500000, 7500000, 5000000, 12000000],
            'area': [3000, 6000, 4500, 8000],
            'airconditioning': [True, False, True, True],
            'parking': [1, 2, 1, 3],
            'prefarea': [False, True, False, True]
        })
        
        analyzer = HousingAnalyzer(sample_data)
        
        # Test each analysis function
        price_ranges = analyzer.analyze_price_ranges()
        ac_analysis = analyzer.analyze_ac_prices()
        parking_sim = analyzer.simulate_parking_price_relationship()
        area_gap = analyzer.analyze_area_prefarea_gap()
        
        logger.info("✅ All analysis functions validated successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Analysis validation failed: {str(e)}")
        return False


if __name__ == "__main__":
    # Test the analysis functions
    print("Testing Housing Analysis Functions...")
    
    if validate_analysis_functions():
        print("✅ Analysis functions validated!")
    else:
        print("❌ Analysis validation failed!")
        exit(1)
    
    print("🚀 Phase 2 analysis module ready!")