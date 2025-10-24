# AI Excel Data Analyzer

This project is a work-in-progress to build an AI-powered engine for reading, analyzing, and manipulating data in Excel files using natural language.

## Current Status (Phase 1)

The project is currently in the initial **data exploration and setup phase**.

* **Environment:** A Python virtual environment (`venv`) is set up.
* **Dependencies:** All required libraries are listed in `requirements.txt`.
* **Data Generation:** A script (`generate_data.py`) exists to create a test Excel file (`realistic_synthetic_data.xlsx`) with 1000 rows of structured and unstructured data.
  (!UPCOMING!)
* **Core Logic:** A test script (`test_pandas.py`) exists to demonstrate the core data manipulation operations (filtering, math, aggregation, pivoting) using the Pandas library.

At this stage, **there is no API or AI integration**. The project consists of standalone scripts for data creation and testing.

## How to Use (Developer Setup)

To set up the project and run the current test files:

### 1. Setup Environment
First, create and activate the virtual environment, then install the required libraries.

```bash
# Create the virtual environment
python -m venv venv

# Activate the environment (macOS/Linux)
source venv/bin/activate
# (Windows)
# .\venv\Scripts\activate

# Install all required libraries
pip install -r requirements.txt

#Run the generate_data.py script to create the synthetic_data.xlsx file.
python generate_data.py
