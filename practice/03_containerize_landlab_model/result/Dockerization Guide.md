## 1. Modified `overland_flow_simulation.py`

The script needs to be updated to save plots to files instead of displaying them interactively, which is suitable for running in a Docker container with the `Agg` Matplotlib backend.

```python
### FILE: `overland_flow_simulation.py`
import numpy as np
import matplotlib.pyplot as plt
from landlab import RasterModelGrid, imshow_grid
from landlab.components import OverlandFlow
from landlab.grid.nodestatus import NodeStatus
import os # Added for path operations and creating directory

# --- 0. Output Directory Setup ---
output_dir = "output_plots" # Define output directory name
# Create the directory if it doesn't exist.
# Docker will map a host volume to this path later.
os.makedirs(output_dir, exist_ok=True)

# --- 1. Grid Setup and Topography ---
# Create a 20x30 raster grid with 10m spacing
nrows = 20
ncols = 30
dx = 10.0  # m
mg = RasterModelGrid((nrows, ncols), xy_spacing=dx)

# Create a simple sloped topography (sloping towards x=0, node 0)
# Elevation decreases from right to left
z = mg.add_zeros("topographic__elevation", at="node")
z[:] = (mg.x_of_node / (ncols * dx)) * 10  # Max 10m elevation at right edge
z[:] = 10.0 - z[:] # Slope towards x=0

# Set boundary conditions
mg.status_at_node[mg.nodes_at_left_edge] = NodeStatus.FIXED_VALUE
mg.status_at_node[mg.nodes_at_right_edge] = NodeStatus.CLOSED
mg.status_at_node[mg.nodes_at_top_edge] = NodeStatus.CLOSED
mg.status_at_node[mg.nodes_at_bottom_edge] = NodeStatus.CLOSED

# --- 2. Initialize Water Depth Field ---
h = mg.add_zeros("surface_water__depth", at="node")
h[:] = 1.0e-12  # m, a very thin veneer of water

# --- 3. Instantiate OverlandFlow Component ---
overland_flow = OverlandFlow(mg, mannings_n=0.01, steep_slopes=True)

# --- 4. Simulation Parameters ---
total_sim_time = 3600.0  # seconds (1 hour)
storm_duration = 1800.0  # seconds (30 minutes of rain)
rainfall_intensity_m_per_s = 20.0 / (1000.0 * 3600.0) # 20 mm/hr

# Plotting parameters
plot_interval = 600.0  # seconds (plot every 10 minutes)
next_plot_time = plot_interval # Initialize next_plot_time

# --- 5. Simulation Loop ---
elapsed_time = 0.0
print("Starting simulation...")
while elapsed_time < total_sim_time:
    # Determine current rainfall rate
    if elapsed_time < storm_duration:
        overland_flow.rainfall_intensity = rainfall_intensity_m_per_s
    else:
        overland_flow.rainfall_intensity = 0.0

    # Calculate adaptive timestep (dt)
    # Start with the component's suggested dt
    dt_component = overland_flow.calc_time_step()
    dt = dt_component

    # Cap dt: first by total_sim_time
    if elapsed_time + dt > total_sim_time:
        dt = total_sim_time - elapsed_time
    
    # Then, cap dt by next_plot_time (if relevant and earlier than total_sim_time cap)
    # This ensures plotting occurs close to the desired next_plot_time.
    if next_plot_time <= total_sim_time and (elapsed_time + dt > next_plot_time):
        dt = next_plot_time - elapsed_time
    
    # Ensure dt is positive. If dt is zero (e.g. already at next_plot_time),
    # overland_flow might do nothing. The loop structure should handle this:
    # plot, advance next_plot_time, then next iteration will get a new dt_component.
    if dt <= 1e-9: # If dt is effectively zero
        if elapsed_time >= total_sim_time: # If at the end, dt=0 is fine, loop will break
            pass
        elif elapsed_time >= next_plot_time: # If at a plot time, dt=0 is fine, plot will occur
            pass
        else: # dt is zero unexpectedly, try to advance with a small step or component's step
              # This case should be rare with the above dt logic.
              # Forcing a minimal dt if not at a target time might be an option if issues arise.
              # For now, assume overland_flow handles dt=0 gracefully (likely by doing nothing).
              pass


    # Run the overland flow component for one timestep
    overland_flow.overland_flow(dt=dt)

    # Update elapsed time
    elapsed_time += dt

    # Plotting
    if elapsed_time >= next_plot_time or elapsed_time >= total_sim_time:
        print(f"Time: {elapsed_time:.2f} s / {total_sim_time:.2f} s, Rainfall: {overland_flow.rainfall_intensity > 0}. Plotting...")
        
        plt.figure(figsize=(8, 6)) # Create a new figure for each plot
        imshow_grid(
            mg,
            "surface_water__depth",
            plot_name=f"Water Depth at {elapsed_time/60.0:.1f} min",
            var_name="Water Depth (m)",
            var_units="m",
            grid_units=("m", "m"),
            cmap="Blues",
            vmin=0, vmax=0.1 # Adjust vmax as needed based on expected depths
        )
        plot_filename = f"water_depth_simtime{elapsed_time:.0f}s.png"
        plt.savefig(os.path.join(output_dir, plot_filename))
        plt.close() # Close the figure to free memory
        print(f"Saved plot: {os.path.join(output_dir, plot_filename)}")
        
        if elapsed_time < total_sim_time:
             next_plot_time += plot_interval
        # If elapsed_time == total_sim_time, loop will terminate after this.
        # next_plot_time is not advanced further, which is correct.

    # Break if total simulation time is reached
    if elapsed_time >= total_sim_time:
        break

print("Simulation finished.")

# Plot final topography and save it
plt.figure(figsize=(8,6))
imshow_grid(mg, "topographic__elevation", plot_name="Final Topography", cmap="terrain")
topography_filename = "final_topography.png"
plt.savefig(os.path.join(output_dir, topography_filename))
plt.close()
print(f"Saved final topography to: {os.path.join(output_dir, topography_filename)}")
```

