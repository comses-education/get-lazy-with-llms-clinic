# Simple Landlab Overland Flow Simulation

This Python script demonstrates a basic overland flow simulation using the [Landlab](https://landlab.readthedocs.io/) modeling toolkit. It simulates how water flows over a simple, tilted land surface when subjected to a constant rainfall event.

## What it Simulates

The simulation models the following:

1.  **Domain:** A 2D `RasterModelGrid` representing a rectangular piece of land.
2.  **Topography:** A simple planar surface, tilted to create a slope, allowing water to flow towards one edge.
3.  **Rainfall:** A constant rainfall intensity applied uniformly over the entire grid for a specified duration.
4.  **Overland Flow:** The movement of surface water across the grid, governed by:
    *   Local water surface slopes.
    *   Manning's equation to account for surface roughness (friction).
    *   The script uses Landlab's `OverlandFlow` component, which is based on a 2D finite-volume solution of the shallow-water equations (St. Venant equations) under the kinematic wave approximation.
5.  **Boundary Conditions:**
    *   One edge of the grid is defined as an **open outlet**, allowing water to flow off the model domain.
    *   The other three edges are **closed boundaries**, meaning no flow can enter or exit through them.
6.  **Output:**
    *   The initial topographic elevation.
    *   The final distribution of water depth across the grid at the end of the simulation.

## Requirements

*   Python (3.8 or newer recommended)
*   [`uv`](https://github.com/astral-sh/uv) (for environment and package management)
*   The script itself (e.g., `overland_flow_simulation.py`)

## Setup and Installation (using `uv`)

1.  **Download the Script:**
    Save the Python script provided in the previous step to a file, for example, `overland_flow_simulation.py`.

2.  **Open your Terminal/Command Prompt.**

3.  **Navigate to the Directory:**
    Change to the directory where you saved the script.
    ```bash
    cd path/to/your/script_directory
    ```

4.  **Create and Activate a Virtual Environment using `uv`:**
    ```bash
    # Create the virtual environment (e.g., named .venv)
    uv venv

    # Activate the virtual environment
    # On macOS/Linux:
    source .venv/bin/activate
    # On Windows (PowerShell):
    .venv\Scripts\Activate.ps1
    # On Windows (CMD):
    .venv\Scripts\activate.bat
    ```
    Your terminal prompt should now indicate that you are in the virtual environment (e.g., `(.venv) your_prompt$`).

5.  **Install Required Python Packages using `uv`:**
    With the virtual environment activated, install Landlab and Matplotlib:
    ```bash
    uv pip install landlab matplotlib
    ```

## How to Run the Simulation

Once the setup is complete and the virtual environment is activated, run the script from your terminal:

```bash
python overland_flow_simulation.py
```

## Understanding the Output

The script will:

1.  Print status messages to the console as it sets up the grid, topography, and runs the simulation.
2.  Display two Matplotlib plot windows:
    *   **"Initial Topography"**: Shows the elevation map of the grid at the start.
    *   **"Final Water Depth"**: Shows the depth of water across the grid at the end of the simulated rainfall event. You should see water accumulated and flowing towards the open boundary.

## Customizing the Simulation

You can modify the simulation by changing the parameters defined at the beginning of the `overland_flow_simulation.py` script:

*   **Grid Parameters:**
    *   `nrows`, `ncols`: Number of rows and columns in the grid.
    *   `dx`: Grid cell spacing (resolution).
*   **Time Parameters:**
    *   `rainfall_intensity_mmhr`: How heavy the rain is.
    *   `simulation_duration_hr`: How long the simulation (and rainfall) lasts.
    *   `output_interval_hr`: How often to print status (can be used for intermediate plots too).
*   **OverlandFlow Component Parameters:**
    *   `manning_n`: Manning's roughness coefficient, representing the friction of the surface. Higher values mean rougher surfaces and slower flow.
    *   `h_init`: Initial water depth on the surface.
    *   `alpha`: Time-step coefficient for the solver (influences stability and speed).
*   **Topography:**
    Modify the lines under `"# --- 5. Create Topography ---"` to create different landforms (e.g., add a channel, a depression, or read from a DEM file if you have one).
*   **Boundary Conditions:**
    Change the arguments in `mg.set_closed_boundaries_at_grid_edges(...)` to alter which sides are open or closed.

After making changes, save the script and re-run it using `python overland_flow_simulation.py`.

## License

This script is typically provided for educational or illustrative purposes. If it were part of a larger project, a license like MIT or Apache 2.0 would be appropriate. For this example, consider it to be in the public domain or under a permissive license like MIT if you plan to distribute it.
```

**To use this README:**

1.  Save the Python script as `overland_flow_simulation.py` (or whatever name you prefer, just be consistent).
2.  Save the content above as `README.md` in the same directory as your Python script.
3.  Follow the "Setup and Installation" and "How to Run" instructions in the `README.md` file.