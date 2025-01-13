# Rideshare Driver Analytics Dashboard

A comprehensive analytics dashboard for rideshare drivers to track their earnings, hours, and mileage. Built with Streamlit and Python, this application provides intuitive visualizations and data management capabilities.

## Features

- Easy data entry for daily rides (hours, miles, earnings)
- Interactive data table with edit capabilities
- Dynamic visualizations including:
  - Daily earnings breakdown with trend analysis
  - Hours worked over time
  - Miles driven tracking
  - Efficiency metrics (earnings per hour/mile)
- Date range selection for customized analysis
- Automatic statistics calculation
- Data export functionality (CSV, PDF)
- Save/Load progress capability

## Installation

1. Install Python 3.8 or higher if you haven't already.

2. Clone or download this repository to your local machine.

3. Navigate to the project directory in your terminal:
```bash
cd rideshare-analytics
```

4. Install required packages:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Streamlit server:
```bash
streamlit run main.py
```

2. Your default web browser should automatically open to:
```
http://localhost:8501
```

## Usage

1. Use the sidebar to enter new ride data:
   - Select the date
   - Enter hours worked
   - Enter miles driven
   - Enter total earnings

2. View your data in the interactive table:
   - Edit entries directly in the table
   - Sort by any column
   - Filter data as needed

3. Analyze your performance through various charts:
   - Daily earnings with trend line
   - Hours worked over time
   - Miles driven patterns
   - Efficiency metrics

4. Use the date range selector to focus on specific time periods

5. Export your data:
   - CSV format for spreadsheet analysis
   - PDF format for reporting

6. Save and load your progress:
   - Save your current data
   - Restore from previous saves

## Directory Structure

- `main.py`: Main application file
- `database.py`: Database operations
- `utils.py`: Utility functions
- `visualizations.py`: Chart creation functions
- `requirements.txt`: Required Python packages
- `backups/`: Directory for saved progress
- `exports/`: Directory for exported files

## License

MIT License