## 2. `Dockerfile`

This `Dockerfile` sets up the environment, installs dependencies, and configures the application to run.

```dockerfile
### FILE: Dockerfile
# Use Python 3.9 slim image as a base
FROM python:3.9-slim-buster

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV MPLBACKEND="Agg" # For headless matplotlib, plots will be saved to files

# Add metadata labels
LABEL maintainer="Your Name <youremail@example.com>"
LABEL version="0.1.0"
LABEL description="Landlab Overland Flow Simulation"

# Set working directory
WORKDIR /app

# Copy only pyproject.toml first to leverage Docker cache for dependencies
COPY pyproject.toml .

# Install dependencies using pip and pyproject.toml
# --no-cache-dir reduces image size
# -e . installs the project in editable mode, which also installs dependencies from pyproject.toml
RUN pip install --no-cache-dir -e .

# Copy the rest of the application code
COPY . .

# Create a non-root user and switch to it for security
RUN useradd -m appuser
USER appuser

# Command to run the simulation script
# The script will save plots to "output_plots" directory inside /app
CMD ["python", "overland_flow_simulation.py"]
```

## 3. `docker-compose.yml`

This file makes it easier to manage the Docker container, especially for defining volumes.

```yaml
### FILE: docker-compose.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    image: landlab-overland-flow-demo:latest
    container_name: landlab_simulation_app
    # Mount the host's ./output_plots directory to /app/output_plots in the container
    # This persists the generated plots on your host machine.
    volumes:
      - ./output_plots:/app/output_plots
    # If you want to modify the script and re-run without rebuilding (for development):
    # volumes:
    #   - ./output_plots:/app/output_plots
    #   - ./overland_flow_simulation.py:/app/overland_flow_simulation.py
    #   - ./pyproject.toml:/app/pyproject.toml # If dependencies change, rebuild is still needed
```

## 4. `Makefile`

A `Makefile` provides convenient shortcuts for common Docker operations.

