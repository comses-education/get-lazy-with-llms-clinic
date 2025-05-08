# Landlab Overland Flow Simulation with `uv`

This document describes how to set up and run the `overland_flow_simulation.py` script using `uv`, a fast Python package installer and resolver. The script simulates simple overland flow on a generated terrain using the Landlab toolkit.

## Prerequisites

1.  **Python:** Ensure you have Python installed (Python 3.8 or newer is recommended). You can download it from [python.org](https://www.python.org/).
2.  **`uv`:** If you don't have `uv` installed, you can install it via pipx (recommended) or pip:
    ```bash
    # Using pipx (recommended)
    pipx install uv

    # Or using pip (ensure pip is up-to-date)
    pip install uv
    ```
    Refer to the [official `uv` installation guide](https://github.com/astral-sh/uv#installation) for more options.
3.  **Script:** You need the `overland_flow_simulation.py` script that was previously generated. Save it in your working directory.

## Setup and Running the Simulation

Follow these steps to create a virtual environment, install dependencies, and run the script.

1.  **Navigate to your Project Directory:**
    Open your terminal or command prompt and change to the directory where you saved `overland_flow_simulation.py`.

    ```bash
    cd path/to/your/script_directory
    ```

2.  **Create a Virtual Environment with `uv`:**
    It's highly recommended to use a virtual environment to manage project dependencies.

    ```bash
    uv venv
    ```
    This will create a virtual environment named `.venv` in your current directory.

3.  **Activate the Virtual Environment:**
    *   On macOS and Linux:
        ```bash
        source .venv/bin/activate
        ```
    *   On Windows (Command Prompt):
        ```bash
        .venv\Scripts\activate.bat
        ```
    *   On Windows (PowerShell):
        ```bash
        .venv\Scripts\Activate.ps1
        ```
    Your terminal prompt should now indicate that the virtual environment is active (e.g., `(.venv) your-prompt$`).

4.  **Install Dependencies with `uv`:**
    The script requires `landlab`, `numpy`, and `matplotlib`. Install them using `uv pip install`:

    ```bash
    uv pip install landlab numpy matplotlib
    ```
    `uv` will resolve and install these packages and their dependencies quickly.

5.  **Run the Simulation Script:**
    Now that the environment is set up and dependencies are installed, you can run the Python script:

    ```bash
    python overland_flow_simulation.py
    ```

## Expected Output

When you run the script, you should see:

1.  **Console Output:**
    *   Messages like "Starting simulation..."
    *   Periodic updates showing the elapsed simulation time (e.g., "Time: 600.00 s / 3600.00 s, Rainfall: True").
    *   A final "Simulation finished." message.

2.  **Matplotlib Plot Windows:**
    *   One or more Matplotlib windows will appear, displaying plots of "Water Depth (m)" at different time intervals during the simulation.
    *   A final Matplotlib window showing the "Final Topography".

    *Note: Depending on your Matplotlib backend configuration and operating system, you might need to close each plot window manually for the script to proceed or finish.*

## Alternative: Using `requirements.txt` or `pyproject.toml` (Recommended for Projects)

For better project management and reproducibility, you can define dependencies in a `requirements.txt` or `pyproject.toml` file.

### Using `requirements.txt`

1.  Create a file named `requirements.txt` in your project directory with the following content:
    ```
    landlab
    numpy
    matplotlib
    ```
2.  Then, after activating the virtual environment (step 3), install dependencies using:
    ```bash
    uv pip install -r requirements.txt
    ```

### Using `pyproject.toml`

1.  Create a file named `pyproject.toml` in your project directory with the following content:
    ```toml
    [project]
    name = "landlab-overland-flow-demo"
    version = "0.1.0"
    description = "A simple Landlab overland flow simulation."
    dependencies = [
        "landlab",
        "numpy",
        "matplotlib",
    ]

    requires-python = ">=3.8"

    [build-system]
    requires = ["setuptools", "wheel"]
    build-backend = "setuptools.build_meta"
    ```
2.  After activating the virtual environment, you can install dependencies (and your "project" in editable mode if you were developing it as a package) using:
    ```bash
    uv pip install -e .
    ```
    Or, if you just want to install dependencies defined in `pyproject.toml` without treating the current directory as an installable package, you can first compile them to a lock file and then install (this is good for pinning versions):
    ```bash
    uv pip compile pyproject.toml -o requirements.lock
    uv pip sync --python $(which python) requirements.lock # Ensure you use the venv python
    # Or more simply for just installing dependencies:
    # uv pip install landlab numpy matplotlib # as before, uv can read dependencies from pyproject.toml implicitly in some contexts
    ```
    For simply running a script, `uv pip install landlab numpy matplotlib` after `uv venv` and activating it is the most straightforward if you don't want to create a `pyproject.toml` initially.

## Troubleshooting

*   **`uv: command not found`**: Ensure `uv` is installed and its installation directory is in your system's PATH. Refer to the `uv` installation guide.
*   **Matplotlib plots not showing / Backend issues**: If plots don't appear, you might need to configure your Matplotlib backend (e.g., by setting the `MPLBACKEND` environment variable or configuring `matplotlibrc`). For interactive use, backends like `QtAgg`, `TkAgg`, or `MacOSX` (on macOS) usually work well. If running in a headless environment, you might need a non-interactive backend like `Agg`.
*   **Dependency resolution issues**: `uv` is generally very good at this, but if you encounter problems, ensure your base Python version is compatible with the packages.