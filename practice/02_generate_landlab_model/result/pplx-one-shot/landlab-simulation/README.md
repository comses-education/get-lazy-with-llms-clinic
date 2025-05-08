# Landlab Overland Flow Simulation

This project demonstrates a simple overland flow simulation using Landlab's OverlandFlow component. It sets up a synthetic terrain, applies rainfall, simulates water flow, and visualizes the resulting surface water depth.

## Prerequisites

- **Python 3.7 or later**
- **`uv` package manager** (see [uv's documentation](https://github.com/astral-sh/uv) for installation)

## Setup

### 1. Initialize Project

If you haven't already, initialize a new project with `uv`:

```
uv init landlab-simulation
cd landlab-simulation
```

### 2. Install Dependencies

Install the required packages using `uv`:

```
uv add landlab numpy matplotlib
```

This will update your `pyproject.toml` and create a `uv.lock` file.

## Running the Simulation

Start the simulation with:

```
python -m uv run main.py
```

This will:
- Create a synthetic terrain grid
- Apply rainfall for 2 hours
- Simulate water flow for a total of 3 hours
- Display a plot of the resulting surface water depth

## Customization

You can adjust the following parameters in `main.py` to customize the simulation:

- **Grid dimensions and resolution**: `RasterModelGrid((50, 50), xy_spacing=30)`
- **Surface roughness coefficient**: `mannings_n=0.03`
- **Rainfall duration**: `storm_duration = 7200` (in seconds)
- **Rainfall intensity**: `rainfall_mmhr = 5.0` (in mm/hr)
- **Total simulation time**: `total_run_time = 10800` (in seconds)

## Expected Output

The script will display a visualization of the surface water depth across the terrain after the simulation completes. Areas with higher water accumulation will appear lighter on the color scale.

---

*For more details, see the [Landlab documentation](https://landlab.readthedocs.io/).*