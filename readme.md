# Vehicle Dynamics Dashboard

A PyQt6 desktop application for loading, visualizing, and analyzing vehicle test data. Built as a final project for ENGR 10.

## Project Structure

| File | Description |
|------|-------------|
| `main.py` | Dashboard UI and application entry point |
| `data_manager.py` | CSV loading, filtering, and statistics calculations |
| `graph_manager.py` | Matplotlib plot generation |
| `generate_vehicle_data.py` | Vehicle test data generator (provided) |
| `sample_data/` | Folder containing pre-generated CSV datasets |

## Requirements

- Python 3.x
- PyQt6
- matplotlib
- pandas
- numpy

Install dependencies:

```
pip install PyQt6 matplotlib pandas numpy
```

## Running the App

```
python main.py
```

## Dashboard Features

### Data File Selection
Select any CSV file from the `sample_data` folder using the dropdown at the top of the dashboard, or use **Load New File** to browse for a file elsewhere on your device.

### Vehicle & Profile Type Filters
After loading a file, the vehicle type and profile type dropdowns are automatically populated with valid combinations found in the data. Selecting one filter updates the other to only show compatible options.

### Plot Buttons
Five plot types are available once a file and filters are selected:

| Button | Plot |
|--------|------|
| Plot Basic Stats | Bar chart of speed statistics (mean, median, std dev, etc.) |
| Plot Acceleration | Acceleration over time (m/s²) |
| Plot Fuel Efficiency | Fuel consumption over time (L/100km) |
| Plot Braking | Acceleration with braking threshold highlighted at -2.0 m/s² |
| Plot Motion | Speed over time (km/h) |

### Generating New Test Data
At the bottom of the dashboard, choose a vehicle type, profile type, and duration (in seconds), then click **Generate New Test Data**. The file is saved to `sample_data/` and automatically loaded.

**Vehicle types:** sedan, SUV, sports
**Profile types:** urban, highway, sport
**Default duration:** 300 seconds