```makefile
### FILE: Makefile
# Define default image name and output directory
IMAGE_NAME ?= landlab-overland-flow-demo
OUTPUT_DIR_HOST ?= ./output_plots
OUTPUT_DIR_CONTAINER ?= /app/output_plots

.PHONY: all build run up down shell clean clean-output logs help

all: build run

help:
	@echo "Makefile for Landlab Overland Flow Simulation Docker application"
	@echo ""
	@echo "Usage:"
	@echo "  make build            Build the Docker image."
	@echo "  make run              Run the simulation using docker compose up (shows logs, then exits)."
	@echo "                        Equivalent to 'make up'."
	@echo "  make up               Start the service defined in docker-compose.yml."
	@echo "  make down             Stop and remove containers, networks defined in docker-compose.yml."
	@echo "  make shell            Open a bash shell inside a new container instance."
	@echo "  make clean-output     Remove the local output_plots directory."
	@echo "  make clean            Stop containers and remove local output_plots directory."
	@echo "  make logs             Follow logs from the running service (if detached)."
	@echo ""
	@echo "Variables:"
	@echo "  IMAGE_NAME          Override Docker image name (default: $(IMAGE_NAME))"
	@echo "  OUTPUT_DIR_HOST     Host directory for plots (default: $(OUTPUT_DIR_HOST))"

# Build the Docker image using docker-compose
build:
	@echo "Building Docker image..."
	docker compose build

# Run the simulation using docker compose up
# This will create the output directory on the host if it doesn't exist due to the volume mount.
run: up

up:
	@echo "Running simulation via docker compose up..."
	@echo "Output plots will be saved to $(OUTPUT_DIR_HOST)"
	mkdir -p $(OUTPUT_DIR_HOST) # Ensure host output directory exists
	docker compose up --remove-orphans

# Stop and remove containers, networks, etc.
down:
	@echo "Stopping and removing containers..."
	docker compose down -v

# Open a bash shell in a new container instance
shell:
	@echo "Opening bash shell in a new container instance..."
	docker compose run --rm app bash

# Remove the local output directory
clean-output:
	@echo "Removing local output directory: $(OUTPUT_DIR_HOST)"
	rm -rf $(OUTPUT_DIR_HOST)

# Clean everything: stop containers and remove output
clean: down clean-output

# Follow logs (useful if 'docker compose up -d' was used)
logs:
	@echo "Following logs..."
	docker compose logs -f
```

## 5. `.gitignore` (Recommended)

Create a `.gitignore` file to keep your Git repository clean.

```gitignore
### FILE: .gitignore
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/

# Docker
output_plots/

# IDE / OS specific
.vscode/
.idea/
*.DS_Store
```

## 6. Updated `README.md`

The `README.md` should be updated to include instructions for Docker.

