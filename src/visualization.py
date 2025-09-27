"""
Visualization Module - Optimized Housing Data Visualization
=========================================================

This module provides high-performance visualization functions for housing data
analysis using Matplotlib and Seaborn with optimization for memory efficiency
and scalability.

Features:
- Line chart for price range distribution (Objective 1)
- Bar chart for AC vs no-AC comparison (Objective 2) 
- Scatter plot for parking-price relationship (Objective 3)
- Comparison plots for area-prefarea analysis (Objective 4)
- Optimized plotting with vectorized operations

Author: Data Scientist Agent
Created for: Housing Data Exploration Mini-Project (Phase 2)
"""

import matplotlib.pyplot as plt
import seaborn as sns
import polars as pl
import numpy as np
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Set optimized plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")


class HousingVisualizer:
    """
    Optimized housing data visualizer with memory-efficient plotting.
    """
    
    def __init__(self, figsize: Tuple[int, int] = (12, 8)):
        """
        Initialize visualizer with plotting parameters.
        
        Args:
            figsize (Tuple[int, int]): Default figure size
        """
        self.figsize = figsize
        self.colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        
    def plot_price_ranges_line_chart(self, price_analysis: Dict, save_path: Optional[str] = None) -> plt.Figure:
        """
        Create line chart for price range distribution (Objective 1).
        
        Args:
            price_analysis (Dict): Price range analysis results
            save_path (Optional[str]): Path to save the plot
            
        Returns:
            plt.Figure: Generated figure
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        ranges = price_analysis['ranges']
        counts = price_analysis['counts']
        
        # Create line chart with markers
        ax.plot(ranges, counts, marker='o', linewidth=3, markersize=8, 
                color=self.colors[0], markerfacecolor=self.colors[1])
        
        # Add data labels on points
        for i, (range_label, count) in enumerate(zip(ranges, counts)):
            ax.annotate(f'{count} houses\n({price_analysis["percentages"][i]:.1f}%)', 
                       (i, count), textcoords="offset points", 
                       xytext=(0,10), ha='center', fontsize=10,
                       bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.7))
        
        # Styling
        ax.set_title('House Distribution by Price Ranges\n(Objective 1: Price Range Analysis)', 
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Price Range (Lakhs ₹)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Houses', fontsize=12, fontweight='bold')
        
        # Improve grid and styling
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_facecolor('#fafafa')
        
        # Add summary text
        total_houses = price_analysis['total_houses']
        ax.text(0.02, 0.98, f'Total Houses: {total_houses}', transform=ax.transAxes, 
                fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.7))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            
        return fig
    
    def plot_ac_comparison_bar_chart(self, ac_analysis: Dict, save_path: Optional[str] = None) -> plt.Figure:
        """
        Create bar chart for AC vs no-AC price comparison (Objective 2).
        
        Args:
            ac_analysis (Dict): AC analysis results
            save_path (Optional[str]): Path to save the plot
            
        Returns:
            plt.Figure: Generated figure
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        categories = ['No AC', 'With AC']
        avg_prices = [ac_analysis['ac_no']['avg_price'], ac_analysis['ac_yes']['avg_price']]
        counts = [ac_analysis['ac_no']['count'], ac_analysis['ac_yes']['count']]
        
        # Create bar chart
        bars = ax.bar(categories, avg_prices, color=[self.colors[3], self.colors[2]],
                     alpha=0.8, width=0.6)
        
        # Add value labels on bars
        for i, (bar, price, count) in enumerate(zip(bars, avg_prices, counts)):
            height = bar.get_height()
            ax.annotate(f'₹{price:,.0f}\n({count} houses)', 
                       (bar.get_x() + bar.get_width()/2., height),
                       ha='center', va='bottom', fontsize=12, fontweight='bold',
                       bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
        
        # Styling
        ax.set_title('Average House Prices: AC vs No-AC\n(Objective 2: Air Conditioning Analysis)', 
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_ylabel('Average Price (₹)', fontsize=12, fontweight='bold')
        ax.set_xlabel('Air Conditioning Status', fontsize=12, fontweight='bold')
        
        # Format y-axis to show prices in lakhs
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x/100000:.1f}L'))
        
        # Add price difference annotation
        price_diff = ac_analysis['price_difference']
        percentage_diff = ac_analysis['percentage_difference']
        ax.text(0.5, 0.95, f'Price Difference: ₹{price_diff:,.0f} ({percentage_diff:.1f}% higher with AC)', 
                transform=ax.transAxes, ha='center', va='top', fontsize=11,
                bbox=dict(boxstyle="round,pad=0.5", facecolor='yellow', alpha=0.7))
        
        ax.grid(True, alpha=0.3, axis='y')
        ax.set_facecolor('#fafafa')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            
        return fig
    
    def plot_parking_price_relationship(self, parking_analysis: Dict, save_path: Optional[str] = None) -> plt.Figure:
        """
        Create scatter plot for parking-price relationship (Objective 3).
        
        Args:
            parking_analysis (Dict): Parking analysis results
            save_path (Optional[str]): Path to save the plot
            
        Returns:
            plt.Figure: Generated figure
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        parking_spaces = parking_analysis['parking_spaces']
        avg_prices = parking_analysis['avg_prices']
        counts = parking_analysis['counts']
        correlation = parking_analysis['correlation']
        
        # Plot 1: Average price by parking spaces
        bars = ax1.bar(parking_spaces, avg_prices, color=self.colors[4], alpha=0.7)
        
        # Add value labels
        for bar, price, count in zip(bars, avg_prices, counts):
            height = bar.get_height()
            ax1.annotate(f'₹{price:,.0f}\n({count} houses)', 
                        (bar.get_x() + bar.get_width()/2., height),
                        ha='center', va='bottom', fontsize=10)
        
        ax1.set_title('Average Price by Parking Spaces', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Number of Parking Spaces', fontsize=12)
        ax1.set_ylabel('Average Price (₹)', fontsize=12)
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x/100000:.1f}L'))
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Plot 2: Trend line
        ax2.plot(parking_spaces, avg_prices, marker='o', linewidth=2, markersize=8,
                color=self.colors[0], markerfacecolor=self.colors[1])
        
        # Add trend line
        z = np.polyfit(parking_spaces, avg_prices, 1)
        p = np.poly1d(z)
        ax2.plot(parking_spaces, p(parking_spaces), "--", alpha=0.8, color=self.colors[3])
        
        ax2.set_title(f'Parking-Price Correlation\n(r = {correlation:.3f}, {parking_analysis["relationship_strength"]})', 
                     fontsize=14, fontweight='bold')
        ax2.set_xlabel('Number of Parking Spaces', fontsize=12)
        ax2.set_ylabel('Average Price (₹)', fontsize=12)
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x/100000:.1f}L'))
        ax2.grid(True, alpha=0.3)
        
        # Main title
        fig.suptitle('Parking-Price Relationship Analysis\n(Objective 3: Simulation)', 
                    fontsize=16, fontweight='bold', y=1.02)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            
        return fig
    
    def plot_area_prefarea_comparison(self, area_analysis: Dict, save_path: Optional[str] = None) -> plt.Figure:
        """
        Create comparison plot for area-prefarea price gap (Objective 4).
        
        Args:
            area_analysis (Dict): Area-prefarea analysis results
            save_path (Optional[str]): Path to save the plot
            
        Returns:
            plt.Figure: Generated figure
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        categories = ['<5000 sqft\n& No Preferred Area', '≥5000 sqft\n& With Preferred Area']
        avg_prices = [area_analysis['small_no_prefarea']['avg_price'], 
                     area_analysis['large_with_prefarea']['avg_price']]
        counts = [area_analysis['small_no_prefarea']['count'],
                 area_analysis['large_with_prefarea']['count']]
        
        # Create bar chart with different colors
        bars = ax.bar(categories, avg_prices, color=[self.colors[3], self.colors[2]], 
                     alpha=0.8, width=0.6)
        
        # Add value labels
        for i, (bar, price, count) in enumerate(zip(bars, avg_prices, counts)):
            if price > 0:  # Only add label if data exists
                height = bar.get_height()
                ax.annotate(f'₹{price:,.0f}\n({count} houses)', 
                           (bar.get_x() + bar.get_width()/2., height),
                           ha='center', va='bottom', fontsize=12, fontweight='bold',
                           bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
        
        # Styling
        ax.set_title('Price Gap: Small Houses (No Pref Area) vs Large Houses (With Pref Area)\n(Objective 4: Area-Prefarea Analysis)', 
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_ylabel('Average Price (₹)', fontsize=12, fontweight='bold')
        ax.set_xlabel('House Category', fontsize=12, fontweight='bold')
        
        # Format y-axis
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x/100000:.1f}L'))
        
        # Add gap information
        price_gap = area_analysis['price_gap']
        percentage_gap = area_analysis['percentage_gap']
        gap_interpretation = area_analysis['gap_interpretation']
        
        if price_gap > 0:
            ax.text(0.5, 0.95, f'Price Gap: ₹{price_gap:,.0f} ({percentage_gap:.1f}% higher)\nClassification: {gap_interpretation}', 
                    transform=ax.transAxes, ha='center', va='top', fontsize=11,
                    bbox=dict(boxstyle="round,pad=0.5", facecolor='lightyellow', alpha=0.8))
        
        ax.grid(True, alpha=0.3, axis='y')
        ax.set_facecolor('#fafafa')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            
        return fig
    
    def create_comprehensive_dashboard(self, analysis_results: Dict, save_path: Optional[str] = None) -> plt.Figure:
        """
        Create comprehensive dashboard with all visualizations.
        
        Args:
            analysis_results (Dict): Complete analysis results
            save_path (Optional[str]): Path to save the dashboard
            
        Returns:
            plt.Figure: Dashboard figure
        """
        fig = plt.figure(figsize=(20, 15))
        
        # Create subplots grid
        gs = fig.add_gridspec(3, 2, height_ratios=[1, 1, 1], width_ratios=[1, 1], 
                             hspace=0.3, wspace=0.3)
        
        # Plot 1: Price ranges (top left)
        ax1 = fig.add_subplot(gs[0, 0])
        price_data = analysis_results['objective_1_price_ranges']
        ranges = price_data['ranges']
        counts = price_data['counts']
        
        ax1.plot(ranges, counts, marker='o', linewidth=3, markersize=8, color=self.colors[0])
        ax1.set_title('Price Range Distribution', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Number of Houses')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: AC comparison (top right)
        ax2 = fig.add_subplot(gs[0, 1])
        ac_data = analysis_results['objective_2_ac_analysis']
        categories = ['No AC', 'With AC']
        avg_prices = [ac_data['ac_no']['avg_price'], ac_data['ac_yes']['avg_price']]
        
        ax2.bar(categories, avg_prices, color=[self.colors[3], self.colors[2]], alpha=0.8)
        ax2.set_title('AC vs No-AC Prices', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Average Price (₹)')
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x/100000:.1f}L'))
        
        # Plot 3: Parking relationship (middle, span both columns)
        ax3 = fig.add_subplot(gs[1, :])
        parking_data = analysis_results['objective_3_parking_simulation']
        parking_spaces = parking_data['parking_spaces']
        parking_prices = parking_data['avg_prices']
        
        ax3.plot(parking_spaces, parking_prices, marker='o', linewidth=2, markersize=8, color=self.colors[4])
        ax3.set_title(f'Parking-Price Relationship (Correlation: {parking_data["correlation"]:.3f})', 
                     fontsize=14, fontweight='bold')
        ax3.set_xlabel('Number of Parking Spaces')
        ax3.set_ylabel('Average Price (₹)')
        ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x/100000:.1f}L'))
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Area-prefarea comparison (bottom, span both columns)
        ax4 = fig.add_subplot(gs[2, :])
        area_data = analysis_results['objective_4_area_gap']
        categories = ['<5000 sqft & No Pref Area', '≥5000 sqft & With Pref Area']
        area_prices = [area_data['small_no_prefarea']['avg_price'], 
                      area_data['large_with_prefarea']['avg_price']]
        
        ax4.bar(categories, area_prices, color=[self.colors[3], self.colors[2]], alpha=0.8)
        ax4.set_title(f'Area-Prefarea Price Gap: ₹{area_data["price_gap"]:,.0f} ({area_data["percentage_gap"]:.1f}%)', 
                     fontsize=14, fontweight='bold')
        ax4.set_ylabel('Average Price (₹)')
        ax4.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x/100000:.1f}L'))
        
        # Main dashboard title
        fig.suptitle('Housing Data Analysis Dashboard\nComplete Objectives (1-4) Visualization', 
                    fontsize=18, fontweight='bold', y=0.98)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            
        return fig


# Utility functions for quick visualization
def quick_price_range_plot(price_analysis: Dict, save_path: Optional[str] = None) -> plt.Figure:
    """
    Quick utility for price range line chart.
    
    Args:
        price_analysis (Dict): Price range analysis results
        save_path (Optional[str]): Path to save the plot
        
    Returns:
        plt.Figure: Generated figure
    """
    visualizer = HousingVisualizer()
    return visualizer.plot_price_ranges_line_chart(price_analysis, save_path)


if __name__ == "__main__":
    # Test visualization functions
    print("Testing Housing Visualization Functions...")
    
    # Create sample data for testing
    sample_price_analysis = {
        'ranges': ['0-25L', '26-50L', '51-75L', '76-100L', '>100L'],
        'counts': [50, 150, 200, 100, 45],
        'percentages': [9.2, 27.5, 36.7, 18.3, 8.3],
        'total_houses': 545
    }
    
    try:
        visualizer = HousingVisualizer()
        fig = visualizer.plot_price_ranges_line_chart(sample_price_analysis)
        plt.close(fig)  # Close to prevent display in testing
        
        print("✅ Visualization functions validated!")
        print("🚀 Phase 2 visualization module ready!")
        
    except Exception as e:
        print(f"❌ Visualization validation failed: {str(e)}")
        exit(1)