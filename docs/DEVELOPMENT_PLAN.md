# DEVELOPMENT PLAN: Housing Data Exploration & Visualization Mini-Project
## Overview
This plan outlines the 4-phase development of a compute-optimized, memory-efficient project to analyze `Housing.csv` and satisfy the objectives in `changes.md`. The project uses Polars for data processing, ensuring scalability for large datasets.

## Project Structure
```
mini-project/
├── data/
│   └── Housing.csv                    # Dataset (price, area, bedrooms, etc.)
├── docs/
│   ├── DEVELOPMENT_PLAN.md            # This file
│   └── Minor Project - Python.pdf     # Existing documentation
├── src/                               # Source code (optimized scripts)
│   ├── data_loader.py                 # Polars-based data loading and preprocessing
│   ├── analysis.py                    # Core analysis functions (averages, gaps, simulations)
│   └── visualization.py               # Plotting functions (line/bar charts)
├── notebooks/                         # Jupyter notebooks for interactive exploration
│   └── housing_analysis.ipynb         # Main analysis notebook
├── requirements.new.txt               # Optimized dependencies
├── changes.md                         # Objectives
├── README.md                          # Project summary and usage
└── venv/                              # Virtual environment (activated via source venv/bin/activate)
```

## Phases (4 Phases)
### Phase 1: Environment Setup & Data Exploration
- **Objective**: Set up optimized environment and explore dataset structure.
- **Tasks**:
  - Install dependencies from `requirements.new.txt`.
  - Load `Housing.csv` with Polars; inspect schema, data types, and summary stats.
  - Handle mixed data: Convert yes/no to booleans; note furnishingstatus (furnished, semi-furnished, unfurnished).
  - Validate data integrity (no nulls, outliers).
- **Files Created/Modified**:
  - `src/data_loader.py` (Polars data loading with type casting).
  - Initial `notebooks/housing_analysis.ipynb` (exploration cells).
- **Validation**: Run in Jupyter; check memory usage with Polars profiling.

### Phase 2: Price Range Analysis & Visualization
- **Objective**: Satisfy Objective 1 (price ranges 0-25L, 26-50L, etc.; line chart).
- **Tasks**:
  - Bin prices into ranges; count houses per bin.
  - Generate line chart with Matplotlib/Seaborn.
- **Files Created/Modified**:
  - `src/analysis.py` (price binning function).
  - `src/visualization.py` (line chart function).
  - Update `notebooks/housing_analysis.ipynb` (analysis cells).
- **Validation**: Test with sample data; ensure vectorized ops for efficiency.

### Phase 3: Advanced Analysis & Simulations
- **Objective**: Satisfy Objectives 2-4 (AC averages bar chart, parking-price simulation, sqft-prefarea gap).
- **Tasks**:
  - Compute averages for AC/no-AC; plot bar chart.
  - Simulate parking-price relationship (e.g., correlation/scatter with SciPy).
  - Calculate price gap for <5000sqft & no prefarea vs. >5000sqft & prefarea.
- **Files Created/Modified**:
  - Update `src/analysis.py` (averages, gaps, simulations).
  - Update `src/visualization.py` (bar/scatter plots).
  - Update `notebooks/housing_analysis.ipynb` (full analysis).
- **Validation**: Performance test with tqdm; validate stats with NumPy/SciPy.

### Phase 4: Documentation, Optimization & Delivery
- **Objective**: Finalize, document, and validate the project.
- **Tasks**:
  - Optimize code for memory (Polars lazy mode if needed).
  - Create `README.md` with usage, results summary, and performance notes.
  - Run full pipeline; generate outputs (charts, stats).
- **Files Created/Modified**:
  - `README.md` (comprehensive guide).
  - Final `notebooks/housing_analysis.ipynb` (complete with outputs).
- **Validation**: End-to-end run; check scalability (e.g., simulate larger dataset).

## Key Principles
- **Optimization**: Polars for 10x speed; vectorized NumPy/Matplotlib; memory-efficient data handling.
- **Modularity**: Separate concerns (loading, analysis, viz) for reusability.
- **Validation**: Test each phase; include performance metrics.
- **Dependencies**: Stick to `requirements.new.txt` for minimal footprint.

## Timeline & Milestones
- Phase 1: 1-2 hours (setup/exploration).
- Phase 2: 1 hour (price analysis).
- Phase 3: 2 hours (advanced analysis).
- Phase 4: 1 hour (docs/validation).

Total: ~5-6 hours.
</content>
<parameter name="filePath">/home/prats/Playground/Internships/Elewayte/mini-project/docs/DEVELOPMENT_PLAN.md