```md
### FILE: `README.md`
# Landlab Overland Flow Simulation

This document describes how to set up and run the `overland_flow_simulation.py` script.
The script simulates simple overland flow on a generated terrain using the Landlab toolkit.
You can run this simulation either using Docker (recommended for consistency and ease of setup) or locally using `uv`.

## Prerequisites

1.  **Python:** (For local development without Docker) Ensure you have Python installed (Python 3.8 or newer is recommended).
2.  **`uv`:** (For local development without Docker) A fast Python package installer. See installation instructions below.
3.  **Docker & Docker Compose:** (For Docker setup) Ensure Docker and Docker Compose are installed on your system.
    *   [Install Docker Engine](https://docs.docker.com/engine/install/)
    *   [Install Docker Compose](https://docs.docker.com/compose/install/)

## Option 1: Running with Docker (Recommended)

This method uses Docker to create a consistent environment for running the simulation. Plots generated by the simulation will be saved to an `output_plots` directory on your host machine.

1.  **Ensure Files are Present:**
    Make sure you have the following files in your project directory:
    *   `overland_flow_simulation.py` (the version modified to save plots)
    *   `pyproject.toml`
    *   `Dockerfile`
    *   `docker-compose.yml`
    *   `Makefile` (optional, but provides convenient commands)

2.  **Build the Docker Image:**
    Open your terminal in the project directory and run:
    ```bash
    make build
    ```
    Alternatively, without `make`:
    ```bash
    docker compose build
    ```

3.  **Run the Simulation:**
    To run the simulation:
    ```bash
    make run
    ```
    Alternatively, without `make`:
    ```bash
    docker compose up
    ```
    This will start the simulation. You'll see console output, and upon completion, plot images (e.g., `water_depth_simtime600s.png`, `final_topography.png`) will be saved in the `./output_plots` directory on your host machine.

4.  **Accessing a Shell inside the Container (for debugging/exploration):**
    ```bash
    make shell
    ```
    Alternatively, without `make`:
    ```bash
    docker compose run --rm app bash
    ```

5.  **Cleaning Up:**
    *   To remove the generated plots:
        ```bash
        make clean-output
        ```
    *   To stop and remove the Docker containers, networks, and volumes defined in `docker-compose.yml`:
        ```bash
        make down
        ```
    *   To do both:
        ```bash
        make clean
        ```

### Note on Interactive Plots with Docker (Advanced)

The provided Docker setup uses the `Agg` backend for Matplotlib, which is non-interactive and saves plots to files. If you need to display plots interactively from within the Docker container (e.g., for debugging), you would typically need to:
1.  Modify the `Dockerfile` to install necessary X11 client libraries (e.g., `python3-tk` or `python3-qt5`) and potentially remove/override `ENV MPLBACKEND="Agg"`.
2.  Configure X11 forwarding when running the container (e.g., by setting the `DISPLAY` environment variable and mounting `/tmp/.X11-unix`). This can be complex and platform-dependent.
For most use cases, saving plots to files is more straightforward with Docker.

## Option 2: Local Development Setup (without Docker)

This section describes how to set up and run the script directly on your machine using `uv`.

1.  **Navigate to your Project Directory:**
    Open your terminal or command prompt and change to the directory where `overland_flow_simulation.py` and `pyproject.toml` are located.

2.  **Install `uv` (if not already installed):**
    ```bash
    # Using pipx (recommended)
    pipx install uv
    # Or using pip
    pip install uv
    ```

3.  **Create and Activate a Virtual Environment with `uv`:**
    ```bash
    uv venv
    source .venv/bin/activate  # On macOS/Linux
    # .venv\Scripts\activate.bat  # On Windows CMD
    # .venv\Scripts\Activate.ps1 # On Windows PowerShell
    ```

4.  **Install Dependencies with `uv`:**
    Dependencies are defined in `pyproject.toml`. You can install them using:
    ```bash
    uv pip install -e .
    ```
    This installs the project and its dependencies. Alternatively, to just install dependencies:
    ```bash
    uv pip install landlab numpy matplotlib
    ```

5.  **Run the Simulation Script:**
    ```bash
    python overland_flow_simulation.py
    ```
    If running locally and you haven't modified the script to save plots (i.e., it still uses `plt.show()`), Matplotlib windows will appear. If you are using the modified script that saves plots, they will appear in the `output_plots` directory.

## Expected Output (from script logic)

1.  **Console Output:**
    *   Messages like "Starting simulation..."
    *   Periodic updates showing the elapsed simulation time and plotting actions.
    *   A final "Simulation finished." message.
    *   Messages indicating where plots are saved (e.g., "Saved plot: output_plots/water_depth_simtime600s.png").

2.  **Saved Plot Files (in `output_plots` directory):**
    *   Image files for "Water Depth (m)" at different time intervals.
    *   An image file for the "Final Topography".

## Project Structure (with Docker files)

```
.
├── Dockerfile
├── Makefile
├── README.md
├── docker-compose.yml
├── overland_flow_simulation.py
├── pyproject.toml
├── output_plots/          # Created when simulation runs, contains plot images
└── .gitignore             # Optional, for version control
```

## Troubleshooting

*   **Docker Issues:**
    *   Ensure Docker daemon is running.
    *   Permission errors when running `docker` commands: You might need to run Docker commands with `sudo` or add your user to the `docker` group.
    *   Volume mount issues: Ensure the path `./output_plots` is writable by the user Docker runs as, or check Docker's file sharing settings (especially on Docker Desktop for Windows/macOS).
*   **`uv: command not found`**: (For local setup) Ensure `uv` is installed and its installation directory is in your system's PATH.
*   **Matplotlib plots not showing / Backend issues (Local Setup)**: If using `plt.show()` locally and plots don't appear, you might need to configure your Matplotlib backend.
*   **Dependency resolution issues**: `uv` is generally very good at this, but if you encounter problems, ensure your base Python version is compatible with the packages.